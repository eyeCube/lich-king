'''
    assets.py

    Models, collision data, interactivity, and anything else
    associated with assets.
'''

import os
from panda3d.core import *
import random

from meta import *
import game

MODELSDIR = "../Models/" #os.path.join("..","Models","") #<-- not working for some ungodly reason
##CONFIGFILE = os.path.join(os.path.dirname(__file__),"..","config","Config.prc")
##loadPrcFile(CONFIGFILE)

def fm(model:str) -> str: # format model
    return "{}{}".format(MODELSDIR,model)

class Asset:
    def __init__(self):
        self.flags=set()

class Static: # solid unmoving object
    # has an (x,y,z) position, a model, and a hidden collision model
    # with the name of the model + "_collision".
    # The collision model should be as simple as possible.
    # The collider can only be a solid object.
    # To have game objects with interactive nonsolid colliders, use
    # GameObject class.
    def __init__(self, model:str, x=0, y=0, z=0):
        self.node=NodePath('node')
        self.node.reparentTo(game.environment_layer())
        self.node.setPos(x,y,z)
        
        # load assets
        self.model = game.game().loader.loadModel(model)
##        self.model.setZ(-1)
        self.model.reparentTo(self.node)
        
        # load collision geometry
        self.collision = game.game().loader.loadModel(model+"_collision")
##        self.model.setZ(-1)
        self.collision.reparentTo(self.node)
        self.collision.hide() # make collision geometry invisible!
# end class

class GameObject: # nonsolid object
        # NOTE TO SELF: we can use setPythonTag on non-solid things
        # like weapons collision boxes, enemies, etc.
        # to identify them without having to use names or strings.
        # This is what we will do, but not for solid things,
        # because the automatic solid geometry thing from the .egg
        # file does not reparent the collision nodes to the node
        # of the object.
        # Just reparent collisionSpheres for enemies, etc. onto the
        # enemy node. We can do this since we create those colliders
        # manually. Give them the notSolid tag.
    def __init__(self, model:str, layer=None, tags={}, x=0, y=0, z=0):
        layer = game.environment_layer() if layer is None else layer
        self.node=NodePath('node')
        self.node.reparentTo(layer)
        self.node.setPos(x,y,z)
        for tag,value in tags.items():
            self.node.setPythonTag(tag,value)
        
        # load assets
        if model:
            self.model = game.game().loader.loadModel(model)
            self.model.reparentTo(self.node)

    def interact(self, _type):
        pass

class GameSphere(GameObject): # nonsolid spherical object
    def __init__(self,
                 model:str, interactFunc,
                 radius=1, tags={}, x=0, y=0, z=0
                 ):
        super(GameSphere, self).__init__(model,tags,x,y,z)
        
        # create collision geometry
        self.collision = CollisionSphere(0,0,0,radius)
        self.collision.reparentTo(self.node)
        self.interact = interactFunc

      
    #--------------#
#---# object types #---------------------------------------------------#
    #--------------#

    #----------#
    # triggers #
    #----------#

class Load_Trigger(GameObject):
    ID = ASSET_TRIGGER_LOAD
    def __init__(self,model:str,zone:int,x=0,y=0,z=0):
        GameObject.__init__(
            self, None,
            layer=game.object_layer(), x=x,y=y,z=z,
            tags={'trigger':self.trigger_func}
            )
        self.zone = zone # ZONE_ const
        
        # load collision geometry
        self.collision = game.game().loader.loadModel(model)
##        self.model.setZ(-1)
        self.collision.reparentTo(self.node)
        self.collision.hide() # make collision geometry invisible!
    def trigger_func(self):
        game.unload_zone() # unload current area/room/scene/zone
        game.load_zone(self.zone)
# end class
class Load_Trigger_Rect(Load_Trigger):
    def __init__(self,x=0,y=0,z=0,rotz=0):
        Load_Trigger.__init__(self,x=x,y=y,z=z)
        self.node.setH(rotz)

    #--------#
    # static #
    #--------#

class Static_Plane(Asset): # flat floor plane
    ID = ASSET_PLANE_SOLID
    def __init__(self,x=0,y=0,z=0):
        Asset.__init__(self)
        self.node=NodePath('node')
        self.node.reparentTo(game.renderer())
        self.node.setPos(0,0,0)
        point=Point3(x,y,z)
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
    
class Static_Corridor_Arched_1_Corner(Static, Asset):
    ID = ASSET_CORRIDOR_ARCHED_1_CORNER
    def __init__(self, x=0, y=0, z=0):
        Static.__init__(self,
            fm("corridor_arch1_corner"), x,y,z)
        Asset.__init__(self)
        
class Static_Corridor_Arched_1(Static, Asset):
    ID = ASSET_CORRIDOR_ARCHED_1
    def __init__(self, x=0, y=0, z=0):
        Static.__init__(self,
            fm("corridor_arch1"), x,y,z,)
        Asset.__init__(self)

class Static_Corridor_Stairs_1(Static, Asset):
    ID = ASSET_CORRIDOR_STAIRS_1
    def __init__(self, x=0, y=0, z=0):
        Static.__init__(self,
            fm("corridor_stairs1"), x,y,z)
        Asset.__init__(self)

    #-------#
    # decor #
    #-------#
    
class Decor_Fern_1(GameObject, Asset):
    ID = ASSET_DECOR_FERN_1
    def __init__(self, x=0, y=0, z=0):
        model=random.choice( (fm("fern"),fm("fern2"),) )
        GameObject.__init__(self,
            model, x=x,y=y,z=z)
        Asset.__init__(self)
        self.node.setH(random.random()*360)

    #--------#
    # scenes #
    #--------#
    
class Scene_1(Static, Asset):
    ID = ASSET_SCENE_TEST_1
    def __init__(self, x=0, y=0, z=0):
        Static.__init__(
            self,
            fm("scene1"),
            x,y,z
            )
        Asset.__init__(self)
    
class Scene_Courtyard(Static, Asset):
    ID = ASSET_SCENE_COURTYARD_1
    def __init__(self, x=0, y=0, z=0):
        Static.__init__(
            self,
            fm("lordland-courtyard"),
            x,y,z
            )
        Asset.__init__(self)
    
class Scene_Courtyard_Rock(Static, Asset):
    ID = ASSET_SCENE_COURTYARD_1
    def __init__(self, x=0, y=0, z=0):
        Static.__init__(
            self,
            fm("lordland-courtyard-rock"),
            x,y,z
            )
        Asset.__init__(self)

# list of all assets
ASSETS={
Static_Plane.ID : Static_Plane,
Static_Corridor_Arched_1_Corner.ID : Static_Corridor_Arched_1_Corner,
Static_Corridor_Arched_1.ID : Static_Corridor_Arched_1,
Static_Corridor_Stairs_1.ID : Static_Corridor_Stairs_1,
Decor_Fern_1.ID : Decor_Fern_1,
Scene_1.ID : Scene_1,
    }
EDITOR_ASSETS=(
    Static_Corridor_Arched_1_Corner.ID,
    Static_Corridor_Arched_1.ID,
    Static_Corridor_Stairs_1.ID,
    Decor_Fern_1.ID,
    )









