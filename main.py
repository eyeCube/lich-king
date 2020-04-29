'''
    
'''

from meta import *

from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase

import sys
import math

    #-----------#
    #  classes  #
    #-----------#

class Global:
    env = None
    game = None

class _Options:
    ''' global variables '''
    FOV=100
    
class _Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        base.disableMouse()
        base.accept( "escape" , sys.exit)   # controls to close the game
        
        # window properties
        properties = WindowProperties()
        properties.setSize(1024, 768)
        self.win.requestProperties(properties)
        
        # init collision system
        base.cTrav = CollisionTraverser()
        base.cTrav.setRespectPrevTransform(True) # continuous collision checking
        base.pusher = CollisionHandlerPusher()
# end class

class _Environment:
    def __init__(self):
        # load level (TODO: move to sep. cls)
        # load assets
##        self.environment = game().loader.loadModel("Models/Sample/Environment/environment")
##        self.environment.reparentTo(game().render)
        
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
    '''
        the main actor | Player Character (PC)
        controls the camera (first-person controller)
    '''
    # constants
    PITCH_MAX = 85      # max degrees you can look up or down
    
    # states
    STATE_NORMAL = 0
    STATE_FROZEN = 1
    
    # stats
    SPEED = 100
    ACCELERATION = 0.1 # max speed vector: 1
