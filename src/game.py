'''
    game.py

    Classes and functions for the main game engine for Lich King
    Action-Adventure / RPG copyright by Jacob Wharton
'''

from meta import *
import assets
import levels

from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec4

import sys
import math

''' imported keywords from panda3d.core:

global:
    render
    base

classes:
    ShowBase
    WindowProperties
    CollisionTraverser
    CollisionHandlerPusher
    AmbientLight
    DirectionalLight
    NodePath
    CollisionNode
    CollisionRay
    CollisionHandlerQueue
    Vec3
    Point3
'''

    #-----------#
    #  classes  #
    #-----------#

class Global:
    env = None
    game = None
    editor = None

class _Options:
    ''' global variables '''
    FOV=100
    
class _Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.base = base
        base.disableMouse()
        base.accept("escape", sys.exit)   # controls to close the game / quit the game 
        
        # window properties
        properties = WindowProperties()
        properties.setSize(1024, 768)
        self.win.requestProperties(properties)
        
        # init collision system
        base.cTrav = CollisionTraverser()
        base.cTrav.setRespectPrevTransform(True) # continuous collision checking
        base.pusher = CollisionHandlerPusher()
    
    def init_lighting(self):
        ambientLight = AmbientLight("ambient")
        ambientLight.setColor(Vec4(0.15, 0.15, 0.1, 1))
        self.ambientLight = render.attachNewNode(ambientLight)
        environment_layer().setLight(self.ambientLight)
        sun = DirectionalLight("sun")
        sun.setColor(Vec4(1.5, 1.5, 1.5, 1))
        self.sun = render.attachNewNode(sun)
        self.sun.setHpr(0, -45, 0) # aimed northward and down at 45 degrees (if north is up on the blender map from top-down view)
        environment_layer().setLight(self.sun)
        environment_layer().setShaderAuto()
##        sun.setShadowCaster(True, 512, 512)
            # scene cannot self shadow (?) -- need to divide scene into
            # multiple different objects? Is this worth it? Well, we need
            # to have shadows, right?
# end class

class _Environment:
    def __init__(self):
        self.layer = NodePath("environment_layer")
        self.layer.reparentTo(renderer())
        self.statics=[]

    def load_level(self):
        # load assets
##        self.environment = game().loader.loadModel("Models/Sample/Environment/environment")
##        self.environment.setZ(0)
##        self.environment.reparentTo(game().render)
        
        self.add_static(assets.Scene_1(0,0,-10))
##        self.add_decor(assets.Decor_Fern_1())
        
##        self.add_static(assets.Static_Plane())
##        self.add_static(assets.Static_Corridor_Arched_1(0,0,0))
##        self.add_static(assets.Static_Corridor_Arched_1(), 0, 2, 0)
##        self.add_static(assets.Static_Corridor_Arched_1_Corner(), 0, 4, 0)
##        self.add_static(assets.Static_Corridor_Stairs_1(), 2, 4, 0)
##        self.add_static(assets.Static_Corridor_Stairs_1(), 4, 4, 1.5)
        
    def add_static(self, static, x=0, y=0, z=0):
        static.node.setPos(static.node, x,y,z)
        self.statics.append(static)
# end class

        
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
    
