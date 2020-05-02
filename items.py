'''
    Dictionaries of items

    Only include nonzero values
'''

# Weapons #

''' Format: {WeaponID : {variable : value,},},
    For stats: {stat : (Lv1, Lv2, Lv3,),},
    necessary values:
        type - type of item, directly affects what happens when you use it
        model - inventory / get view: .egg or .bam directory/file
        sound - when used: directory/file
        frames - default number of frames the animation runs for at 60fps
            (directly determines attack / cast speed)
        life - durability
    possible values:
        mass - mass of the item in KG (0 by default)
        model_action - when used: .egg or .bam directory/file
        model_projectile - model of the projectile directory/file
        speed - speed of projectile on spells / missile weapons
        duration - how long the spell lasts in frames at 60fps
        shots - number of projectiles (1 by default)
        spread - shotgun-like spread of projectiles
        deviation - accuracy of projectiles (0 is perfect accuracy)
        pierces - no. enemies it can hit before disappearing (1 by default)
        hitbox - HitBox object, for melee attacks
        reach - how far the weapon can reach in centimeters
        slash - slash damage
        stab
        crush
        fire - fire elemental magic power (not fire damage on weapon)
        elec
        water
        armor - damage reduction (linear) (for physical damage types)
        res_slash - resistances
        res_stab
        res_crush
        res_fire
        res_elec
        res_water
'''
    

# WEAPONS[wp_id].get('fire', 0)

hitbox_sword1 = HitBox(3) # args: number of keyframes
hitbox_sword1.frame1 = CollisionBox(Point3(0.5,0.5,0),0.4,1.0,0.2)

ARMOR={
    # sound is sound played when you hit the armor
    AR_GAMBESON:{
        'type': 'armor_torso',
        'model': "Models/ar_gambeson",
        'sound': "Sounds/hit_cloth.ogg",
        'life': 1200,
        'armor': 2,
        'res_slash': 40,
        'res_stab': 25,
        'res_crush': 40,
        'mass': 4.0,
        'value': 120,
        },
    AR_LEATHERARMOR:{
        'type': 'armor_torso',
        'model': "Models/ar_leatherarmor",
        'sound': "Sounds/hit_leather.ogg",
        'life': 600,
        'armor': 4,
        'res_slash': 33,
        'res_stab': 33,
        'res_crush': 25,
        'mass': 12.0,
        'value': 320,
        },
    AR_IRONARMOR:{
        'type': 'armor_torso',
        'model': "Models/ar_ironarmor",
        'sound': "Sounds/hit_metal.ogg",
        'life': 3600,
        'armor': 5,
        'res_slash': 75,
        'res_stab': 50,
        'res_crush': 20,
        'mass': 15.0,
        'value': 820,
        },
    }

WEAPONS={
    # swing sounds: 1 - 4: highest pitch -> lowest pitch
    WP_HAMMER:{
        'type': 'weapon_onehand',
        'model': "Models/wp_hammer_view",
        'model_action': "Models/wp_hammer",
        'sound': "Sounds/swing4.ogg",
        'hitbox': hitbox_hammer1,
        'reach': 30,
        'life': 320,
        'frames': (90, 75, 60,),
        'slash': (1, 2, 4,),
        'stab': (0, 0, 0,),
        'crush': (36, 48, 60,),
        'mass': 0.9,
        'value': 10,
        },
    WP_AXE:{
        'type': 'weapon_onehand',
        'model': "Models/wp_axe_view",
        'model_action': "Models/wp_axe",
        'sound': "Sounds/swing3.ogg",
        'hitbox': hitbox_axe1,
        'reach': 40,
        'life': 200,
        'frames': (90, 75, 60,),
        'slash': (5, 10, 20,),
        'stab': (1, 2, 4,),
        'crush': (36, 48, 60,),
        'mass': 1.0,
        'value': 20,
        },
    WP_WARHAMMER:{
        'type': 'weapon_onehand',
        'model': "Models/wp_warhammer_view",
        'model_action': "Models/wp_warhammer",
        'sound': "Sounds/swing4.ogg",
        'hitbox': hitbox_hammer2,
        'reach': 50,
        'life': 960,
        'frames': (90, 75, 60,),
        'slash': (2, 4, 7,),
        'stab': (5, 8, 12,),
        'crush': (45, 60, 75,),
        'mass': 1.2,
        'value': 60,
        },
    WP_IRONSWORD:{
        'type': 'weapon_onehand',
        'model': "Models/wp_ironsword_view",
        'model_action': "Models/wp_ironsword",
        'sound': "Sounds/swing2.ogg",
        'hitbox': hitbox_sword1,
        'reach': 80,
        'life': 80,
        'frames': (60, 50, 40,),
        'slash': (20, 30, 40,),
        'stab': (10, 20, 30,),
        'crush': (5, 10, 15,),
        'mass': 1.0,
        'value': 80,
        },
    WP_LONGSWORD:{
        'type': 'weapon_twohands',
        'model': "Models/wp_longsword_view",
        'model_action': "Models/wp_longsword",
        'sound': "Sounds/swing2.ogg",
        'hitbox': hitbox_sword2,
        'reach': 110,
        'life': 200,
        'frames': (60, 50, 40,),
        'slash': (30, 45, 60,),
        'stab': (20, 30, 45,),
        'crush': (6, 12, 18,),
        'mass': 1.6,
        'value': 300,
        },
    WP_ESTOC:{
        'type': 'weapon_twohands',
        'model': "Models/wp_estoc_view",
        'model_action': "Models/wp_estoc",
        'sound': "Sounds/swing1.ogg",
        'hitbox': hitbox_estoc,
        'reach': 125,
        'life': 120,
        'frames': (50, 40, 30,),
        'slash': (10, 20, 30,),
        'stab': (25, 35, 50,),
        'crush': (6, 12, 18,),
        'mass': 1.65,
        'value': 1440,
        },
    }

SPELLS={
    SP_FLAMES:{ # a la DS1 combustion
        'type': 'spell_melee',
        'model': "Models/sp_flames_view"
        'model_action': "Models/fp_castspell1",
        'effect': "Effects/sp_flames.eff",
        'sound': "Sounds/spell_fire1.ogg",
        'hitbox': hitbox_flames,
        'frames': (45, 35, 25,),
        'mana': (5, 6, 7,),
        'stamina': (40, 35, 30,),
        'fire': (30, 45, 60,),
        'value': 450,
        },
    SP_HEATWAVE:{ # a la KF4:TAC "fireball" - slow-moving large wave of fire
        'type': 'spell_ranged',
        'model': "Models/sp_flames_view"
        'model_action': "Models/fp_castspell2",
        'effect': "Effects/sp_heatwave.eff",
        'sound': "Sounds/spell_fire2.ogg",
        'frames': (60, 50, 40,),
        'duration': (180, 180, 180,),
        'mana': (5, 6, 7,),
        'stamina': (40, 35, 30,),
        'speed': (40, 60, 80,),
        'pierces': (3, 4, 5,),
        'fire': (20, 25, 30,),
        'element': ELEM_FIRE,
        'value': 800,
        },
    }

















