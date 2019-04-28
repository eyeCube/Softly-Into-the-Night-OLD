'''
    weapons.py
    Author: Jacob Wharton

'''

import random

from const import *
from colors import COLORS as COL
import rogue as rog
import thing
import action


NUMWPNSTATS = 3

MEL     = T_MELEEWEAPON
THRO    = T_THROWWEAPON
GUN     = T_GUN
CHEM    = T_CHEMWEAPON

#ARRO    = T_ARROW
#BOW     = T_BOW

FLSH = MAT_FLESH
LETH = MAT_LEATHER
CLTH = MAT_CLOTH
WOOD = MAT_WOOD
BONE = MAT_BONE
CARB = MAT_CARBON
PLAS = MAT_PLASTIC
METL = MAT_METAL

A_ELEC = AMMO_ELEC
A_OIL  = AMMO_OIL
A_BULL = AMMO_BULLETS
A_HAZM = AMMO_HAZMATS
A_ACID = AMMO_ACID
#A_ARRO = AMMO_ARROWS

PH = ELEM_PHYS
FI = ELEM_FIRE
BI = ELEM_BIO
CH = ELEM_CHEM
EL = ELEM_ELEC
RA = ELEM_RADS




        

WEAPONS = {
# $$$, KG, Dur      price, mass, durability
# Rn                maximum Range
# At,Dm             Attack (accuracy), Damage,         
# DV,AV,            Dodge Value, Armor Value,
# Asp,Msp           Attack Speed, Move Speed,
# FIR,BIO,          FIRE damage, BIO damage
# Ammo              Ammunition / Fuel required to use weapon
    
           ##------- Type, $$$$, KG,  Dur, Mat, (Rn,At,Dm, DV, AV, Asp,Msp,ELEM),Ammo,{Misc.Mods},
    # melee weapons
"pocket knife"      :(MEL, 15,   0.25,120, METL,(1, 6, 3,   1,  0,  40, 0, PH,),None,),
"baton"             :(MEL, 45,   0.75,310, PLAS,(1, 7, 2,   1,  0,  5, -3, PH,),None,),
"graphene baton"    :(MEL, 900,  0.6, 480, CARB,(1, 9, 4,   2,  0,  10,-3, PH,),None,),
"cudgel"            :(MEL, 15,   1.5, 680, METL,(1, 3, 15, -1,  0, -33,-9, PH,),None,),
"axe"               :(MEL, 120,  1.25,350, METL,(1, 5, 12,  0,  0, -22,-6, PH,),None,),
"sword"             :(MEL, 1450, 1.25,260, METL,(1, 12,6,   2,  0,  33,-6, PH,),None,),
"spring-blade"      :(MEL, 9660, 2.8, 150, CARB,(1, 8, 22, -2,  0, -60,-15,PH,),A_ELEC,),
"buzz saw"          :(MEL, 7500, 3.5, 480, METL,(1, 15,5,  -5,  0,  66,-18,PH,),A_ELEC,),
    # chemical weapons
"shitstormer"       :(CHEM,1090, 2.5, 220, PLAS,(4, 5, 25, -4,  0, -25,-15,BI,),A_HAZM,),
"raingun"           :(CHEM,2000, 2.85,175, PLAS,(3, 26,40, -5,  0,  50,-18,CH,),A_ACID,),
"battery gun"       :(CHEM,2000, 4.20,175, PLAS,(2, 40,70, -8,  0, -60,-24,EL,),A_ELEC,),
"plasma sword"      :(CHEM,84490,2.0, 250, METL,(1, 11,100,-2,  0, -40,-12,FI,),A_OIL,),
    # guns
"pistol"            :(GUN, 2990, 1.0, 200, METL,(10,25,10,  0,  0,  33,-3, PH,),A_BULL,),
"rifle"             :(GUN, 4200, 2.2, 240, METL,(16,35,18, -3,  0, -45,-12,PH,),A_BULL,),
"carbine"           :(GUN, 3750, 1.7, 280, METL,(12,30,16, -2,  0, -15,-9, PH,),A_BULL,),
}

