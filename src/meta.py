'''
    meta-data for all (or most) modules
    contains constants and global protected variables
'''


from panda3d.core import *

    # meta #

class Meta:
    ''' should not be accessed outside of functions below '''
    _nextID = 0
    _symbols_names = {}
    _symbols_ids = {}
# end class

# meta-functions #

def symbol(name:str) -> int:
    Meta._nextID += 1
    _id = Meta._nextID
    Meta._symbols_names.update({name : _id})
    Meta._symbols_ids.update({_id : name})
    return _id
def get_symbol_name_by_id(_id:int) -> str:
    return Meta._symbols_ids.get(_id, "NOT_A_SYMBOL")
def get_symbol_id_by_name(name:str) -> int: # this should never be needed
    return Meta._symbols_names.get(name, -1)
#

    #-----------#
#---# constants #--------------------------------------------------------#
    #-----------#

# program
FPSHI = 60
FPSLO = 30

# game
GLOBAL_GRAVITY = 5
GLOBAL_GRAVITY_WATER = 1
    # skill levels -- experience required
LEVEL_2 = 50
LEVEL_3 = 150
LEVEL_4 = 300

# vectors
V_FORWARD   = Vec3(0,1,0)
V_BACK      = Vec3(0,-1,0)
V_LEFT      = Vec3(-1,0,0)
V_RIGHT     = Vec3(1,0,0)
V_ZERO      = Vec3(0)

# controls
FORWARD   = symbol('FORWARD')
BACK      = symbol('BACK')
LEFT      = symbol('LEFT')
RIGHT     = symbol('RIGHT')
STOP      = symbol('STOP')

# elements
ELEM_FIRE = symbol('ELEM_FIRE')
ELEM_WATER = symbol('ELEM_WATER')
ELEM_ELEC = symbol('ELEM_ELEC')

# zones
# OUTSIDE : outside the large outer walls of the main castle
# INSIDE : inside the large outer walls of the main castle
# CASTLE : inside the inner walls of the main castle

# OUTSIDE
# courtyard
    # starting area
    # shrine interior
ZONE_OUTSIDE_COURTYARD = symbol('ZONE_OUTSIDE_COURTYARD')
ZONE_OUTSIDE_COURTYARD_SHRINE_B1 = symbol('ZONE_OUTSIDE_COURTYARD_SHRINE_B1') # interior of ancient shrine
ZONE_OUTSIDE_COURTYARD_SHRINE_B2 = symbol('ZONE_OUTSIDE_COURTYARD_SHRINE_B2') # interior of ancient shrine
ZONE_OUTSIDE_COURTYARD_SHRINE_B3 = symbol('ZONE_OUTSIDE_COURTYARD_SHRINE_B3') # interior of ancient shrine
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
ZONE_OUTSIDE_UPTOWN = symbol('ZONE_OUTSIDE_UPTOWN') # "ville" or cantons (on any canton except residential and foreign)
ZONE_OUTSIDE_UPTOWN_INTERIOR_CHURCH = symbol('ZONE_OUTSIDE_UPTOWN_INTERIOR_CHURCH') # canton interior
ZONE_OUTSIDE_UPTOWN_INTERIOR_MARKET = symbol('ZONE_OUTSIDE_UPTOWN_INTERIOR_MARKET') # canton interior
ZONE_OUTSIDE_UPTOWN_RESIDENTIAL = symbol('ZONE_OUTSIDE_UPTOWN_RESIDENTIAL') # on the residential canton
ZONE_OUTSIDE_UPTOWN_INTERIOR_RESIDENTIAL = symbol('ZONE_OUTSIDE_UPTOWN_INTERIOR_RESIDENTIAL') # canton interior
ZONE_OUTSIDE_UPTOWN_INTERIOR_BARRACKS = symbol('ZONE_OUTSIDE_UPTOWN_INTERIOR_BARRACKS') # canton interior
ZONE_OUTSIDE_UPTOWN_INTERIOR_ARENA = symbol('ZONE_OUTSIDE_UPTOWN_INTERIOR_ARENA') # canton interior
ZONE_OUTSIDE_UPTOWN_FOREIGN = symbol('ZONE_OUTSIDE_UPTOWN_FOREIGN') # on the foreign canton
ZONE_OUTSIDE_UPTOWN_INTERIOR_FOREIGN = symbol('ZONE_OUTSIDE_UPTOWN_INTERIOR_FOREIGN') # canton interior
ZONE_OUTSIDE_UPTOWN_GROUND = symbol('ZONE_OUTSIDE_UPTOWN_GROUND') # cantons ground level
ZONE_OUTSIDE_UPTOWN_SEWER = symbol('ZONE_OUTSIDE_UPTOWN_SEWER') # cantons underground
# forest (a low wall divides the city and the sewer river from the forest)
    # riverside (outside the forest wall)
    # field (field of cut-down trees separating the wall from the forest)
    # shallow forest (by the field)
    # deep forest -- procedurally generated infinite terrain?
    # foothills? Of giant mountain to the North?
