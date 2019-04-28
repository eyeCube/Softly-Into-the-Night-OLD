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
                 flammable=False, extinguish=False):

        self._type=t
        self.name=name
        self.color=color
        self.material=material
        self.density=d
        self.viscosity=v
        self.mass=kg
        self.flammable=flammable
        self.extinguish=extinguish  #does it put out fires?

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
        floodFill = False
        if self.size + quantity > MAX_FLUID_IN_TILE:
            quantity = MAX_FLUID_IN_TILE - self.size
            floodFill = True #partial floodfill / mixing
            #how should the fluids behave when you "inject" a new fluid into a full lake of water, etc.?
            #regular floodfill will not cut it
            #maybe just replace the current fluid with the new fluid to keep it simple.
            
        newQuant = self.dic.get(name, 0) + quantity
        self.dic.update({name : newQuant})
        self.size += quantity

        if floodFill:
            #do flood fill algo.
            #this is going to also have to run a cellular automata to distribute different types of fluids
            return

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
            
        

FLUIDS = {
#attributes:
#   d       : density
#   v       : viscosity
#   kg      : mass
#   flamm   : flammable?
#   snuff   : snuffs out fires?
#name       : (    type,   name,      color,          material,   d,    v,    kg,  flamm,snuff,
"smoke"     : Data(T_GAS,  "smoke",   COL['white'],   MAT_GAS,    0.01, 0.01, 0,   False,False,),
"water"     : Data(T_FLUID,"water",   COL['blue'],    MAT_WATER,  1,    1,    0.1, False,True,),
"blood"     : Data(T_FLUID,"blood",   COL['red'],     MAT_WATER,  0.9,  2,    0.1, False,True,),
    }
def create_fluid(x,y,name):
    fluid = FLUIDS[name] #maybe this should return an actual new Fluid object...
    return fluid

        
#****????
#should fluids be Things, creatures, tiles, or something else???
#


def simulate_flow():
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
        

