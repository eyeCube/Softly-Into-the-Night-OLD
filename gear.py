'''
    gear.py

    Armor, helmets
    Functions for making gear items
'''

from const import *
from colors import COLORS as COL
#import rogue as rog
import thing

ARMR = T_ARMOR
HELM = T_HELMET

FLSH = MAT_FLESH
LETH = MAT_LEATHER
CLTH = MAT_CLOTH
WOOD = MAT_WOOD
BONE = MAT_BONE
CARB = MAT_CARBON
PLAS = MAT_PLASTIC
METL = MAT_METAL

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
#--Name-----------------------Type,$$$$$, KG,   Dur, Mat, (DV, AV, MSp, Vis,FIR,BIO,)
    #Armor
"cloak"                     :(ARMR,420,   6.0,  150, CLTH,( 4,  1, -3,   0,  10, 10,), ),
"skin suit"                 :(ARMR,450,   14.7, 90,  FLSH,( 2,  2, -6,   0,  0,  10,), ),
"boiled leather plate"      :(ARMR,975,   12.5, 180, LETH,( 0,  4, -6,   0,  5,  5,), ),
"bone armor"                :(ARMR,890,   27.8, 475, BONE,(-4,  7, -15,  0,  15, 10,), ),
"carb garb"                 :(ARMR,1100,  22.5, 600, CARB,(-3,  8, -12,  0,  10, 10,), ),
"metal gear"                :(ARMR,9950,  27.5, 1000,METL,(-4,  11,-18,  0,  5,  5,), ),
"full metal suit"           :(ARMR,12000, 35.1, 1200,METL,(-5,  14,-21,  0,  5,  10,), ),
"graphene armor"            :(ARMR,58250, 16.5, 900, CARB,(-2,  20,-9,   0,  20, 20,), ),
"space suit"                :(ARMR,36000, 40.0, 50,  CARB,(-15, 3, -33,  0,  20, 40,), ),
"hazard suit"               :(ARMR,2445,  14.5, 75,  PLAS,(-12, 2, -20,  0,  5,  50,), ),
"disposable PPE"            :(ARMR,110,   9.25, 25,  PLAS,(-9,  1, -20,  0, -10, 30,), ),
"wetsuit"                   :(ARMR,1600,  8.2,  50,  PLAS,( 0,  0, -6,   0,  30, 5,), ),
"fire blanket"              :(ARMR,600,   12.4, 175, CLTH,(-3,  1, -9,   0,  35, 15,), ),
"burn jacket"               :(ARMR,1965,  19.5, 150, CLTH,(-5,  2, -12,  0,  50, 15,), ),
    #Helmets
"bandana"                   :(HELM,40,    0.1,  30,  CLTH,( 2,  0,  0,   0,  5,  10,), ),
"skin mask"                 :(HELM,180,   1.25, 20,  FLSH,( 1,  0,  0,  -1,  0,  5,), ),
"wood mask"                 :(HELM,10,    1.0,  60,  WOOD,( 1,  1, -3,  -1, -5,  5,), ),
"skull helm"                :(HELM,750,   2.8,  125, BONE,(-3,  1, -6,  -2,  5,  5,), ),
"carb hat"                  :(HELM,1200,  2.1,  310, CARB,(-2,  2, -6,  -2,  5,  5,), ),
"metal mask"                :(HELM,6000,  2.2,  375, METL,(-3,  3, -3,  -2,  0,  5,), ),
"metal helm"                :(HELM,8500,  3.0,  600, METL,(-4,  4, -6,  -2,  0,  5,), ),
"graphene mask"             :(HELM,21850, 0.8,  225, CARB,(-1,  5, -3,  -2,  10, 10,), ),
"graphene helmet"           :(HELM,25450, 1.2,  310, CARB,(-1,  6, -3,  -1,  10, 10,), ),
"space helmet"              :(HELM,51950, 3.5,  50,  CARB,(-4,  3, -12, -1,  15, 25,), ),
"gas mask"                  :(HELM,19450, 2.5,  40,  PLAS,(-2,  1, -3,  -2,  10, 30,), ),
"respirator"                :(HELM,2490,  1.7,  35,  PLAS,(-3,  0, -6,   0,  20, 15,), ),

    }



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
    
    #item resistances

    return g
#
























