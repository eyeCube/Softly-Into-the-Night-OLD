'''
    const.py
    
'''


from enum import Flag, auto

import tcod as libtcod





#
# Init Global Constants #
#



GAME_TITLE = "Softly Into the Night"

ROOMW       = 100           #max level size, width and height
ROOMH       = 75
MAXLEVEL    = 20            #deepest dungeon level
TILES_PER_ROW = 16          # Num tiles per row (size of the char sheet 
TILES_PER_COL = 16          # " per column         used for ASCII display)




#
# Gameplay Constants
#

SPRINT_SPEEDMOD     = 100   # move speed bonus when you sprint
SLOW_SPEEDMOD       = -33   # speed penalty while slowed
HASTE_SPEEDMOD      = 50    # speed bonus when hasty

#items
RATIONFOOD          = 100

SATIETY_PER_RATION  = 100   # how much hunger is healed per ration of food
WATER_HYDRATION     = 25    # how much hydration is healed per unit of water

#skills
SKILLMAX            = 2     # highest skill level you can attain

#stats
AVG_HEARING         = 100
AVG_SPD             = 100

#combat
COMBATROLL          = 20    # die roll

#action potential cost to perform actions
NRG_MOVE            = 1     # multiplier 
NRG_ATTACK          = 200 
NRG_BOMB            = 150 
NRG_PICKUP          = 50    # grab thing and wield it (requires empty hand)
NRG_POCKET          = 200   # picking up and putting in your inventory
NRG_OPENCONTAINER   = 50    # Should it cost energy just to look in a container?
NRG_OPEN            = 50    # Cost to open/close a door
NRG_RUMMAGE         = 100   # Cost of picking an item from a container
NRG_EXAMINE         = 200
NRG_QUAFF           = 100
NRG_EAT             = 200   # AP cost per (unit of consumption) to eat
NRGSAVED_FASTSHOT   = 50

#fluids
MAX_FLUID_IN_TILE   = 100

#status effects
# bio (sick)
BIO_METERLOSS   = 2     # sickness points lost per turn
BIO_HURT        = 1     # damage per turn while sick

# chem (exposure)
CHEM_METERLOSS  = 5     # exposure points lost per turn
CHEM_HURT       = 5     # damage chem effect causes when exposure meter fills

# temp (fire)
FIRE_METERLOSS  = 10    # temperature points lost per turn
FIRE_METERMAX   = 1000   #maximum temperature a thing can reach
FIRE_TEMP       = 100   #avg. temperature at which a thing will set fire
FIRE_BURN       = 50    #dmg fire deals to things (in fire damage) per turn
FIRE_HURT       = 1     #lo dmg dealt per turn to things w/ burning status effect
FIRE_LIGHT      = 10    #how much light is produced by fire?
#FIRE_LEVELMAX     = 3     #max fire level; 0 is no fire, max is blazing flame

# paralysis
ROLL_SAVE_PARAL = 10    #affects chance to undo paralysis

#direction
DIRECTIONS={
    (-1,-1) : 'northwest',
    (1,-1)  : 'northeast',
    (0,-1)  : 'north',
    (-1,0)  : 'west',
    (0,0)   : 'self',
    (1,0)   : 'east',
    (-1,1)  : 'southwest',
    (0,1)   : 'south',
    (1,1)   : 'southeast',
}
DIRECTIONS_TERSE={
    (-1,-1) : 'NW',
    (1,-1)  : 'NE',
    (0,-1)  : 'N',
    (-1,0)  : 'W',
    (0,0)   : 'self',
    (1,0)   : 'E',
    (-1,1)  : 'SW',
    (0,1)   : 'S',
    (1,1)   : 'SE',
}
DIRECTION_FROM_INT={
    0   : (1,0,),
    1   : (1,-1,),
    2   : (0,-1,),
    3   : (-1,-1,),
    4   : (-1,0,),
    5   : (-1,1,),
    6   : (0,1,),
    7   : (1,1,),
    }




#
# Keys
#

    # special character key inputs
K_ESCAPE    = 19
K_UP        = 24
K_DOWN      = 25
K_RIGHT     = 26
K_LEFT      = 27
K_ENTER     = 28
K_PAGEUP    = 30
K_PAGEDOWN  = 31
K_HOME      = 127
K_END       = 144
K_BACKSPACE = 174
K_DELETE    = 175
K_INSERT    = 254