# having different acceleration values for forward/back resulted
#   in a weird glitch where we wouldn't move in the right direction.
    FRICTION_MULT = 0.9
    GRAVITY = GLOBAL_GRAVITY
    TERMINALVELOCITY = 66 # IRL == 66 m/s
    RUN_SPEED_MULT = 1.5
    
    def __init__(self):
        ''' inits the player '''
        self.init_states()
        self.init_stats()
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
        self.walking = False
        self.walkingToggled = False     # this var improves player control by making the toggle run button flip the control of the Shift run key.
        self.prevX = -999
        self.prevY = -999
        self.prevZ = -999
    
    def init_stats(self):
        self.scale = 0.05
        self.speed = 50     # start: 50, soft cap: ~150
        self.jump = 2.5       # start: 2, soft cap: ~3.5
        self.acceleration = 0.1 # max speed vector: 1
        self.lifeMax = 100      # maximum life points
        self.life = self.lifeMax
        self.manaMax = 10       # maximum magic points
        self.mana = self.manaMax
        self.staminaMax = 200   # maximum stamina points
        self.stamina = self.staminaMax
        self.strength = 12      # physical power
        self.wisdom = 12        # magical power
        self.armor = 0          # physical damage reduction (linear)
        self.res_slash = 100    # resistances - % damage reduction
        self.res_stab = 100
        self.res_crush = 100
        self.res_fire = 100
        self.res_elec = 100
        self.res_water = 100
        self.pow_slash = 0      # damage dealt with certain damage types
        self.pow_stab = 0
        self.pow_crush = 0
        self.pow_fire = 0
        self.pow_elec = 0
        self.pow_water = 0

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
        self.node.setPos(0,0,0.5)
        # Set player scale to 1/20; this effects everything!
        # Every unit needs to be scaled up 20x to be consistent with the world.
        self.node.setScale(self.scale)
        self.body = NodePath('body')
        self.body.reparentTo(self.node)
        self.head = NodePath('head')
        self.head.reparentTo(self.body)
        self.head.setPos(self.body,0,0,1.5/self.scale)
    # end def
    
    def init_camera(self):
        ''' puts camera at the players node '''
        pl =  base.cam.node().getLens()
        pl.setFov(_Options.FOV)
        base.cam.node().setLens(pl)
        base.camera.reparentTo(self.head)
            # is the camera centered in the sphere of collision? Need to move camera above and forward slightly.
    # end def
        
    def init_collisions(self):
        ''' create a collision solid and ray for the player '''
        # IDEA: use two or more collisionSphere's in order to simulate
        # different body parts: at least head/torso?

        # head (TODO)
        # torso (TODO)
        
        # pusher -- this collisionSphere keeps us out of walls.
        # THIS IS NOT THE COLLIDER FOR GETTING DAMAGED BY ENEMIES.
        cn = CollisionNode('cplayer')
        cn.addSolid(CollisionSphere(0,0,1/self.scale,0.33/self.scale))#CollisionCapsule(0,0,-1,0,0,1,1))
        solid = self.node.attachNewNode(cn)
        base.cTrav.addCollider(solid,base.pusher)
        base.pusher.addCollider(solid,self.node)
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        # downcast ray for floor collisions
        ray = CollisionRay()
        ray.setOrigin(0,0,1/self.scale)
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
        # game control
        base.accept("shift-r",      self.reset)
        # player control
        base.accept("r",            self.walk_toggle)
        base.accept("shift",        self.walk_on)
        base.accept("shift-up",     self.walk_off)
        base.accept("space",        self.jump_ready)
        base.accept("space-up",     self.jump_unready)
        base.accept("w",            self.walk_forward)
        base.accept("w-up",         self.walk_forward_stop)
        base.accept("s",            self.walk_back)
        base.accept("s-up",         self.walk_back_stop)
        base.accept("a",            self.walk_left)
        base.accept("a-up",         self.walk_left_stop)
        base.accept("d",            self.walk_right)
        base.accept("d-up",         self.walk_right_stop)
        base.accept("shift-w",      self.walk_forward)
        base.accept("shift-w-up",   self.walk_forward_stop)
        base.accept("shift-s",      self.walk_back)
        base.accept("shift-s-up",   self.walk_back_stop)
        base.accept("shift-a",      self.walk_left)
        base.accept("shift-a-up",   self.walk_left_stop)
        base.accept("shift-d",      self.walk_right)
        base.accept("shift-d-up",   self.walk_right_stop)
    # end def

    def reset(self):
        self.node.setX(0)
        self.node.setY(0)
        self.node.setZ(3)
        self.moveZ=0
    def walk_toggle(self):
        self.walkingToggled = False if self.walkingToggled else True
    def walk_on(self):
        self.walking = True
    def walk_off(self):
        self.walking = False
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
        spin = degtorad(self.head.getH()+angle_mod)
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
            pitch = self.head.getP() - (y - base.win.getYSize()//2)*0.1
            pitch = max(-self.PITCH_MAX, min(self.PITCH_MAX, pitch))
            self.head.setH(self.head.getH() - (x - base.win.getXSize()//2)*0.1)
            self.head.setP(pitch)
        return task.cont
    # end def
    
    def statusUpdate(self,task):
        if self.state==self.STATE_NORMAL:
            self.grounded=False
            
            # get the highest Z from collisions w/ the downward ray
            highestZ = -99999
            # also collect information about the ground type below us
            floor_slipperiness = 0 # vertical friction (Z)
            floor_friction = 0 # horizontal friction (X/Y)
            floor_damage = 0
            floor_damageType = 0
            for i in range(self.nodeGroundHandler.getNumEntries()):
                entry = self.nodeGroundHandler.getEntry(i)
                z = entry.getSurfacePoint(render).getZ()
                # get properties of collision node's parent (damage, elemental, etc.)
                has = entry.getIntoNode().getParent(0).hasPythonTag('notsolid')
                if has: continue
                has = entry.getIntoNode().getParent(0).hasPythonTag('slippery')
                if has:
                    tag = entry.getIntoNode().getParent(0).getPythonTag('slippery')
                    floor_slipperiness = tag
                highestZ = z
            # end for
            # ground if we've collided with a floor
            zd = highestZ - (self.node.getZ()-.3)
            if zd > 0:
                self.grounded=True          # we're on solid ground
                self.node.setZ(highestZ+.3) # set Z to floor height
                self.moveZ = 0              # stop downward momentum
                # move slower up slopes
                # this is not ideal for non-stair-like slopes
                #   to do slopes better:
                # cast ray starting from same position but
                # a little forward (using sin/cos) from origin in the dir.
                # that the player's MOVING (not facing).
                # Aim downward and check if the
                # DIFFERENCE BETWEEN the Z values of the two rays is
                # significant, and if so, reduce the speed.
                # Cap at a certain value where the slope is too high to
                # climb.
                    #
                # TODO: factor in floor_slipperiness
                    #
                speedMult = max(0.2, min(1,1-(zd*3)))
                self.moveX *= speedMult
                self.moveY *= speedMult
                #
            # end if
            
            if self.moveZ <= -3: # do not allow bouncing from great heights
                self.readyToJump = False

            # get collisions from body colliders (TODO)
            # 
                
        return task.cont
    # end def

    def keyUpdate(self,task):
        ''' update from key input states '''
        if self.state==self.STATE_NORMAL:
            
            # movement controls
            if self.control_fb == FORWARD:
                self.move_fb(self.acceleration)
            elif self.control_fb == BACK:
                self.move_fb(-self.acceleration)
            if self.control_strafe == LEFT:
                self.move_strafe(-self.acceleration)
            elif self.control_strafe == RIGHT:
                self.move_strafe(self.acceleration)
                
            # friction
##            if self.grounded:
            self.moveX = self.moveX*self.FRICTION_MULT
            self.moveY = self.moveY*self.FRICTION_MULT
##            else:
            self.moveZ = max(-self.TERMINALVELOCITY,
                             self.moveZ - self.GRAVITY*globalClock.getDt())
            
        return task.cont
    
    def moveUpdate(self,task):
        ''' update position based on X, Y, and Z inertia '''
        
        if self.state==self.STATE_NORMAL:
            # walking motion
            walk=Vec3(self.moveX, self.moveY, 0) # create vector w/ length <= 1
            if math.sqrt(self.moveX**2 + self.moveY**2) > 1:
                walk = walk.normalized() # don't move faster diagonally.
                
            # momentum -> update position
            walking = not self.walking if self.walkingToggled else self.walking
            speed = self.speed if walking else self.speed * self.RUN_SPEED_MULT
            self.node.setFluidPos(self.node, walk*speed*globalClock.getDt())
            
            if self.grounded:
                if self.readyToJump:
##                    print("jumped!")
                    self.readyToJump = False
                    self.moveZ = self.jump
            
            # vertical momentum
            self.node.setFluidZ(self.node.getZ()+self.moveZ*globalClock.getDt())
        
        return task.cont
    # end def
# end class



    #-----------#
    # functions #
    #-----------#

def play(): # start the main game
    Global.game = _Game()
    Global.player = _Player()
    Global.env = _Environment()
    Global.env.load_level()
    Global.editor = levels.LevelEditor()
    Global.game.init_lighting()
    Global.game.run()
# end def

# global data
def environment_layer(): return Global.env.layer
def env(): return Global.env
def game(): return Global.game
def editor(): return Global.editor
def renderer(): return render
def player(): return Global.player

# global data interface
def add_static_asset(gameObj): Global.env.add_static(gameObj)

# maths
def degtorad(degs): return math.pi*degs/180
def radtodeg(degs): return 180*degs/math.pi
def distance3d(x1,y1,z1,x2,y2,z2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

# panda3d interface
def addnode(obj, name):
    ''' add a node to the object obj named name '''
    obj.__dict__[name] = NodePath(name)
    obj.__dict__[name].reparentTo(obj.node)

# engine -- gameplay
def calculate_damage(strength, weaponDMG, defense):
    return max(1, round(0.0001 + (strength + weaponDMG) * (100/defense)))







    

