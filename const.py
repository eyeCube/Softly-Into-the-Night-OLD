'''
    const.py
    
'''


import libtcodpy as libtcod





#
# Init Global Constants #
#



GAME_TITLE = "Softly Into the Night"

# Room size
ROOMW       = 150
ROOMH       = 150

TILES_PER_ROW = 16          # Num tiles per row
TILES_PER_COL = 16          # " per column






# commands #

    # for Input of special chars
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
# Thing types
#

T_FLOOR         =   249     # centered dot
T_DOORCLOSED    = ord('+')
T_DOOROPEN      = ord('-')
T_WALL          = ord('#')
T_TRAP          = ord('^')
T_STAIRUP       = ord('<')
T_STAIRDOWN     = ord('>')
T_MONEY         = ord('$')
T_POTION        =   173     # upside down '!'
T_PHONE         =   168     # upside down '?' - basically a "magic scroll"
T_CORPSE        = ord('%')
T_FOOD          = ord('%')
T_BULLET        = ord(':')
T_ROCK          = ord('`')
T_AMULET        = ord('"')
T_CONTAINER     = ord('|')
T_MULTIITEMS    = ord('&')
T_MELEEWEAPON   = ord('/')
T_THROWWEAPON   = ord('\\')
T_CHEMWEAPON    = ord('=')
T_BOW           = ord('}')
T_GUN           = ord('{')
T_SHIELD        = ord(')')
T_BUCKLER       = ord('(')
T_ARMOR         = ord(']')
T_HELMET        =   252     # fancy high up n
T_SCRAPELEC     =   171     # 1/2
T_SCRAPMETAL    =   172     # 1/4
T_CREDIT        =   172     # 1/4


#
# special chars #
#

# border 0
# single-line on all sides
CH_VW       = [179, 179, 186] # vertical wall
CH_HW       = [196, 205, 205] # horizontal wall
CH_TLC      = [218, 213, 201] # top-left corner
CH_BLC      = [192, 212, 200] # bottom-left corner
CH_BRC      = [217, 190, 188] # bottom-right corner
CH_TRC      = [191, 184, 187] # top-right corner







#
# Gameplay Constants
#

AVG_HEARING         = 100
COMBATROLL          = 20    # die roll
AVG_SPD             = 100 
NRG_MOVE            = 1     # multiplier 
NRG_ATTACK          = 200 
NRG_BOMB            = 150 
NRG_PICKUP          = 50    # grab thing and wield it (requires empty hand)
NRG_POCKET          = 200   # picking up and putting in your inventory
NRG_OPENCONTAINER   = 50    # Should it cost energy just to look in a container?
NRG_RUMMAGE         = 100   # Cost of picking an item from a container
NRG_EXAMINE         = 200
NRG_QUAFF           = 100
NRG_EAT             = 200   # per unit of consumption
NRGSAVED_FASTSHOT   = 50
DMG_FIRE            = 1    
DMG_BIO             = 1
SKILLMAX            = 2     # highest skill level you can attain
CHEM_DAMAGE         = 5     # damage chem effect causes when exposure meter fills

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





#
# Flags
#

# Monster and item flags

i = 1
DEAD        = i; i+=1;
RAVAGED     = i; i+=1;  # Creature is starved: strong desire for food
THIEF       = i; i+=1;  # Creature desires gold / treasure and will steal it
MEAN        = i; i+=1;  # Creature is always hostile to rogues
CONFU       = i; i+=1;  # Is confused
TRIPN       = i; i+=1;  # Is hallucinating
SLEEP       = i; i+=1;  # Is asleep
FIRE        = i; i+=1;  # Is burning
WET         = i; i+=1;  # Is wet
SICK        = i; i+=1;  # Is poisoned / ill
IRRIT       = i; i+=1;  # Is irritated
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
CANTALK     = i; i+=1;  # Can engage in jolly conversation
CANFLY      = i; i+=1;  # Can fly
FLYING      = i; i+=1;  # Is currently flying
CANEAT      = i; i+=1;  # Can be eaten
CANQUAFF    = i; i+=1;  # Can be quaffed
CANEQUIP    = i; i+=1;  # Can be equipped
CANUSE      = i; i+=1;  # Can be used


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
MAT_PAPER       = i; i+=1;
MAT_LEATHER     = i; i+=1;
MAT_CLOTH       = i; i+=1;
MAT_GLASS       = i; i+=1;



#
# Ammo types
#
i=0;
AMMO_BULLETS    = i; i+=1;
AMMO_ELEC       = i; i+=1;
AMMO_OIL        = i; i+=1;
AMMO_HAZMATS    = i; i+=1;
AMMO_ACID       = i; i+=1;



#
# Skills
#
i=0;
SKL_GUNS        = i; i+=1;
SKL_HEAVY       = i; i+=1;
SKL_TECH        = i; i+=1;
SKL_ENGINR      = i; i+=1;
SKL_FIGHTR      = i; i+=1;
SKL_PILOT       = i; i+=1;
SKL_ATHLET      = i; i+=1;
SKL_PERSUA      = i; i+=1;
SKL_CHEMIS      = i; i+=1;
SKL_SNEAK       = i; i+=1;

SKILLS = {
"guns" : SKL_GUNS,
"tech" : SKL_TECH,
"chemistry" : SKL_CHEMIS,
"engineering" : SKL_ENGINR,
"fighting" : SKL_FIGHTR,
"piloting" : SKL_PILOT,
"athletics" : SKL_ATHLET,
"persuasion" : SKL_PERSUA,
"heavy weapons" : SKL_HEAVY,
    }



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

CLASSES = {
CLS_ENGINEER    : "E",
CLS_TECHNICIAN  : "T",
CLS_THIEF       : "t",
CLS_SECURITY    : "O",
CLS_ATHLETE     : "A",
CLS_PILOT       : "p",
CLS_SMUGGLER    : "u",
CLS_CHEMIST     : "C",
CLS_POLITICIAN  : "I",
CLS_RIOTPOLICE  : "P",
CLS_JANITOR     : "j",
CLS_DEPRIVED    : "d",
CLS_SOLDIER     : 'S',
    }



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
# ITEMS
#
i=0;

#
# weapons
#
'''
i=1
WP_ARMINGSWORD  = i; i+=1;
WP_LONGSWORD    = i; i+=1;
WP_ESTOC        = i; i+=1;
'''




'''
DEEP        = libtcod.Color(20,20,0)
ACCENT      = libtcod.Color(255,230,165)
LTGRAY      = libtcod.Color(200,200,200)
GRAY        = libtcod.grey
DKGRAY      = libtcod.Color(80,80,80)
VDKGRAY     = libtcod.Color(50,50,50)
GOLD        = libtcod.Color(255,150,50)
LTCYAN      = libtcod.Color(150,200,200)
LTPINK      = libtcod.Color(255,0,75)
RED         = libtcod.Color(150,0,0)
DKRED       = libtcod.Color(60,0,0)
BLUE        = libtcod.Color(55,120,170)
GREEN       = libtcod.Color(140,210,40)
DKGREEN     = libtcod.Color(0,100,0)
YELLOW      = libtcod.Color(200,200,50)
SWAMP       = libtcod.Color(50,50,0)
ORANGE      = libtcod.Color(255,155,40)
TEAL        = libtcod.Color(0,100,150)
MAGENTA     = libtcod.Color(200,50,150)
VIOLET      = libtcod.Color(150,50,200)
PURPLE      = libtcod.Color(180,60,180)'''







