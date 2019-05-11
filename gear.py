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



NUMWPNSTATS = 3


PH = ELEM_PHYS
FI = ELEM_FIRE
BI = ELEM_BIO
CH = ELEM_CHEM
EL = ELEM_ELEC
RA = ELEM_RADS

ARMR = T_ARMOR
HELM = T_HELMET
BACK = T_CLOAK

TSTO    = T_STONE
MEL     = T_MELEEWEAPON
OFF     = T_OFFHANDWEAP
ENER    = T_ENERGYWEAPON
HEVY    = T_HEAVYWEAPON
GUN     = T_GUN
BOW     = T_BOW
EXPL    = T_EXPLOSIVE

FLSH = MAT_FLESH
LETH = MAT_LEATHER
CLTH = MAT_CLOTH
WOOD = MAT_WOOD
BONE = MAT_BONE
CARB = MAT_CARBON
PLAS = MAT_PLASTIC
METL = MAT_METAL
STON = MAT_STONE

A_BULL = AMMO_BULLETS
A_BALL = AMMO_BALLS
A_SHOT = AMMO_SHOT
A_ARRO = AMMO_ARROWS
A_ELEC = AMMO_ELEC
A_FLUID= AMMO_FLUIDS
A_OIL  = AMMO_OIL
A_HAZM = AMMO_HAZMATS
A_ACID = AMMO_ACID
A_CHEM = AMMO_CHEMS
A_ROCKT= AMMO_ROCKETS
A_GREN = AMMO_GRENADES
A_FLAM = AMMO_FLAMMABLE
A_ANY  = AMMO_ANYTHING



def get_gear_type(gData):           return gData[0]
def get_gear_value(gData):          return gData[1]
def get_gear_mass(gData):           return gData[2]
def get_gear_hpmax(gData):          return gData[3]
def get_gear_mat(gData):            return gData[4]
def get_gear_dfn(gData):            return gData[5][0]
def get_gear_arm(gData):            return gData[5][1]
def get_gear_msp(gData):            return gData[5][2]
def get_gear_sight(gData):          return gData[5][3]
def get_gear_resbio(gData):         return gData[5][4]
def get_gear_resfire(gData):        return gData[5][5]
def get_gear_reselec(gData):        return gData[5][6]
def get_gear_script(gData):         return gData[6]

def get_weapon_type(gData):         return gData[0]
def get_weapon_value(gData):        return gData[1]
def get_weapon_mass(gData):         return gData[2]
def get_weapon_hpmax(gData):        return gData[3]
def get_weapon_capacity(gData):     return gData[4]
def get_weapon_rt(gData):           return gData[5]
def get_weapon_jam(gData):          return gData[6]
def get_weapon_mat(gData):          return gData[7]
def get_weapon_range(gData):        return gData[7][0]
def get_weapon_atk(gData):          return gData[7][1]
def get_weapon_dmg(gData):          return gData[7][2]
def get_weapon_pow(gData):          return gData[7][3]
def get_weapon_dv(gData):           return gData[7][4]
def get_weapon_av(gData):           return gData[7][5]
def get_weapon_asp(gData):          return gData[7][6]
def get_weapon_msp(gData):          return gData[7][7]
def get_weapon_elem(gData):         return gData[7][8]
def get_weapon_ammo(gData):         return gData[8]
def get_weapon_mods(gData):         return gData[9]
def get_weapon_script(gData):       return gData[10]


def _cloak(tt):
    pass

def _nvisionGoggles(tt):
    pass

def _earPlugs(tt):
    pass

def _incendiary(tt):
    def func(self):
        rog.set_fire(self.x, self.y)
        rog.explosion("the bullet", self.x, self.y, 1)
    tt.deathFunction = func

def _molotov(tt):
    def func(self):
        diameter = 7
        radius = int(diameter/2)
        for i in range(diameter):
            for j in range(diameter):
                xx = self.x + i - radius
                yy = self.y + j - radius
                if not rog.in_range(self.x,self.y, xx,yy, radius):
                    continue
                rog.create_fluid(FL_NAPALM, xx,yy, dice.roll(3))
                rog.set_fire(xx,yy)
    tt.deathFunction = func


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
#--Name-----------------------Type,Dlv,$$$$$, KG,   Dur, Mat, (DV, AV, MSp, Vis,FIR,BIO,ELE), script
    #Back
"cloak"                     :(BACK,1,  420,   6.0,  150, CLTH,( 4,  1, -3,  0,  10, 10, 0,), _cloak,),
    #Armor
