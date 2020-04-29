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

# controls
FORWARD   = Symbol()
BACK      = Symbol()
LEFT      = Symbol()
RIGHT     = Symbol()
STOP      = Symbol()

# vectors
V_FORWARD   = Vec3(0,1,0)
V_BACK      = Vec3(0,-1,0)
V_LEFT      = Vec3(-1,0,0)
V_RIGHT     = Vec3(1,0,0)
V_ZERO      = Vec3(0)