#
# Tiles
#

FLOOR           =   249     # centered dot
WALL            = ord('#')
DOORCLOSED      = ord('+')
DOOROPEN        = ord('-')
STAIRUP         = ord('<')
STAIRDOWN       = ord('>')
FUNGUS          = ord('\"')
TREE            =   5       # club
SHROOM          =   6       # spade
PUDDLE          =   7       # circle
SHALLOW         = ord('_')
WATER           = ord('~')
DEEPWATER       =   247     # double ~

#
# Thing types
#

T_TRAP          = ord('!')
T_TREE          =   5       # club
T_SHROOM        =   6       # spade
T_FUNGUS        = ord('\"')
T_FOUNTAIN      =   144     # faucet-looking thing
T_MONEY         = ord('$')
T_BOTTLE        =   173     # upside down '!'
T_PHONE         =   168     # upside down '?' - basically a "magic scroll"
T_CORPSE        = ord('%')
T_FOOD          = ord('&')
T_BULLET        = ord('.')
T_BOULDER       = ord('0')
T_DUST          = ord('^')
T_POLE          = ord('|')
T_TERMINAL      =   167     # o underlined
T_MELEEWEAPON   = ord('/')
T_THROWWEAPON   = ord('\\')
T_HEAVYWEAPON   = ord('=')
T_GUN           =   169     # pistol-looking char
T_ENERGYWEAPON  =   170     # backward pistol-looking char
T_BOMB          = ord('*')
#T_LAUNCHER      =   151     # sqrt
T_SHIELD        = ord(')')
T_CLOAK         = ord('(')
T_ARMOR         = ord(']')
T_HELMET        = ord('[')
T_FLUID         = ord('~')
T_GAS           = ord(' ')
T_SCRAPMETAL    =   171     # 1/2
T_SCRAPELEC     =   172     # 1/4
#T_CREDIT        =   172     # 1/4
T_WOOD          =   246     # div
T_BOX           =   22      # horizontal rectangle
T_LOG           =   28      # upside down gun-looking char
T_CHEST         =   127     # house looking thing
T_VORTEX        =   21 
T_GRAVE         =   241     # +/-

'''
unused chars:
({}';|_?!*
'''

# special chars #

# border 0
# single-line on all sides
CH_VW       = [179, 179, 186] # vertical wall
CH_HW       = [196, 205, 205] # horizontal wall
CH_TLC      = [218, 213, 201] # top-left corner
CH_BLC      = [192, 212, 200] # bottom-left corner
CH_BRC      = [217, 190, 188] # bottom-right corner
CH_TRC      = [191, 184, 187] # top-right corner



#
# equip types
#
i=0;
EQ_MAINHAND =i; i+=1;
EQ_OFFHAND  =i; i+=1;
EQ_BODY     =i; i+=1;
EQ_BACK     =i; i+=1;
EQ_HEAD     =i; i+=1;
EQ_AMMO     =i; i+=1;




#
# genders
#
GENDER_MALE     = 11
GENDER_FEMALE   = 12
GENDER_OTHER    = 255




#
# Flags
#

# Monster and item flags

