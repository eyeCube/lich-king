'''

'''


from panda3d.core import *

    # meta #

class Symbol:
    nextID=1
    def __init__(self):
        self.ID=Symbol.nextID
        Symbol.nextID += 1
    def __eq__(self, other):
        return self.ID==other.ID
# end class

    #-----------#
    # constants #
    #-----------#

FPSHI = 60
FPSLO = 30

# vectors
V_FORWARD   = Vec3(0,1,0)
V_BACK      = Vec3(0,-1,0)
V_LEFT      = Vec3(-1,0,0)
V_RIGHT     = Vec3(1,0,0)
V_ZERO      = Vec3(0)

# controls
FORWARD   = Symbol()
BACK      = Symbol()
LEFT      = Symbol()
RIGHT     = Symbol()
STOP      = Symbol()

# elements
ELEM_FIRE = Symbol()
ELEM_WATER = Symbol()
ELEM_ELEC = Symbol()

    #-------#
    # items #
    #-------#

# armor - torso
AR_GAMBESON = Symbol()

# weapons
WP_IRONSWORD = Symbol()
WP_STEELSWORD = Symbol()

# spells
SP_FLAMES = Symbol()
SP_HEATWAVE = Symbol()
















