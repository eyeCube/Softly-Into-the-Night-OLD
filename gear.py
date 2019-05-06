'''
    gear.py

    Armor, helmets
    Functions for making gear items
'''


import random

from const import *
from colors import COLORS as COL
import rogue as rog
import thing
import action



ARMR = T_ARMOR
HELM = T_HELMET
BACK = T_CLOAK

NUMWPNSTATS = 3

MEL     = T_MELEEWEAPON
THRO    = T_THROWWEAPON
ENER    = T_ENERGYWEAPON
HEVY    = T_HEAVYWEAPON
GUN     = T_GUN

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
A_BULL = AMMO_BULLETS
A_BALL = AMMO_BALLS
A_SHOT = AMMO_SHOT
A_FLUID= AMMO_FLUIDS
A_OIL  = AMMO_OIL
A_HAZM = AMMO_HAZMATS
A_ACID = AMMO_ACID
A_CHEM = AMMO_CHEMS
#A_ARRO = AMMO_ARROWS

PH = ELEM_PHYS
FI = ELEM_FIRE
BI = ELEM_BIO
CH = ELEM_CHEM
EL = ELEM_ELEC
RA = ELEM_RADS


#GEAR
    #Columns:
    #   $$$$$   cost
    #   KG      mass
    #   Dur     durability
    #   Mat     material
    #   DV      Dodge Value
    #   AV      Armor Value
    #   Msp     Move Speed
    #   Vis     Vision
    #   FIR     Fire Resist
    #   BIO     Bio Resist
    #
GEAR = {
#--Name-----------------------Type,Dlv,$$$$$, KG,   Dur, Mat, (DV, AV, MSp, Vis,FIR,BIO,)
    #Back
"cloak"                     :(BACK,1,  420,   6.0,  150, CLTH,( 4,  1, -3,  0,  10, 10,), ),
    #Armor
"skin suit"                 :(ARMR,1,  450,   14.7, 90,  FLSH,( 2,  2, -6,  0,  0,  10,), ),
"boiled leather plate"      :(ARMR,1,  975,   12.5, 180, LETH,( 0,  3, -6,  0,  5,  5,), ),
"bone armor"                :(ARMR,2,  890,   27.8, 475, BONE,(-6,  5, -18, 0,  15, 10,), ),
"carb garb"                 :(ARMR,2,  1100,  22.5, 600, CARB,(-3,  3, -12, 0,  10, 10,), ),
"riot gear"                 :(ARMR,3,  3490,  20.5, 800, CARB,(-2,  6, -12, 0,  33, 25,), ),
"metal gear"                :(ARMR,12, 9950,  27.5, 1000,METL,(-4,  8, -18, 0,  5,  5,), ),
"full metal suit"           :(ARMR,14, 12000, 35.1, 1200,METL,(-5,  10,-21, 0,  5,  10,), ),
"graphene armor"            :(ARMR,18, 58250, 16.5, 900, CARB,(-2,  12,-9,  0,  20, 20,), ),
"space suit"                :(ARMR,15, 36000, 40.0, 50,  CARB,(-15, 3, -33, 0,  20, 45,), ),
"hazard suit"               :(ARMR,10, 2445,  14.5, 75,  PLAS,(-12, 2, -24, 0,  5,  50,), ),
"disposable PPE"            :(ARMR,1,  110,   9.25, 25,  PLAS,(-9,  1, -15, 0,  -15,30,), ),
"wetsuit"                   :(ARMR,3,  1600,  8.2,  50,  PLAS,( 0,  0, -6,  0,  33, 5,), ),
"fire blanket"              :(BACK,4,  600,   12.4, 175, CLTH,(-3,  1, -9,  0,  40, 15,), ),
"burn jacket"               :(ARMR,8,  1965,  19.5, 150, CLTH,(-5,  2, -12, 0,  55, 15,), ),
    #Helmets
"bandana"                   :(HELM,1,  40,    0.1,  30,  CLTH,( 2,  0,  0,  0,   5,  10,), ),
"skin mask"                 :(HELM,1,  180,   1.25, 20,  FLSH,( 1,  0,  0,  -1,  0,  5,), ),
"wood mask"                 :(HELM,1,  10,    1.0,  60,  WOOD,( 1,  1, -3,  -1,  -5, 5,), ),
"skull helm"                :(HELM,2,  750,   2.8,  125, BONE,(-3,  2, -6,  -2,  5,  5,), ),
"metal mask"                :(HELM,12, 6000,  2.2,  375, METL,(-3,  3, -3,  -2,  0,  5,), ),
"metal helm"                :(HELM,14, 8500,  3.0,  600, METL,(-4,  4, -6,  -2,  0,  5,), ),
"graphene mask"             :(HELM,18, 21850, 0.8,  225, CARB,(-1,  5, -3,  -2,  10, 10,), ),
"graphene helmet"           :(HELM,18, 25450, 1.2,  310, CARB,(-1,  6, -3,  -1,  10, 10,), ),
"space helmet"              :(HELM,15, 51950, 3.5,  50,  CARB,(-4,  1, -12, -1,  15, 25,), ),
"gas mask"                  :(HELM,11, 19450, 2.5,  40,  PLAS,(-2,  1, -3,  -2,  10, 30,), ),
"respirator"                :(HELM,5,  2490,  1.7,  35,  PLAS,(-3,  0, -6,  0,   20, 15,), ),

    }        