"skin suit"                 :(ARMR,1,  450,   14.7, 90,  FLSH,( 2,  2, -6,  0,  0,  10, 3,), None,),
"boiled leather plate"      :(ARMR,1,  975,   12.5, 180, LETH,( 0,  3, -6,  0,  5,  5,  15,), None,),
"bone armor"                :(ARMR,2,  890,   27.8, 475, BONE,(-6,  5, -18, 0,  15, 10, 0,), None,),
"carb garb"                 :(ARMR,2,  1100,  22.5, 600, CARB,(-3,  3, -12, 0,  10, 10, 0,), None,),
"riot gear"                 :(ARMR,3,  3490,  20.5, 700, CARB,(-2,  5, -12, 0,  33, 25, 0,), None,),
"metal gear"                :(ARMR,12, 9950,  27.5, 740, METL,(-4,  7, -18, 0,  5,  5,  -10,), None,),
"full metal suit"           :(ARMR,14, 12000, 35.1, 850, METL,(-5,  10,-21, 0,  5,  10, -20,), None,),
"graphene armor"            :(ARMR,18, 58250, 16.5, 900, CARB,(-2,  8, -9,  0,  20, 20, 25,), None,),
"bullet-proof armor"        :(ARMR,18, 135000,12.8, 1000,CARB,(-1,  12,-3,  0,  5,  5,  0,), None,),
"space suit"                :(ARMR,15, 36000, 40.0, 50,  CARB,(-15, 3, -33, 0,  20, 40, 5,), None,),
"hazard suit"               :(ARMR,10, 2445,  14.5, 75,  PLAS,(-12, 2, -24, 0,  5,  50, 10,), None,),
"disposable PPE"            :(ARMR,1,  110,   9.25, 25,  PLAS,(-9,  1, -15, 0,  -15,30, 5,), None,),
"wetsuit"                   :(ARMR,3,  1600,  8.2,  50,  PLAS,( 0,  0, -6,  0,  33, 5,  21,), None,),
"fire blanket"              :(BACK,4,  600,   12.4, 175, CLTH,(-3,  1, -9,  0,  40, 15, 10,), None,),
"burn jacket"               :(ARMR,8,  1965,  19.5, 150, CLTH,(-5,  2, -12, 0,  55, 15, 15,), None,),
    #Helmets
"bandana"                   :(HELM,1,  40,    0.1,  30,  CLTH,( 2,  0,  0,  0,  5,  10, 5,), None,),
"skin mask"                 :(HELM,1,  180,   1.25, 20,  FLSH,( 1,  0,  0,  -1, 0,  5,  2,), None,),
"wood mask"                 :(HELM,1,  10,    1.0,  60,  WOOD,( 1,  1, -3,  -1, -5, 5,  5,), None,),
"skull helm"                :(HELM,2,  750,   2.8,  125, BONE,(-3,  2, -6,  -2, 5,  5,  5,), None,),
"metal mask"                :(HELM,12, 6000,  2.2,  375, METL,(-3,  3, -3,  -2, 0,  5,  -5,), None,),
"metal helm"                :(HELM,14, 8500,  3.0,  600, METL,(-4,  4, -6,  -2, 0,  5,  -10,), None,),
"graphene mask"             :(HELM,18, 21850, 0.8,  225, CARB,(-1,  2, -3,  -2, 10, 10, 8,), None,),
"graphene helmet"           :(HELM,18, 25450, 1.2,  310, CARB,(-1,  3, -3,  -1, 10, 10, 10,), None,),
"kevlar hat"                :(HELM,14, 89500, 1.5,  750, CARB,(-1,  4, -3,  0,  0,  0,  0,), None,),
"space helmet"              :(HELM,15, 51950, 3.5,  50,  CARB,(-4,  1, -12, -1, 15, 25, 5,), None,),
"gas mask"                  :(HELM,11, 19450, 2.5,  40,  PLAS,(-2,  1, -3,  -2, 10, 45, 6,), None,),
"respirator"                :(HELM,5,  2490,  1.7,  35,  PLAS,(-3,  0, -6,  0,  20, 30, 3,), None,),
#"night vision goggles"
#"ear plugs"
    }        

