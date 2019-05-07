'''
    fluids
'''

from const import *
import thing
from colors import COLORS as COL

#non-tile container of fluids
class FluidContainer:
    def __init__(self,size):
        self.size=size
        self.quantity=0
        self.fluidType=None

#Fluid data, each type of fluid has one (1) unique fluid data object.
class Data:

    def __init__(self, x,y, t=T_FLUID, name=None,
                 color=None, material=None, d=1,v=1,kg=1,
                 burns=False, putsout=False):

        self._type=t
        self.name=name
        self.color=color
        self.material=material
        self.density=d
        self.viscosity=v
        self.mass=kg
        self.flammable=burns
        self.extinguish=putsout  #does it put out fires?

#Tile fluid container
class Fluid:

    def __init__(self, x,y):
        self.x=x
        self.y=y
        self.dic={}
        self.size=0 #total quantity of fluid in this tile

    def getData(self, stat):    #get a particular stat about the fluid
        return FLUIDS[self.name].__dict__[stat]
    
    def clear(self):            #completely remove all fluids from the tile
        self.dic={}
        self.size=0
    
    def add(self, name, quantity=1):
        newQuant = self.dic.get(name, 0) + quantity
        self.dic.update({name : newQuant})
        self.size += quantity
        
        '''floodFill = False
        if self.size + quantity > MAX_FLUID_IN_TILE:
            quantity = MAX_FLUID_IN_TILE - self.size
            floodFill = True #partial floodfill / mixing
            #how should the fluids behave when you "inject" a new fluid into a full lake of water, etc.?
            #regular floodfill will not cut it
            #maybe just replace the current fluid with the new fluid to keep it simple.
            '''

        '''if floodFill:
            #do flood fill algo.
            #this is going to also have to run a cellular automata to distribute different types of fluids
            return'''

    def removeType(self, name, quantity=1):
        if self.size > 0:
            curQuant = self.dic.get(name, 0)
            newQuant = max(0, curQuant - quantity)
            diff = curQuant - newQuant
            if not diff:     #no fluid of that type to remove
                return
            self.size -= diff
            if newQuant != 0:
                self.dic.update({name : newQuant})
            else:
                #we've run out of this type of fluid
                self.dic.remove(name)


            
        
#effects
def _cough(actor, n):
    pass
def _hydrate(actor, n):
    actor.hydration += n * WATER_HYDRATE
def _blood(actor, n):
    pass
def _acid(actor, n):
    pass
def _sick(actor, n):
    pass
def _drunk(actor, n):
    pass

FLUIDS = {
#attributes:
#   d       : density
#   v       : viscosity
#   kg      : mass
#   flamm   : flammable?
#   snuff   : snuffs out fires?
#  ID       : (    type,   name,      color,          d,    v,    kg,  flamm,snuff,effect,
FL_SMOKE    : Data(T_GAS,  "smoke",   COL['white'],   0.05, 0.01, 0.01,False,False,_cough,),
FL_WATER    : Data(T_FLUID,"water",   COL['blue'],    1,    1,    0.1, False,True, _hydrate,),
FL_BLOOD    : Data(T_FLUID,"blood",   COL['red'],     1.1,  2,    0.12,False,True, _blood),
FL_ACID     : Data(T_FLUID,"acid",    COL['green'],   1.21, 0.5,  0.2, False,True, _acid),
FL_OIL      : Data(T_FLUID,"oil",     COL['purple'],  0.9,  3,    0.3, True,False, _sick),
FL_MOONSHINE: Data(T_FLUID,"moonshine",COL['brown'],  1.2,  0.8,  0.15,True,False, _drunk),
    }
FLUID_COMBONAMES={
FL_SMOKE    : "smokey",
FL_WATER    : "watery",
FL_BLOOD    : "bloody",
FL_ACID     : "acidic",
FL_OIL      : "oily",
    }

#create a fluid
def create_fluid(x,y,ID,volume):
    fluid = Fluid(x,y)
    fluid.add(ID, volume)
    return fluid

        

def simulate_flow():
#idea: if any fluid tiles contain more than the maximum allowed,
    #always flow outward using flood fill if necessary.
    for fluid in rog.list_fluids():
        #simultaneous cellular automata
        newMap = TileMap(self.w,self.h)
        newMap.COPY(rog.map())
        #define some functions to reduce duplicate code
        def _doYourThing(x,y,num,nValues): # alter a tile or keep it the same based on input
            if nValues[num]==-1:
                newMap.tile_change(x,y,offChar)
            elif nValues[num]==1:
                newMap.tile_change(x,y,onChar)
        for ii in range(iterations):
            for x in range(self.w):
                for y in range(self.h):
                    num = newMap.countNeighbors(x,y, onChar)
                    _doYourThing(x,y,num,nValues)
        self.COPY(newMap)
        