# having different acceleration values for forward/back resulted
#   in a weird glitch where we wouldn't move in the right direction.
    FRICTION_MULT = 0.9
    GRAVITY = 2
    
    def __init__(self):
        ''' inits the player '''
        self.init_states()
        self.init_control()
        self.init_model()
        self.init_camera()
        self.init_collisions()
        self.init_controls()
        taskMgr.add(self.statusUpdate, 'status-task')
        taskMgr.add(self.mouseUpdate, 'mouse-task')
        taskMgr.add(self.moveUpdate, 'move-task')
        taskMgr.add(self.keyUpdate, 'input-task')
    # end def

    def __del__(self):
        taskMgr.remove('mouse-task')
        taskMgr.remove('move-task')
        taskMgr.remove('input-task')
    # end def

    def init_states(self):
        self.state = self.STATE_NORMAL
        self.readyToJump = False
        self.grounded = False
    
    def init_control(self):
        # controls: player input
        self.control_fb = V_ZERO        # player input for walking forward/back
        self.control_strafe = V_ZERO    # strafing left/right
        self.moveZ = 0      # vertical (up/down movement)
        self.moveY = 0      # forward/back movement
        self.moveX = 0      # strafe movement
    # end def
        
    def init_model(self):
        ''' make the nodepath for player '''
        self.node = NodePath('player')
        self.node.reparentTo(render)
        self.node.setPos(0,0,4)
        self.node.setScale(.05)
        addnode(self, 'body')
    # end def
    
    def init_camera(self):
        ''' puts camera at the players node '''
        pl =  base.cam.node().getLens()
        pl.setFov(_Options.FOV)
        base.cam.node().setLens(pl)
        base.camera.reparentTo(self.body)
    # end def
        
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
        
    def init_controls(self):
        ''' attach key events '''
        base.accept("space",    self.jump_ready)
        base.accept("space-up", self.jump_unready)
        base.accept("w",        self.walk_forward)
        base.accept("w-up",     self.walk_forward_stop)
        base.accept("s",        self.walk_back)
        base.accept("s-up",     self.walk_back_stop)
        base.accept("a",        self.walk_left)
        base.accept("a-up",     self.walk_left_stop)
        base.accept("d",        self.walk_right)
        base.accept("d-up",     self.walk_right_stop)
        base.accept("r", self.reset)
    # end def

    def reset(self):
        self.node.setX(0)
        self.node.setY(0)
        self.node.setZ(10)
        self.moveZ=0
    def jump_ready(self):
        self.readyToJump = True
    def jump_unready(self):
        self.readyToJump = False
    def walk_forward(self):
        if self.control_fb != BACK: self.control_fb = FORWARD
    def walk_forward_stop(self):
        if self.control_fb == FORWARD: self.control_fb = STOP
    def walk_back(self):
        self.control_fb = BACK # priority over forward
    def walk_back_stop(self):
        if self.control_fb == BACK: self.control_fb = STOP
    def walk_left(self):
        if self.control_strafe != RIGHT: self.control_strafe = LEFT
    def walk_left_stop(self):
        if self.control_strafe == LEFT: self.control_strafe = STOP
    def walk_right(self):
        self.control_strafe = RIGHT # priority over left
    def walk_right_stop(self):
        if self.control_strafe == RIGHT: self.control_strafe = STOP
        
    def move_set(self, xs,ys):
        ''' set & constrain X,Y movement speeds '''
        self.moveX = max(-1, min(1, xs))
        self.moveY = max(-1, min(1, ys))
    def move(self, value, angle_mod):
        ''' alter X,Y movement speeds by the value and angle given '''
        spin = degtorad(self.body.getH()+angle_mod)
        xr = -value*math.sin(spin) # make it relative from the body
        yr = value*math.cos(spin)  # to the world using trigonometry
        self.move_set(self.moveX + xr, self.moveY + yr)
    def move_fb(self, value):
        self.move(value, 0)
    def move_strafe(self, value):
        self.move(value, -90)
        
    def mouseUpdate(self,task):
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if base.win.movePointer(0, base.win.getXSize()//2, base.win.getYSize()//2):
            pitch = self.body.getP() - (y - base.win.getYSize()//2)*0.1
            pitch = max(-self.PITCH_MAX, min(self.PITCH_MAX, pitch))
            self.body.setH(self.body.getH() - (x - base.win.getXSize()//2)*0.1)
            self.body.setP(pitch)
        return task.cont
    # end def

    def statusUpdate(self,task):
        if self.state==self.STATE_NORMAL:
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

    def keyUpdate(self,task):
        ''' update from key input states '''
        if self.state==self.STATE_NORMAL:
            
            # movement controls
            if self.control_fb == FORWARD:
                self.move_fb(self.ACCELERATION)
            elif self.control_fb == BACK:
                self.move_fb(-self.ACCELERATION)
            if self.control_strafe == LEFT:
                self.move_strafe(-self.ACCELERATION)
            elif self.control_strafe == RIGHT:
                self.move_strafe(self.ACCELERATION)
            # friction
##            if self.grounded:
            self.moveX = self.moveX*self.FRICTION_MULT
            self.moveY = self.moveY*self.FRICTION_MULT
##            else:
            self.moveZ -= self.GRAVITY*globalClock.getDt()
            
        return task.cont
    
    def moveUpdate(self,task):
        ''' update position based on X, Y, and Z inertia '''
        
        if self.state==self.STATE_NORMAL:
            # walking motion
            walk=Vec3(self.moveX,self.moveY,0) # create vector w/ length <= 1
            if math.sqrt(self.moveX**2 + self.moveY**2) > 1:
                walk = walk.normalized() # don't move faster diagonally.
                
            # momentum -> update position
            self.node.setPos(self.node,walk*self.SPEED*globalClock.getDt())
            
            if self.grounded:
                if self.readyToJump:
                    self.moveZ = 1
            
            # vertical momentum
            self.node.setZ(self.node.getZ()+self.moveZ*globalClock.getDt())
        
        return task.cont
    # end def
# end class

    #-----------#
    # functions #
    #-----------#

def game(): return Global.game
def player(): return Global.player
def degtorad(degs): return math.pi*degs/180
def radtodeg(degs): return 180*degs/math.pi

def addnode(obj, name):
    ''' add a node to the object obj named name '''
    obj.__dict__[name] = NodePath(name)
    obj.__dict__[name].reparentTo(obj.node)
    
def main():
    Global.game = _Game()
    Global.player = _Player()
    Global.env = _Environment()
    Global.game.run()
    
if __name__=="__main__":
    main()