WEAPONS = {
# Type              Weapon type
# $$$, KG, Dur      Value, mass, durability
# Cap               Ammo Capacity (for ranged weapons)
# Mat               Material
# Rn                Range/Accuracy (for ranged weapons or for throwing weapons),
# At,Dm,Pw          Attack, Damage (melee/throwing), Power (ranged weapon damage),
# DV,AV,            Dodge Value, Armor Value,
# Asp,Msp           Attack Speed, Move Speed,
# FIR,BIO,          FIRE damage, BIO damage
# Ammo              Ammunition / Fuel required to use weapon

    #Should melee damage be separated from ranged damage?
    #If you get claws and gain +2 dmg that should not affect gun damage.
    
           ##------- Type, $$$$, KG,  Dur, Cap,RT, Jam,Mat, (Rn,At,Dm,Pw, DV, AV, Asp,Msp,ELEM),Ammo,{Misc.Mods}, script script
    # melee weapons
"stone"             :(TSTO,1,    0.3, 150, 0,  0,  0,  STON,(6, 3, 3, 0,  0,  0, -10, 0, PH,),None,(),),
"stick"             :(MEL, 1,    0.75,50,  0,  0,  0,  WOOD,(4, 2, 2, 0,  0,  0,  10,-3, PH,),None,(),),
"fork"              :(MEL, 3,    0.1, 40,  0,  0,  0,  METL,(4, 3, 1, 0,  0,  0,  20, 0, PH,),None,(),), #CUTS
"cudgel"            :(MEL, 5,    1.5, 980, 0,  0,  0,  WOOD,(3, 3, 10,0,  -3, 0, -33,-12,PH,),None,(),),
"staff"             :(MEL, 15,   1.2, 400, 0,  0,  0,  WOOD,(4, 9, 4, 0,  1,  0,  33,-15,PH,),None,(REACH,),),
"axe"               :(MEL, 20,   1.25,650, 0,  0,  0,  WOOD,(4, 5, 12,0,  -2, 0, -25,-12,PH,),None,(),), #CUTS, CHOPS #(CHOPS TREES)
"baton"             :(MEL, 35,   0.75,500, 0,  0,  0,  PLAS,(3, 5, 2, 0,  0,  0,  10,-3, PH,),None,(),),
"spear"             :(MEL, 35,   1.5, 325, 0,  0,  0,  WOOD,(10,16,8, 0,  -1, 0,  33,-18,PH,),None,(REACH,), #CUTS),
"pocket knife"      :(MEL, 95,   0.2, 120, 0,  0,  0,  METL,(5, 8, 3, 0,  2,  0,  50, 0, PH,),None,(),), #CUTS
"bayonet"           :(MEL, 150,  0.3, 200, 0,  0,  0,  METL,(5, 9, 4, 0,  2,  0,  40, 0, PH,),None,(),), #CUTS
"dagger"            :(MEL, 275,  0.4, 240, 0,  0,  0,  METL,(6, 12,5, 0,  3,  0,  40, 0, PH,),None,(),), #CUTS
"sword"             :(MEL, 650,  1.25,260, 0,  0,  0,  METL,(6, 12,6, 0,  4,  0,  25,-6, PH,),None,(),), #CUTS
#chainsaw
#plasma sword
    # shields
"wooden shield"     :(OFF, 145,  5.3, 520, 0,  0,  0,  WOOD,(3, 0, 1, 0,  4,  3,  0, -24,PH,),None,(),),
"metal shield"      :(OFF, 540,  7.5, 900, 0,  0,  0,  METL,(3, 0, 2, 0,  3,  5,  0, -33,PH,),None,(),),
    # bows
"short bow"         :(BOW, 60,   1.1, 40,  1,  1,  0,  WOOD,(20,12,1, 2,  -1, 0, -10,-6,PH,),A_ARRO,(),),
"longbow"           :(BOW, 120,  1.6, 60,  1,  1,  0,  WOOD,(35,9, 1, 5,  -2, 0, -20,-9,PH,),A_ARRO,(),),
    # exposives
"molotov"           :(EXPL,50,   1.2, 5,   0,  0,  0,  METL,(8, 3, 1, 1,  -1, 0, -10,-6,PH,),None,(),), #_molotov
"IED"               :(EXPL,75,   2.5, 5,   0,  0,  0,  METL,(8, 3, 1, 1,  -1, 0, -10,-6,PH,),None,(),), #_ied
"frag grenade"      :(EXPL,165,  0.8, 5,   0,  0,  0,  METL,(8, 3, 1, 1,  -1, 0, -10,-6,PH,),None,(),), #_fragBomb
"land mine"         :(EXPL,425,  5.0, 5,   0,  0,  0,  METL,(8, 3, 1, 1,  -1, 0, -10,-6,PH,),None,(),), #_fragMine
    # heavy weapons
"MK-18 shitstormer" :(HEVY,2090, 2.5, 220, 100,3,  0,  PLAS,(7, 3, 1, 25, -4, 0,  0, -15,BI,),A_HAZM,(),),
"raingun"           :(HEVY,2990, 2.85,175, 125,3,  0,  PLAS,(7, 5, 1, 40, -5, 0,  0, -18,CH,),A_ACID,(),),
"supersoaker 9000"  :(HEVY,3750, 3.5, 100, 200,5,  0,  PLAS,(9, 5, 0, 3,  -10,0,  10,-18,None,),A_FLUID,(),),
"spring gun"        :(HEVY,1860, 7.3, 75,  1,  4,  0,  METL,(10,5, 0, 3,  -10,0, -33,-21,PH,),A_ANY,(),),
"flamethrower"      :(HEVY,5800, 12.7,100, 300,8,  0,  METL,(5, 15,2, 100,-15,0,  33,-40,FI,),A_FLAM,(),), #_flamethrower
#"napalm thrower"      :(HEVY,5800, 12.7,100, 300,8,  0,  METL,(5, 15,2, 100,-15,0,  33,-40,FI,),A_FLAM,(),), #_flamethrower
    # guns
"hand cannon"       :(GUN, 145,  8.75,450, 1,  10, 15, METL,(6, 18,5, 8,  -15,1, -50,-30,PH,),A_BALL,(),),
"musket"            :(GUN, 975,  2.5, 120, 1,  8,  8,  WOOD,(16,12,4, 6,  -3, 0, -33,-12,PH,),A_BALL,(),),
"flintlock pistol"  :(GUN, 1350, 1.3, 150, 1,  8,  12, WOOD,(8, 7, 2, 2,   0, 0, -25,-3, PH,),A_BALL,(),),
"revolver"          :(GUN, 3990, 1.1, 360, 6,  1,  8,  METL,(12,10,3, 4,   0, 0, -15,-3, PH,),A_BULL,(),),
"rifle"             :(GUN, 4575, 2.2, 280, 1,  1,  8,  WOOD,(30,16,4, 8,  -3, 0, -33,-12,PH,),A_BULL,(),),
"repeater"          :(GUN, 13450,2.0, 300, 7,  1,  7,  WOOD,(22,14,4, 8,  -3, 0, -15,-9, PH,),A_BULL,(),),
"'03 Springfield"   :(GUN, 26900,2.5, 350, 5,  1,  6,  WOOD,(50,22,4, 11, -3, 0, -33,-12,PH,),A_BULL,(),),
"luger"             :(GUN, 55450,0.9, 210, 8,  1,  10, METL,(16,12,3, 6,   0, 0, -6, -3, PH,),A_BULL,(),),
"shotgun"           :(GUN, 2150, 2.0, 325, 1,  1,  8,  WOOD,(8, 6, 4, 2,  -2, 0, -33,-9, PH,),A_SHOT,(),),
"double barrel shotgun":(GUN,6200,2.8,285, 2,  1,  8,  WOOD,(8, 6, 4, 2,  -3, 0, -33,-12,PH,),A_SHOT,(),),
    # energy weapons
"battery gun"       :(ENER,3250, 4.20,175, 20, 1,  0,  PLAS,(5, 40,2, 70, -7,  0, -60,-24,EL,),A_ELEC,(),),
                      
            ##------- Type, $$$$, KG,  Dur, Cap,RT,Jam,Mat, (Rn,At,Dm,Pw, DV, AV, Asp,Msp,ELEM),Ammo,{Misc.Mods},

#"laser pointer"
#"beam rifle"
#"taser"
#"megaphone"
#"paralysis ray"
#"grenade launcher"  :(HEVY,45910,8.2, 200, 1,  3,  0,  METL,(12,5, 0, 4,  -15,0, -33,-30,PH,),A_GREN,(),),
}
#add extra weapons (variations)
BAYONETS=("musket","rifle","shotgun","'03 Springfield",)
for wpn in BAYONETS:
##    _stats = WEAPONS[wpn]
##    bayonetDmg = 4
##    _stats.update( {set_weapon_dmg() : get_weapon_dmg(WEAPONS[wpn]) + bayonetDmg} )
    WEAPONS.update( {"{} with bayonet".format(wpn) : _stats} ))


