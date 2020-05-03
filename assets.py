'''
    assets.py

    Models, collision data, interactivity, and anything else
    associated with assets.
'''

from meta import *
import game

from panda3d.core import *

class GameObject:
    def __init__(self, model:str, x=0, y=0, z=0):
        self.node=NodePath('node')
        self.node.reparentTo(game.game().render)
        self.node.setPos(x,y,z)
##        self.node.setPythonTag('solid',True)
        # NOTE TO SELF: we can use setPythonTag on non-solid things
        # like weapons collision boxes, enemies, etc.
        # to identify them without having to use names or strings.
        # This is what we will do, but not for solid things,
        # because the automatic solid geometry thing from the .egg
        # file does not reparent the collision nodes to the node
        # of the object.
        # Just reparent collisionSpheres for enemies, etc. onto the
        # enemy node. We can do this since we create those colliders
        # manually. Give them the notsolid tag.
        
        # load assets
        self.model = game.game().loader.loadModel(model)
##        self.model.setZ(-1)
        self.model.reparentTo(self.node)
        
        # load collision geometry
        self.model = game.game().loader.loadModel(model+"_collision")
##        self.model.setZ(-1)
        self.model.reparentTo(self.node)

        # collisions (TODO)
        
##        plane = CollisionBox(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
##        cn = CollisionNode('csolid')
##        cn.setFromCollideMask(BitMask32.bit(0))
##        cn.setIntoCollideMask(BitMask32.bit(0))
##        cn.addSolid(plane)
##        solid = self.node.attachNewNode(cn)
####        solid.show()
####        base.cTrav.addCollider(solid, base.pusher)
##        base.pusher.addCollider(solid, self.node)
# end class

    #--------#
    # static #
    #--------#

    # ( S_ == static )

class S_Plane: # floor plane
    def __init__(self):
        self.node=NodePath('node')
        self.node.reparentTo(game.renderer())
        self.node.setPos(0,0,0)
        point=Point3(0, 0, 0)
        vec=Vec3(0, 0, 1)
        plane = CollisionPlane(Plane(vec, point))
        cn = CollisionNode('plane')
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.bit(0))
        cn.addSolid(plane)
        solid = self.node.attachNewNode(cn)
##        solid.show()
##        base.cTrav.addCollider(solid, base.pusher)
        base.pusher.addCollider(solid, self.node)
# end class
    
class S_Corridor_Arched_1_Corner(GameObject):
    def __init__(self, x=0, y=0, z=0):
        super(S_Corridor_Arched_1_Corner,self).__init__(
            "Models/corridor_arch1_corner", x,y,z)
        
class S_Corridor_Arched_1(GameObject):
    def __init__(self, x=0, y=0, z=0):
        super(S_Corridor_Arched_1,self).__init__(
            "Models/corridor_arch1", x,y,z,)

class S_Corridor_Stairs_1(GameObject):
    def __init__(self, x=0, y=0, z=0):
        super(S_Corridor_Stairs_1,self).__init__(
            "Models/corridor_stairs1", x,y,z)

# list of all assets
ASSETS={
ASSET_PLANE_SOLID : S_Plane,
ASSET_CORRIDOR_ARCHED_1_CORNER : S_Corridor_Arched_1_Corner,
ASSET_CORRIDOR_ARCHED_1 : S_Corridor_Arched_1,
ASSET_CORRIDOR_STAIRS_1 : S_Corridor_Stairs_1,
    }