i = 1
ONGRID      = i; i+=1;  # Is positioned on the game grid
DEAD        = i; i+=1;  # Is dead
WET         = i; i+=1;  # Is wet
BLOODY      = i; i+=1;  # Is covered in blood
RAVAGED     = i; i+=1;  # Creature is starved: strong desire for food
THIEF       = i; i+=1;  # Creature desires gold / treasure and will steal it
MEAN        = i; i+=1;  # Creature is always hostile to rogues
SPRINT      = i; i+=1;  # Is sprinting
CONFU       = i; i+=1;  # Is confused
TRIPN       = i; i+=1;  # Is hallucinating
SLEEP       = i; i+=1;  # Is asleep
FIRE        = i; i+=1;  # Is burning
ACID        = i; i+=1;  # Is corroding in acid
SICK        = i; i+=1;  # Is poisoned / ill
IRRIT       = i; i+=1;  # Is irritated by chemicals
BLIND       = i; i+=1;  # Is blinded
PARAL       = i; i+=1;  # Is paralyzed
COUGH       = i; i+=1;  # Is in a coughing fit
VOMIT       = i; i+=1;  # Is in a vomiting fit
DEAF        = i; i+=1;  # Is deafened
INVIS       = i; i+=1;  # Is invisible
NVISION     = i; i+=1;  # Has Night vision
IMMUNE      = i; i+=1;  # Immune to poison
SEEINV      = i; i+=1;  # Can see invisible
SEEXRAY     = i; i+=1;  # LOS not blocked by walls
FLYING      = i; i+=1;  # Is currently flying
CANFLY      = i; i+=1;  # Can fly
CANTALK     = i; i+=1;  # Can engage in jolly conversation
CANEAT      = i; i+=1;  # Can be eaten
CANQUAFF    = i; i+=1;  # Can be quaffed
CANEQUIP    = i; i+=1;  # Can be equipped
CANUSE      = i; i+=1;  # Can be used
CANPUSH     = i; i+=1;  # Can be pushed
CANOPEN     = i; i+=1;  # Can open it like a container (not doors)
HOLDSFLUID  = i; i+=1;  # Can contain fluids


#
# Elements (types of damage)
#
i=0;
ELEM_PHYS   = i; i+=1;
ELEM_BIO    = i; i+=1;
ELEM_RADS   = i; i+=1;
ELEM_CHEM   = i; i+=1;
ELEM_FIRE   = i; i+=1;
ELEM_ELEC   = i; i+=1;



#
# Alerts
#

ALERT_EMPTYCONTAINER    = "This container is empty."
ALERT_CANTUSE           = "You can't use that!"



#
# Tastes
#
i=0;
TASTE_NASTY = i; i+=1;
TASTE_BITTER = i; i+=1;
TASTE_SWEET = i; i+=1;
TASTE_SALTY = i; i+=1;
TASTE_SAVORY = i; i+=1;

TASTES = {
    TASTE_NASTY : "yuck, disgusting!",
    TASTE_BITTER : "ack, bitter.",
    TASTE_SWEET : "yum, sweet.",
    TASTE_SALTY : "ack, salty.",
    TASTE_SAVORY : "mmm... delicious!",
}




#
# Materials
#
i=0;
MAT_FLESH       = i; i+=1;
MAT_BONE        = i; i+=1;
MAT_FUNGUS      = i; i+=1;
MAT_VEGGIE      = i; i+=1;
MAT_METAL       = i; i+=1;
MAT_CARBON      = i; i+=1;
MAT_PLASTIC     = i; i+=1;
MAT_STONE       = i; i+=1;
MAT_DUST        = i; i+=1;
MAT_WOOD        = i; i+=1;
MAT_SAWDUST     = i; i+=1;
MAT_PAPER       = i; i+=1;
MAT_LEATHER     = i; i+=1;
MAT_CLOTH       = i; i+=1;
MAT_GLASS       = i; i+=1;
MAT_GAS         = i; i+=1;
MAT_WATER       = i; i+=1;
MAT_OIL         = i; i+=1;



#
# Ammo types
#
i=0;
AMMO_BULLETS    = i; i+=1;  #bullets for rifles, pistols, etc.
AMMO_BALLS      = i; i+=1;  #balls for muskets
AMMO_SHOT       = i; i+=1;  #shotgun shells
AMMO_ELEC       = i; i+=1;  #electricity
AMMO_FLUIDS     = i; i+=1;  #any fluids
AMMO_OIL        = i; i+=1;
AMMO_HAZMATS    = i; i+=1;
AMMO_ACID       = i; i+=1;
AMMO_CHEMS      = i; i+=1;



#
# Skills
#
i=0;
SKL_FIGHT       = i; i+=1; #melee combat; throwing weapons
SKL_GUNS        = i; i+=1; #kinetic weapons; rifles, pistols, railguns
SKL_HEAVY       = i; i+=1; #heavy weapons; missiles, chem/bio/flame weapons
SKL_ENERGY      = i; i+=1; #energy weapons; lasers, masers, sonic
SKL_EXPLOS      = i; i+=1; #explosives; 
SKL_COMPUT      = i; i+=1; #computers
SKL_ROBOTS      = i; i+=1; #robotics
SKL_PILOT       = i; i+=1;
SKL_ATHLET      = i; i+=1; #athlete
SKL_PERSUA      = i; i+=1; #persuade
SKL_CHEMIS      = i; i+=1; #chemistry
SKL_SNEAK       = i; i+=1; #stealth

