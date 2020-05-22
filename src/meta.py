'''
    meta-data for all (or most) modules
    contains constants and global protected variables
'''


from panda3d.core import *

    # meta #

class Meta:
    ''' should not be accessed outside of functions below '''
    _nextID = 1
# end class

# meta-functions #

def symbol():
    _next = Meta._nextID
    Meta._nextID += 1
    return _next
#

    #-----------#
#---# constants #--------------------------------------------------------#
    #-----------#

# program
FPSHI = 60
FPSLO = 30

# game
GLOBAL_GRAVITY = 5
GLOBAL_GRAVITY_WATER = 0.5

# vectors
V_FORWARD   = Vec3(0,1,0)
V_BACK      = Vec3(0,-1,0)
V_LEFT      = Vec3(-1,0,0)
V_RIGHT     = Vec3(1,0,0)
V_ZERO      = Vec3(0)

# controls
FORWARD   = symbol()
BACK      = symbol()
LEFT      = symbol()
RIGHT     = symbol()
STOP      = symbol()

# elements
ELEM_FIRE = symbol()
ELEM_WATER = symbol()
ELEM_ELEC = symbol()

# zones
# OUTSIDE : outside the large outer walls of the main castle
# INSIDE : inside the large outer walls of the main castle
# CASTLE : inside the inner walls of the main castle

# OUTSIDE
# courtyard
    # starting area
    # shrine interior
ZONE_OUTSIDE_COURTYARD = symbol()
ZONE_OUTSIDE_COURTYARD_SHRINE_B1 = symbol() # interior of ancient shrine
ZONE_OUTSIDE_COURTYARD_SHRINE_B2 = symbol() # interior of ancient shrine
ZONE_OUTSIDE_COURTYARD_SHRINE_B3 = symbol() # interior of ancient shrine
# city North
    # cantons (in order from left-right and bottom-top with bottom facing courtyard):
        # courtyard connection
        # unnamed small canton (with nothing on it as of 5-20-2020)
        # church
        # market
        # foreign
        # barracks
        # arena
        # residential
    # ground
    # sewer
ZONE_OUTSIDE_UPTOWN = symbol() # "ville" or cantons (on any canton except residential and foreign)
ZONE_OUTSIDE_UPTOWN_INTERIOR_CHURCH = symbol() # canton interior
ZONE_OUTSIDE_UPTOWN_INTERIOR_MARKET = symbol() # canton interior
ZONE_OUTSIDE_UPTOWN_RESIDENTIAL = symbol() # on the residential canton
ZONE_OUTSIDE_UPTOWN_INTERIOR_RESIDENTIAL = symbol() # canton interior
ZONE_OUTSIDE_UPTOWN_INTERIOR_BARRACKS = symbol() # canton interior
ZONE_OUTSIDE_UPTOWN_INTERIOR_ARENA = symbol() # canton interior
ZONE_OUTSIDE_UPTOWN_FOREIGN = symbol() # on the foreign canton
ZONE_OUTSIDE_UPTOWN_INTERIOR_FOREIGN = symbol() # canton interior
ZONE_OUTSIDE_UPTOWN_GROUND = symbol() # cantons ground level
ZONE_OUTSIDE_UPTOWN_SEWER = symbol() # cantons underground
# forest (a low wall divides the city and the sewer river from the forest)
    # riverside (outside the forest wall)
    # field (field of cut-down trees separating the wall from the forest)
    # shallow forest (by the field)
    # deep forest -- procedurally generated infinite terrain?
    # foothills? Of giant mountain to the North?
ZONE_OUTSIDE_FOREST_RIVER = symbol() # outside the forest wall
# city South (downtown)
    # Northside
    # Westside
    # Eastside
    # Southside
    # sewer (underground)
ZONE_OUTSIDE_DOWNTOWN_NORTH = symbol()
# cliffs
# INSIDE
    # shrine
    # field
    # inner town
    # courtyard
# CASTLE
    # 

    #-------#
#---# items #------------------------------------------------------------#
    #-------#

# armor - torso
AR_GAMBESON = symbol()

# weapons
WP_IRONSWORD = symbol()
WP_STEELSWORD = symbol()

# spells
SP_FLAMES = symbol()
SP_HEATWAVE = symbol()

    #---------#
#---# assets  #----------------------------------------------------------#
    #---------#

# game objects
ASSET_TRIGGER_LOAD = symbol()

# static

# geometry
ASSET_PLANE_SOLID = symbol()

# models
ASSET_CORRIDOR_ARCHED_1_CORNER = symbol()
ASSET_CORRIDOR_ARCHED_1 = symbol()
ASSET_CORRIDOR_STAIRS_1 = symbol()

# decor
ASSET_DECOR_FERN_1 = symbol()

# scenes (environment models)
    # scenes may have LAYERS* -- essentially the scene is split into
    # several different models / different objects, which can then
    # cast shadows over other objects in the scene, etc.
    # So the models are numbered starting at 1 for the base layer
    # which should be the floor geometry at the lowest Z level.
    # Each proceeding layer should be higher in elevation.

    # * THIS SHOULD BE DONE LASTLY, WHEN ALL SCENES ARE FINALIZED.
    
ASSET_SCENE_TEST_1 = symbol()
ASSET_SCENE_COURTYARD_1 = symbol()
















