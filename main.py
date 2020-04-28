'''
    
'''

from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
import sys
import math

# constants
V_FORWARD   = Vec3(0,1,0)
V_BACK      = Vec3(0,-1,0)
V_LEFT      = Vec3(-1,0,0)
V_RIGHT     = Vec3(1,0,0)
V_ZERO      = Vec3(0)

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        base.disableMouse()
        base.accept( "escape" , sys.exit)   # controls to close the game

        # window properties
        properties = WindowProperties()
        properties.setSize(1024, 768)
        self.win.requestProperties(properties)

        # load assets
        self.environment = self.loader.loadModel("Models/Sample/Environment/environment")
        self.environment.reparentTo(self.render)
        
        # init
        self.initCollision()
##        self.loadLevel()
        self.initPlayer()
        OnscreenText(text="Simple FPS Movement", style=1, fg=(1,1,1,1),
                    pos=(1.3,-0.95), align=TextNode.ARight, scale = .07)
        OnscreenText(text=__doc__, style=1, fg=(1,1,1,1),
            pos=(-1.3, 0.95), align=TextNode.ALeft, scale = .05)
        
    def initCollision(self):
        """ create the collision system """
        base.cTrav = CollisionTraverser()
        base.pusher = CollisionHandlerPusher()
        
##    def loadLevel(self):
##        """ load the self.level 
##            must have
##            <Group> *something* { 
##              <Collide> { Polyset keep descend } 
##            in the egg file
##        """
##        self.level = loader.loadModel('level.egg')
##        self.level.reparentTo(render)
##        self.level.setTwoSided(True)
                
    def initPlayer(self):
        """ loads the player and creates all the controls for him"""
        self.node = Player()

class Body(object):
    def __init__(self, parent):
        self.node = NodePath('body')
        self.node.reparentTo(parent)
        