'''
#need to change the theme of these weapons. Not medieval theme.
#futuristic cyberpunk lovecraftian horror dystopia themed.
"hunting knife"     :(MEL, 0, 18,  0.6, 250, (10,9,  0,  0,), ),

"dagger"            :(MEL, 0, 38,  0.6, 350, (14,10, 0,  0,), ),

"sword of arms"     :(MEL, 1, 142, 1.1, 170, (6, 12,-3, -1,), ),
"bastard sword"     :(MEL, 3, 256, 1.5, 130, (7, 16,-6, -2,), ),
"smallsword"        :(MEL, 1, 875, 1.0, 140, (10,9, -3, -1,), ),
"estoc"             :(MEL, 1, 1550,1.0, 120, (13,8, -3, -1,), ),
"zweihander"        :(MEL, 5, 1800,2.6, 100, (7, 24,-15,-4,),),

"battle ax"         :(MEL, 4, 360, 1.75,750, (8, 28,-18,-3,),),

"mace"              :(MEL, 3, 75,  1.4, 1400,(6, 20,-15,-2,),),
"war hammer"        :(MEL, 3, 75,  1.8, 850, (6, 24,-18,-3,),),

"quarterstaff"      :(MEL, 5, 80,  2.0, 30,  (5, 6,  6, -4,), ),
"spear"             :(MEL, 4, 30,  1.25,15,  (12,12, 6, -4,), ),



"flamed blade"      :(MEL, 5, 7565,2.3, 80,  (8, 27,-12,-4,),),
"ceremonial blade"  :(MEL, 6, 9695,4.0, 20,  (6, 20,-30,-5,),),

"throwing ax"       :(MEL, 2, 12,  1.0, 600, (7, 15,-12,-2,), ),
"war ax"            :(MEL, 3, 25,  1.15,800, (7, 22,-12,-2,), ),

"club"              :(MEL, 3, 2,   1.2, 950, (5, 18,-15,-2,),),
"flail"             :(MEL, 5, 160, 2.2, 520, (3, 32,-24,-4,),),
"mourning star"     :(MEL, 5, 240, 2.8, 620, (5, 26,-21,-5,),),


"javelin"           :(MEL, 2, 4,   0.75,10,  (10,8,  6, -3,), ),

"shortbow"          :(BOW, 3, 60,  1.1, 80,  (7, 8, -12,-1,),),
"recurve bow"       :(BOW, 3, 180, 1.0, 125, (11,10,-6, -1,),),
"longbow"           :(BOW, 4, 260, 1.6, 50,  (15,16,-24,-3,),),
"crescent moon"     :(BOW, 4, 2650,1.6, 60,  (13,14,-12,-2,),),

"broadhead arrow"   :(ARRO,0, 1,   0.05, 2,  (2, 5,  0,  0,), ),
"bodkin arrow"      :(ARRO,0, 4,   0.05, 3,  (5, 7,  0,  0,), ),

"iron dart"         :(THRO,0, 3,   0.05, 5,  (3, 4, -3,  0,), ),
}
'''

#"crossbow"          :(CBOW,1, 415, 5.0, 240, (6, 16,-6, -4,),{'lsp':-60},),

#"crossbow bolt"     :(BOLT,0, 6,   0.05, 4,  (4, 6,  0,  0,), ),







def create_weapon(name, x,y):
    weap = thing.Thing()
    weap.name = name
    weap.x = x
    weap.y = y

    data = WEAPONS[name]
    weap.name       = name
    weap.type       = data[0]
    weap.mask       = weap.type
    weap.value      = data[1]   # $$$
    weap.stats.mass = data[2]   # kg
    weap.stats.hpmax= data[3]   # durability
    weap.stats.hp   = data[3]   # durability
    weap.material   = data[4]
    weap.statMods   = {}        # stat modifiers for equipping
    if data[5][0]:  weap.statMods.update({'range':data[5][0]})
    if data[5][1]:  weap.statMods.update({'atk':data[5][1]})
    if data[5][2]:  weap.statMods.update({'dmg':data[5][2]})
    if data[5][3]:  weap.statMods.update({'dfn':data[5][3]})
    if data[5][4]:  weap.statMods.update({'arm':data[5][4]})
    if data[5][5]:  weap.statMods.update({'asp':data[5][5]})
    if data[5][6]:  weap.statMods.update({'msp':data[5][6]})
    if data[5][7]:  weap.statMods.update({'element':data[5][7]})
    weap.ammoType   = data[6]
    #for mod in data[7]:
    #    weap.mods.append(mod)
    
    weap.color      = COL['white']
    weap.equipType  = EQ_MAINHAND
    rog.make(weap,CANEQUIP)

    return weap
#


'''class Bomb(thing.Thing):
    RADIUS=4
    DMG=16
    MASS=.5

    def __init__(self, x,y, fuse):
        super(Bomb,self).__init__()

        self.x      =x
        self.y      =y
        self.timer  =fuse
        self.name   ="bomb"
        self.type   ='*'
        self.mask   =self.type
        self.color  =COL['yellow']
        self.bgcolor=COL['black']
        self.r      =Bomb.RADIUS
        self.dmg    =Bomb.DMG
        self.mass   =Bomb.MASS
        #self.explo_noise=BOMB_NOISE
        
        rog.register_inanimate(self)
        rog.register_timer(self)

    def tick(self):
        if self.timer == 0:
            self.explode()
        self.timer -= 1

    def explode(self):
        rog.make(self,DEAD)
        action.explosion(self)
        self.close()
    
    def close(self):
        rog.release_inanimate(self)
        rog.release_timer(self)
'''


















                   


'''
"javelin"           :(SPEARS,   0,3,16,  0.75,{'atk':3,'dmg':4,'nrg':5} ),
"claymore"          :('/',SWORDS,   5,1,1800,2.4, 100,{'atk':1,'dmg':12,'nrg':7} ),
"morning star"      :('*',CUDGELS,  5,1,74,  2.6, 320,{'atk':0,'dmg':10,'nrg':9} ),
'''

'''{pointer_to_mon : {'mainHand' : effectID} }
{effectID : {effectDict} }
'''

'''
def get_wpnStats(item):
    stats = [0 for i in range(NUMWPNSTATS)]

    if item != None:
        stats[0] += item.atk
        stats[1] += item.dfn
        stats[2] += item.dmg
        if weap.type in obj.skills:
            for i in range(NUMWPNSTATS):
                stats[i] += SKILL_STATBONUS[weap.skill][i]
    else:
        stats[0] += item.atk
        stats[1] += item.dfn
        stats[2] += item.dmg
        if SK_UNARMED in obj.skills:
            for i in range(NUMWPNSTATS):
                stats[i] += SKILL_STATBONUS[SK_UNARMED][i]

    return stats
'''