WEAPONS = {
# $$$, KG, Dur      price, mass, durability
# Ac                Accuracy (for ranged weapons or for throwing weapons),
# Cap               Ammo Capacity (for ranged weapons)
# At,Dm             Attack, Damage,
# DV,AV,            Dodge Value, Armor Value,
# Asp,Msp           Attack Speed, Move Speed,
# FIR,BIO,          FIRE damage, BIO damage
# Ammo              Ammunition / Fuel required to use weapon
    
           ##------- Type, $$$$, KG,  Dur, Mat, (Ac,Cap,At,Dm, DV, AV, Asp,Msp,ELEM),Ammo,{Misc.Mods},
    # melee weapons
"pocket knife"      :(MEL, 100,  0.25,120, METL,(4, 0,  6, 3,   1,  0,  40, 0, PH,),None,),
"baton"             :(MEL, 75,   0.75,310, PLAS,(3, 0,  7, 2,   1,  0,  5, -5, PH,),None,),
"staff"             :(MEL, 15,   0.6, 480, WOOD,(2, 0,  9, 4,   2,  0,  10,-12,PH,),None,),
"cudgel"            :(MEL, 1,    1.5, 680, WOOD,(0, 0,  3, 10, -1,  0, -33,-15,PH,),None,),
"axe"               :(MEL, 120,  1.25,350, METL,(1, 0,  5, 12,  0,  0, -22,-10,PH,),None,),
"sword"             :(MEL, 1950, 1.25,260, METL,(4, 0,  12,6,   2,  0,  33,-6, PH,),None,),
    # heavy weapons
"shitstormer"       :(HEVY,1090, 2.5, 220, PLAS,(6, 50, 25,25, -4,  0, -25,-15,BI,),A_HAZM,),
"raingun"           :(HEVY,1990, 2.85,175, PLAS,(5, 50, 26,40, -5,  0,  0, -18,CH,),A_ACID,),
"supersoaker 9000"  :(HEVY,6750, 3.5, 100, PLAS,(4, 100,32,1,  -10, 0, -10,-18,None,),A_FLUIDS,),
    # guns
"musket"            :(GUN, 1100, 2.5, 120, METL,(8, 1,  8, 8,  -3,  0, -45,-12,PH,),A_BALL,),
"flintlock pistol"  :(GUN, 1750, 1.3, 150, METL,(8, 1,  7, 4,   0,  0,  0, -3, PH,),A_BALL,),
"revolver"          :(GUN, 3990, 1.0, 360, METL,(12,6,  10,6,   0,  0,  0, -3, PH,),A_BULL,),
"rifle"             :(GUN, 4575, 2.2, 280, METL,(20,1,  15,12, -3,  0, -35,-12,PH,),A_BULL,),
"shotgun"           :(GUN, 2350, 2.0, 325, METL,(5, 1,  7, 3,  -2,  0, -25,-9, PH,),A_SHOT,),
    # energy weapons
"battery gun"       :(ENER,3250, 4.20,175, PLAS,(5, 20, 40,70, -7,  0, -60,-24,EL,),A_ELEC,),
    # heavy weapons
}
'''
"spring-blade"      :(MEL, 9660, 2.8, 150, CARB,(0, 0,  8, 22, -2,  0, -60,-15,PH,),A_ELEC,),
"buzz saw"          :(MEL, 7500, 3.5, 480, METL,(0, 0,  15,5,  -5,  0,  66,-18,PH,),A_ELEC,),
"plasma sword"      :(MEL, 84490,2.0, 250, METL,(0, 0,  11,100,-2,  0, -40,-12,FI,),A_OIL,),
'''



#pass in the name of a gear item
#   quality = 0 to 1. Determines starting condition of the item
def create_gear(name,x,y,quality):
    gData = GEAR[name]
    i =0; j = 0;
    g = thing.Thing()
    g.name = name
    g.x = x
    g.y = y
    g.type = gData[i]; i+=1;
    g.value = gData[i]; i+=1;
    g.mass = gData[i]; i+=1;
    g.hpmax = gData[i]; i+=1;
    g.material = gData[i]; i+=1;
    g.stats.dfn = gData[i][j]; j+=1;
    g.stats.arm = gData[i][j]; j+=1;
    g.stats.msp = gData[i][j]; j+=1;
    g.stats.sight = gData[i][j]; j+=1;
    g.stats.resbio = gData[i][j]; j+=1;
    g.stats.resfire = gData[i][j]; j+=1;

    g.color = COL['white']
    g.mask = g.type    
    g.hp = int(quality*g.hpmax)
    
    rog.make(g,CANEQUIP)
    if g.type == ARMR:
        g.equipType = EQ_BODY
    elif g.type == HELM:
        g.equipType = EQ_HEAD
    elif g.type == BACK:
        g.equipType = EQ_BACK
    
    #item resistances based on material

    return g
#


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
