class Player(object):
    """
        Player is the main actor in the fps game
    """
    # states
    STATE_NORMAL = 0
    
    SPEED_MULT = 200 # multiplier
    ACCELERATION = 0.1 # having different acceleration forward/back resulted in a weird glitch.
    FRICTION_MULT = 0.9
    
    def __init__(self):
        """ inits the player """
        self.init_states()
        self.init_control()
        self.init_model()
        self.init_camera()
        self.init_collisions()
        self.init_controls()
        # init mouse update task
        taskMgr.add(self.mouseUpdate, 'mouse-task')
        taskMgr.add(self.moveUpdate, 'move-task')
        taskMgr.add(self.keyUpdate, 'input-task')
    # end def

    def init_states(self):
        self.state = self.STATE_NORMAL
        self.readyToJump = False
    
    def init_control(self):
        # controls: player input
        self.control_fb = V_ZERO        # player input for walking forward/back
        self.control_strafe = V_ZERO    # strafing left/right
        self.moveZ = 0      # vertical (up/down movement)
        self.moveY = 0      # forward/back movement
        self.moveX = 0      # strafe movement
    # end def
        
    def init_model(self):
        """ make the nodepath for player """
        self.node = NodePath('player')
        self.node.reparentTo(render)
        self.node.setPos(0,0,2)
        self.node.setScale(.05)
        self.body = Body(self.node)
    # end def
    
    def init_camera(self):
        """ puts camera at the players node """
        pl =  base.cam.node().getLens()
        pl.setFov(70)
        base.cam.node().setLens(pl)
        base.camera.reparentTo(self.body.node)
    # end def
        
    def init_collisions(self):
        """ create a collision solid and ray for the player """
        cn = CollisionNode('player')
        cn.addSolid(CollisionSphere(0,0,0,3))
        solid = self.node.attachNewNode(cn)
        base.cTrav.addCollider(solid,base.pusher)
        base.pusher.addCollider(solid,self.node, base.drive.node())
        # init players floor collisions
        ray = CollisionRay()
        ray.setOrigin(0,0,-.2)
        ray.setDirection(0,0,-1)
        cn = CollisionNode('playerRay')
        cn.addSolid(ray)
        cn.setFromCollideMask(BitMask32.bit(0))
        cn.setIntoCollideMask(BitMask32.allOff())
        solid = self.node.attachNewNode(cn)
        self.nodeGroundHandler = CollisionHandlerQueue()
        base.cTrav.addCollider(solid, self.nodeGroundHandler)
    # end def
        
    def init_controls(self):
        """ attach key events """
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
    # end def
    
    def jump_ready(self):
        self.readyToJump = True
    def jump_unready(self):
        self.readyToJump = False
    def walk_forward(self):
        if self.control_fb != V_BACK: self.control_fb = V_FORWARD
    def walk_forward_stop(self):
        if self.control_fb == V_FORWARD: self.control_fb = V_ZERO
    def walk_back(self):
        self.control_fb = V_BACK # priority over forward
    def walk_back_stop(self):
        if self.control_fb == V_BACK: self.control_fb = V_ZERO
    def walk_left(self):
        if self.control_strafe != V_RIGHT: self.control_strafe = V_LEFT
    def walk_left_stop(self):
        if self.control_strafe == V_LEFT: self.control_strafe = V_ZERO
    def walk_right(self):
        self.control_strafe = V_RIGHT # priority over left
    def walk_right_stop(self):
        if self.control_strafe == V_RIGHT: self.control_strafe = V_ZERO
        
    def move_set(self, xs,ys):
        self.moveX = max(-1, min(1, xs)) # normalize
        self.moveY = max(-1, min(1, ys))
    def move_fb(self, value):
        spin = math.pi*self.body.node.getH()/180
        xr = -value*math.sin(spin)
        yr = value*math.cos(spin)
        self.move_set(self.moveX + xr, self.moveY + yr)
    def move_strafe(self, value):
        spin = math.pi*(self.body.node.getH()-90)/180
        xr = -value*math.sin(spin)
        yr = value*math.cos(spin)
        self.move_set(self.moveX + xr, self.moveY + yr)
        
    def mouseUpdate(self,task):
        md = base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if base.win.movePointer(0, base.win.getXSize()//2, base.win.getYSize()//2):
            self.body.node.setH(self.body.node.getH() - (x - base.win.getXSize()//2)*0.1)
            self.body.node.setP(self.body.node.getP() - (y - base.win.getYSize()//2)*0.1)
        return task.cont
    # end def

    def keyUpdate(self,task):
        ''' update from key input states '''
        # movement controls
        
        if self.control_fb == V_FORWARD:
            self.move_fb(self.ACCELERATION)
        elif self.control_fb == V_BACK:
            self.move_fb(-self.ACCELERATION)
        if self.control_strafe == V_LEFT:
            self.move_strafe(-self.ACCELERATION)
        elif self.control_strafe == V_RIGHT:
            self.move_strafe(self.ACCELERATION)
        # friction
        self.moveX = self.moveX*self.FRICTION_MULT
        self.moveY = self.moveY*self.FRICTION_MULT
        return task.cont
    
    def moveUpdate(self,task):
        ''' momentum -> update position '''
        
        # walking motion
        move=Vec3(self.moveX,self.moveY,0)
        self.node.setPos(self.node,move*globalClock.getDt()*self.SPEED_MULT)
        
        # get the highest Z from the down casting ray
##        highestZ = -100
##        for i in range(self.nodeGroundHandler.getNumEntries()):
##            entry = self.nodeGroundHandler.getEntry(i)
##            z = entry.getSurfacePoint(render).getZ()
##            if z > highestZ and entry.getIntoNode().getName() == "Cube":
##                highestZ = z
##        # gravity effects and jumps
##        self.node.setZ(self.node.getZ()+self.moveZ*globalClock.getDt())
##        self.moveZ -= 1*globalClock.getDt()
##        if highestZ > self.node.getZ()-.3:
##            self.moveZ = 0
##            self.node.setZ(highestZ+.3)
##            if self.readyToJump:
##                self.moveZ = 1
        return task.cont
    # end def
     
game = Game()
game.run()