SKILLS={ # ID : name
SKL_FIGHT   : "fighting",
SKL_GUNS    : "guns",
SKL_HEAVY   : "heavy weapons",
SKL_ENERGY  : "energy weapons",
SKL_EXPLOS  : "explosives",
SKL_COMPUT  : "computers",
SKL_ROBOTS  : "robotics",
SKL_PILOT   : "pilot",
SKL_ATHLET  : "athletics",
SKL_PERSUA  : "persuasion",
SKL_CHEMIS  : "chemistry",
SKL_SNEAK   : "stealth",
    }
'''"guns" : SKL_GUNS,
"heavy weapons" : SKL_HEAVY,
"energy weapons" : SKL_ENERGY,
"computers" : SKL_COMPUT,
"robotics" : SKL_ROBOTS,
"fighting" : SKL_FIGHT,
"piloting" : SKL_PILOT,
"athletics" : SKL_ATHLET,
"persuasion" : SKL_PERSUA,
"chemistry" : SKL_CHEMIS,
"stealth" : SKL_SNEAK,'''



#
# Classes
#
#includes all jobs including non-playable jobs
i=0;
CLS_ENGINEER    = i; i+=1;
CLS_TECHNICIAN  = i; i+=1;
CLS_SECURITY    = i; i+=1;
CLS_ATHLETE     = i; i+=1;
CLS_PILOT       = i; i+=1;
CLS_SMUGGLER    = i; i+=1;
CLS_CHEMIST     = i; i+=1;
CLS_POLITICIAN  = i; i+=1;
CLS_RIOTPOLICE  = i; i+=1;
CLS_JANITOR     = i; i+=1;
CLS_DEPRIVED    = i; i+=1;
CLS_SOLDIER     = i; i+=1;
CLS_THIEF       = i; i+=1;



#
# Factions
# flags used for diplomacy
#
i=0;
FACT_ROGUE      = i; i+=1;
FACT_CITIZENS   = i; i+=1;
FACT_DEPRIVED   = i; i+=1;
FACT_ELITE      = i; i+=1;
FACT_WATCH      = i; i+=1;
FACT_MONSTERS   = i; i+=1;
#FACT_      = i; i+=1;



#
# ITEMS
#
i=0;



#
# gear qualities
#
i=0;
QU_CRUDE    =i; i+=1;
QU_MARKET   =i; i+=1;
QU_POLICE   =i; i+=1;
QU_MILITARY =i; i+=1;

QUALITIES={
# ID        :   name        %Acc,Atk,Dmg,Dur,$$$,KG,
QU_CRUDE    : ("crude",     (-50,-25,-25,-50,-50,33,),),
QU_MARKET   : ("market",    (-25,0,  0,  -25,-25,10,),),
QU_POLICE   : ("police",    (0,  25, 0,  0,  0,  0,),),
QU_MILITARY : ("military",  (25, 50, 25, 25, 50, -5,),),
    }



#
# FLUIDS
#
i=0;
FL_SMOKE    =i; i+=1;
FL_WATER    =i; i+=1;
FL_BLOOD    =i; i+=1;
FL_ACID     =i; i+=1;
FL_OIL      =i; i+=1;



#
# Sounds
#

SND_FIRE        = (40, "a fire",)
SND_FIGHT       = (100,"a struggle",)
SND_DOUSE       = (30, "the whisping sound of steam",)
SND_QUAFF       = (20, "gulping noises")


class Struct_Sound():
    def __init__(self):
        self.textSee=textSee
        self.textHear=textHear
        self.textHear=textHear


#
# Things, specific
#

class THG:#(Flag)
    i=0;
    GORE                = i; i+=1;
    JUG                 = i; i+=1;
    CORPSE_SHROOM       = i; i+=1;
    TREE                = i; i+=1;
    LOG                 = i; i+=1;
    WOOD                = i; i+=1;
    SAWDUST             = i; i+=1;
    GRAVE               = i; i+=1;
    BOX                 = i; i+=1;

















