'''
    relevant bits for debugging the collision issue
'''

from meta import *

from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase

import sys
import math

class _Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # init collision system
        base.cTrav = CollisionTraverser()
        base.cTrav.setRespectPrevTransform(True) # continuous collision checking
        base.pusher = CollisionHandlerPusher()
# end class

class _Environment:
    def __init__(self):
        self.plane = _Plane() # floor

class _Plane:
    def __init__(self):
        self.node=NodePath('plane')
        self.node.setPos(0,0,0)
        plane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
        cn = CollisionNode('csolid')
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.bit(0))
        cn.addSolid(plane)
        solid = self.node.attachNewNode(cn)
        solid.show()
##        base.cTrav.addCollider(solid, base.pusher)
        base.pusher.addCollider(solid, self.node)
    # end def

class _Player:
    def __init__(self):
        ''' inits the player '''
        #....
        taskMgr.add(self.statusUpdate, 'status-task')
        #....
        
    def init_collisions(self):
        ''' create a collision solid and ray for the player '''
        cn = CollisionNode('cplayer')
        cn.addSolid(CollisionSphere(0,0,0,3))
        solid = self.node.attachNewNode(cn)
        base.cTrav.addCollider(solid,base.pusher)
        base.pusher.addCollider(solid,self.node)
        # bitmasks 
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        # init players floor collisions
        ray = CollisionRay()
        ray.setOrigin(0,0,-.2)
        ray.setDirection(0,0,-1)
        cn = CollisionNode('cplayerRay')
        cn.addSolid(ray)
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        solid = self.node.attachNewNode(cn)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)
    # end def
        
    def statusUpdate(self,task):
        #....
        self.grounded=False

        # get the highest Z from collisions w/ the downward ray
        highestZ = -100
        for i in range(self.nodeGroundHandler.getNumEntries()):
            entry = self.nodeGroundHandler.getEntry(i)
            z = entry.getSurfacePoint(render).getZ()
            print("player collided with: ", entry.getIntoNode().getName())
            if z > highestZ and entry.getIntoNode().getName() == "csolid":
                highestZ = z
        # ground if we've collided with a floor
        if highestZ > self.node.getZ()-.3:
            self.node.setZ(highestZ+.3) # set Z to floor height
            self.moveZ = 0              # stop downward momentum
            self.grounded=True          # we're on solid ground
                
        return task.cont

 