ZONE_OUTSIDE_FOREST_RIVER = symbol('ZONE_OUTSIDE_FOREST_RIVER') # outside the forest wall
# city South (downtown)
    # Northside
    # Westside
    # Eastside
    # Southside
    # sewer (underground)
ZONE_OUTSIDE_DOWNTOWN_NORTH = symbol('ZONE_OUTSIDE_DOWNTOWN_NORTH')
# cliffs
# INSIDE
    # shrine
    # field
    # inner town
    # courtyard
# CASTLE
    # 

    #-------#
#---# skill #------------------------------------------------------------#
    #-------#

SKILL_SHORTSWORDS = symbol('SKILL_SHORTSWORDS')
SKILL_LONGSWORDS = symbol('SKILL_LONGSWORDS')
SKILL_GREATSWORDS = symbol('SKILL_GREATSWORDS')
SKILL_RAPIERS = symbol('SKILL_RAPIERS')
SKILL_DAGGERS = symbol('SKILL_DAGGERS')
SKILL_KNIVES = symbol('SKILL_KNIVES')
SKILL_HAMMERS = symbol('SKILL_HAMMERS')
SKILL_MALLETS = symbol('SKILL_MALLETS')
SKILL_AXES = symbol('SKILL_AXES')
SKILL_LARGEAXES = symbol('SKILL_LARGEAXES')
SKILL_WARHAMMERS = symbol('SKILL_WARHAMMERS')
SKILL_WARAXES = symbol('SKILL_WARAXES')
SKILL_GREATAXES = symbol('SKILL_GREATAXES')
SKILL_HALBERDS = symbol('SKILL_HALBERDS')
SKILL_POLEAXES = symbol('SKILL_POLEAXES')
SKILL_POLEHAMMERS = symbol('SKILL_POLEHAMMERS')
SKILL_STAVES = symbol('SKILL_STAVES')
SKILL_SPEARS = symbol('SKILL_SPEARS')
SKILL_CLUBS = symbol('SKILL_CLUBS')
SKILL_MACES = symbol('SKILL_MACES')
SKILL_GREATCLUBS = symbol('SKILL_GREATCLUBS')
SKILL_GREATMACES = symbol('SKILL_GREATMACES')
SKILL_BUCKLERS = symbol('SKILL_BUCKLERS')
SKILL_SMALLSHIELDS = symbol('SKILL_SMALLSHIELDS')
SKILL_LARGESHIELDS = symbol('SKILL_LARGESHIELDS')
SKILL_TOWERSHIELDS = symbol('SKILL_TOWERSHIELDS')
SKILL_BOMBS = symbol('SKILL_BOMBS')
SKILL_BOWS = symbol('SKILL_BOWS')
SKILL_CROSSBOWS = symbol('SKILL_CROSSBOWS')
SKILL_GUNS = symbol('SKILL_GUNS')
SKILL_THROWINGKNIVES = symbol('SKILL_THROWINGKNIVES')
SKILL_SLINGS = symbol('SKILL_SLINGS')
SKILL_SLINGSHOTS = symbol('SKILL_SLINGSHOTS')

