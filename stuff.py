'''
    stuff.py
    inanimate tts to populate the world
'''

from const import *
import rogue as rog
import thing
import dice
from colors import COLORS as COL



#conversion functions:
# convert things into specific types of things by giving them certain data
def _edible(tt, nutrition, taste):
    rog.make(tt,EDIBLE)
    rog.taste=taste
    tt.nutrition=nutrition
def _food_poison(tt):
    _edible(tt, RATIONFOOD)
    rog.make(tt,SICK) #makes you sick when you eat it
def _food_ration_savory(tt):
    _edible(tt, RATIONFOOD, TASTE_SAVORY)
def _food_serving_savory(tt):
    _edible(tt, RATIONFOOD*3, TASTE_SAVORY)
def _food_meal_savory(tt):
    _edible(tt, RATIONFOOD*9, TASTE_SAVORY)
def _food_bigMeal_savory(tt):
    _edible(tt, RATIONFOOD*18, TASTE_SAVORY)
def _fluidContainer(tt):
    rog.init_fluidContainer(tt, 20)
def _bigFluidContainer(tt):
    rog.init_fluidContainer(tt, 100)
def _wood(tt):
    rog.make(tt, CANWET)
def _boxOfItems1(tt):
    rog.init_inventory(tt, 100)
    #newt=
    #rog.give(tt, newt)
def _still(tt):
    rog.make(tt, HOLDSFLUID)
    #...
def _dosimeter(tt):
    #todo: make this script
    #use function two options: 1) toggles on/off. 2) displays a reading only when you use it.
    rog.make(tt, WATERKILLS)
    rog.make(tt, CANUSE)
    def funcPlayer(obj, tt): 
        xx=obj.x
        yy=obj.y
        reading = rog.radsat(xx,yy)
        rog.msg("The geiger counter reads '{} rads'".format(reading))
        rog.drain(obj, 'nrg', NRG_USE)
    def funcMonster(obj, tt):
        rog.drain(obj, 'nrg', NRG_USE)
        rog.event_sight(obj.x,obj.y,"{t}{n} looks at a geiger counter.")
    tt.useFunctionPlayer = funcPlayer
    tt.useFunctionMonster = funcMonster
def _towel(tt):
    rog.make(tt, CANWET)
    rog.make(tt, CANUSE)
    rog.make(tt, CANEQUIP)
    tt.equipType = EQ_BODY #Head?? Which is default "equip?"
    tt.useFunctionPlayer = action.towel_pc
    tt.useFunctionMonster = action.towel
def _torch(tt):
    rog.make(tt, CANEQUIP)
    tt.equipType=EQ_OFFHAND
##def _cloak(tt):
##    rog.make(tt, CANEQUIP)
##    tt.equipType=EQ_OFFHAND
##    rog.make(tt, CANUSE)
##    tt.useFunctionPlayer = action.cloak_pc
##    tt.useFunctionMonster = action.cloak


STUFF={
#flag       :  name             type     material, color,  Lo,kg,  solid,push?,script,
THG.GORE    : ("hunk of flesh", T_MEAL, MAT_FLESH, 'red',  1, 1,   False,False,_food_meal_savory,),
THG.LOG     : ("log",           T_LOG,  MAT_WOOD, 'brown',500,20,  False,False,_wood,),
THG.WOOD    : ("wood",          T_WOOD, MAT_WOOD, 'brown',100,2,   False,False,_wood,),
THG.BOX     : ("crate",         T_BOX,  MAT_WOOD, 'brown',100,10,  True,True,  _boxOfItems1,),
THG.GRAVE   : ("grave",         T_GRAVE,MAT_STONE,'silver',100,200,True,False, None,),
THG.POT     : ("pot",           T_POT,  MAT_METAL,'metal',1000,100,True,True, _bigFluidContainer,),
THG.STILL   : ("still",         T_STILL,MAT_METAL,'metal', 20, 100,True,False, _still,),
THG.DOSIMETER:("geiger counter",T_DEVICE,MAT_METAL,'yellow',1,0.5, False,False,_dosimeter,),
THG.TOWEL   : ("towel",         T_TOWEL,MAT_CLOTH,'accent', 10,0.8,False,False,_towel,),
THG.TORCH   : ("torch",         T_TORCH,MAT_WOOD, 'brown',500,1.1, False,False,_torch,),
#THG.CLOAK
    }


#create a thing from STUFF; does not register thing
def create(x,y,ID):
    name,typ,mat,fgcol,lo,kg,solid,push,script = STUFF[ID]
    tt = thing.Thing(x,y, _type=typ,name=name,color=COL[fgcol])
    tt.mass = kg
    tt.material=mat
    if lo: hp(tt, lo)
    tt.isSolid = solid
    if push: rog.make(tt, CANPUSH)
    #_applyResistancesFromMaterial(tt, mat)
    return tt



#quick functions for multiple types of objects:
def hp(tt, value): #give a Thing a specified amount of HP and fully heal them
    tt.stats.hpmax=value; rog.givehp(tt);
#give a random number of items to the inventory of Thing tt
    #func is a function to build the items
    #_min is minimum number of items possible to give
    #_max is maximum "
def giveRandom(tt, func, _min, _max):
    for ii in range((_min - 1) + dice.roll(_max - (_min - 1))):
        item = func()
        rog.give(tt, item)