AMMUNITION={
# Attributes:
#   type        ammo type
#   $$$, KG     value, mass
#   n           number shots
#   Acc, Atk, Dmg, Asp      Range, Attack, Damage, Attack Speed
# name                  : type,  $$$, KG, n, (Acc,Atk,Dmg,Asp,),script
"metal ball"            :(A_BALL,5,  0.1, 1, (0,  0,  4,  0,), None,)
"shotgun shell"         :(A_SHOT,5,  0.1, 5, (-4, -4, 2,  0,), None,)
"shotgun slug"          :(A_SHOT,6,  0.1, 1, (0,  0,  10, -10,), None,)
"small cartridge"       :(A_BULL,4,  0.02,1, (0,  2,  2,  0,), None,)
"magnum cartridge"      :(A_BULL,25, 0.04,1, (-2, -2, 8,  -33,), None,)
"large cartridge"       :(A_BULL,12, 0.06,1, (2,  6,  6,  -15,), None,)
"incendiary cartridge"  :(A_BULL,45, 0.1, 1, (-2, 12, 12, -33,), _incendiary)
    }



#non-weapon gear
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
    g.stats.reselec = gData[i][j]; j+=1;
    i+=1;
    script = gData[i]

    g.color = COL['white']
    g.mask = g.type    
    
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
    weap.type       = get_weapon_type(data)
    weap.mask       = weap.type
    weap.value      = get_weapon_value(data)
    weap.stats.mass = get_weapon_mass(data)
    weap.stats.hpmax= get_weapon_hpmax(data)
    weap.capacity   = get_weapon_capacity(data)
    weap.reloadTime = get_weapon_rt(data)
    weap.jamChance  = get_weapon_jam(data)
    weap.material   = get_weapon_mat(data)
    weap.statMods   = {}        # stat modifiers for equipping
    if get_weapon_range(data):  weap.statMods.update({'range':get_weapon_range(data)})
    if get_weapon_atk(data):  weap.statMods.update({'atk':get_weapon_atk(data)})
    if get_weapon_dmg(data):  weap.statMods.update({'dmg':get_weapon_dmg(data)})
    if get_weapon_pow(data):  weap.statMods.update({'pow':get_weapon_pow(data)})
    if get_weapon_dfn(data):  weap.statMods.update({'dfn':get_weapon_dv(data)})
    if get_weapon_arm(data):  weap.statMods.update({'arm':get_weapon_av(data)})
    if get_weapon_asp(data):  weap.statMods.update({'asp':get_weapon_asp(data)})
    if get_weapon_msp(data):  weap.statMods.update({'msp':get_weapon_msp(data)})
    if data[j][7]:  weap.statMods.update({'element':get_weapon_elem(data)); i+=1;
    j+=1
    weap.ammoType   = data[j]; j+=1;
    
        #mods = #data[j]
    #for mod in data[j]:
    #    weap.mods.append(mod)
    #j+=1;
    
    #script = data[j]; j+=1;

    #get resistances from material...
    
    weap.color      = COL['white']
    rog.makeEquip(weap, EQ_MAINHAND)

    return weap
#















'''
"spring-blade"      :(MEL, 9660, 2.8, 150, CARB,(0, 0,  8, 22, -2,  0, -60,-15,PH,),A_ELEC,),
"buzz saw"          :(MEL, 7500, 3.5, 480, METL,(0, 0,  15,5,  -5,  0,  66,-18,PH,),A_ELEC,),
"plasma sword"      :(MEL, 84490,2.0, 250, METL,(0, 0,  11,100,-2,  0, -40,-12,FI,),A_OIL,),
'''
#"bayonet"   :(MEL, 150,  0.3, 180, 0,  0,  METL,(4, 9, 4, 0,  2,  0,  40, 0, PH,),None,(),),

#--Name-----------------------Type,Dlv,$$$$$, KG,   Dur, Mat, (DV, AV, MSp, Vis,FIR,BIO,ELE)
    #Back
#"cloak"                     :(BACK,1,  420,   6.0,  150, CLTH,( 4,  1, -3,  0,  10, 10, 0,), ),

'''
    Example weapon display:
 #stats nerfed because it's crude


          ,
         /|
       ./ |
       |` |
      ./  |
      |`  |
      /   |
      \`  |
      /   |
      \`  |
      /   |
      \`  |
      /   |
      \`  |
      |   |
      |...|
  o___|___|___o
  "---|   |---"
       bb#
       #bb
       ###
       bb#
       #bb
       \#/
 
    [/] crude bayonet
    0.3kg     $28
    wield in main hand:                  
        Lo        50 (90)        
        Hi        1 (1)
        Atk       4
        Dmg       2  (physical)
        DV        2
        Atk Spd   40

        
    
    Armor display:
    
    [{] lacquered police cloak
    5.7kg     $1460
    wear on back:
        Lo        180 (200)
        Hi        1 (1)
        AV        1
        DV        4
        Move Spd  -3
        Fire Res  10
        Bio Res   10
    
'''