SKILLS={
# SKILL_ const : (name, xp_modf,),
SKILL_SHORTSWORDS : ('short swords', 1,),
SKILL_LONGSWORDS : ('longswords', 1,),
SKILL_GREATSWORDS : ('greatswords', 1,),
SKILL_RAPIERS : ('rapiers', 1,),
SKILL_DAGGERS : ('daggers', 1,),
SKILL_KNIVES : ('knives', 1,),
SKILL_HAMMERS : ('hammers', 1,),
SKILL_MALLETS : ('mallets', 1,),
SKILL_AXES : ('hatchets', 1,),
SKILL_LARGEAXES : ('chop axes', 1,),
SKILL_WARHAMMERS : ('warhammers', 1,),
SKILL_WARAXES : ('war axes', 1,),
SKILL_GREATAXES : ('greataxes', 1,),
SKILL_HALBERDS : ('hallebardes', 1,),
SKILL_POLEAXES : ('pollaxes', 1,),
SKILL_POLEHAMMERS : ('pollhammers', 1,),
SKILL_STAVES : ('staves', 1,),
SKILL_SPEARS : ('spears', 1,),
SKILL_CLUBS : ('clubs', 1,),
SKILL_MACES : ('maces', 1,),
SKILL_GREATCLUBS : ('great clubs', 1,),
SKILL_GREATMACES : ('great maces', 1,),
SKILL_BUCKLERS : ('bucklers', 1,),
SKILL_SMALLSHIELDS : ('small shields', 1,),
SKILL_LARGESHIELDS : ('large shields', 1,),
SKILL_TOWERSHIELDS : ('tower shields', 1,),
SKILL_BOMBS : ('bombs', 1,),
SKILL_BOWS : ('bows', 1,),
SKILL_CROSSBOWS : ('crossbows', 1,),
SKILL_GUNS : ('guns', 1,), # primitive hand-cannons
SKILL_THROWINGKNIVES : ('throwing knives', 1,),
SKILL_SLINGS : ('slings', 1,),
SKILL_SLINGSHOTS : ('slingshots', 1,),
    }


    #-------#
#---# items #------------------------------------------------------------#
    #-------#

# armor - torso
AR_GAMBESON = symbol('AR_GAMBESON')

# weapons
WP_IRONSWORD = symbol('WP_IRONSWORD')
WP_STEELSWORD = symbol('WP_STEELSWORD')

# spells
SP_FLAMES = symbol('SP_FLAMES')
SP_HEATWAVE = symbol('SP_HEATWAVE')

    #---------#
#---# assets  #----------------------------------------------------------#
    #---------#

# game objects
ASSET_TRIGGER_LOAD = symbol('ASSET_TRIGGER_LOAD')

# static

# geometry
ASSET_PLANE_SOLID = symbol('ASSET_PLANE_SOLID')

# models
ASSET_CORRIDOR_ARCHED_1_CORNER = symbol('ASSET_CORRIDOR_ARCHED_1_CORNER')
ASSET_CORRIDOR_ARCHED_1 = symbol('ASSET_CORRIDOR_ARCHED_1')
ASSET_CORRIDOR_STAIRS_1 = symbol('ASSET_CORRIDOR_STAIRS_1')

# decor
ASSET_DECOR_FERN_1 = symbol('ASSET_DECOR_FERN_1')

# scenes (environment models)
    # scenes may have LAYERS* -- essentially the scene is split into
    # several different models / different objects, which can then
    # cast shadows over other objects in the scene, etc.
    # So the models are numbered starting at 1 for the base layer
    # which should be the floor geometry at the lowest Z level.
    # Each proceeding layer should be higher in elevation.

    # * THIS SHOULD BE DONE LASTLY, WHEN ALL SCENES ARE FINALIZED.
    
ASSET_SCENE_TEST_1 = symbol('ASSET_SCENE_TEST_1')
ASSET_SCENE_COURTYARD_1 = symbol('ASSET_SCENE_COURTYARD_1')
















