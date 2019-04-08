'''
    thing.py
    Author: Jacob Wharton

    Contents:
      - class Position
      - class Stats
      - class Thing

'''

from const import *
import rogue as rog
from observer import Observable
from colors import COLORS as COL




'''
HP_PERLVL   = 5
HP_PEREND   = 5
MP_PERMND   = 5
SPD_PERAGI  = 
'''






# Thing class:
# In-game object; items, monsters, the player, etc.

class Thing(Observable):
    new_id = -1
    
    def __init__(self):
        super(Thing,self).__init__()
        
        self.id=Thing.get_new_id()
        
    #   vars that need to be set for all things are set to None
    #   but not all vars set to None must be set
        self.name           = None  # unique or generic
        self.title          = "the "
        self.pronouns   = ("it","it","its",)
        self.color      = None  # drawing color
        self.bgcolor    = COL['black']
        self.flags      = set()
        self.skills     = {}
        self.equip      = Equip()
        self.stats      = Stats(self)
        self.statMods   = {}    # when equipped by someone else
        self.isSolid    = False # cannot be moved through if solid
        self.isCreature = False
        self.x          = None  # position in the game world
        self.y          = None
        self.z          = None
        self.type       = None  # char (int) represents type/species
        self.mask       = None  # char (int) displayed to screen
        self.mass       = None  # KG
        self.material   = None  # what's it made of?
        
    #   values for creatures
        self.gender     = None
        self.job        = None  # what class/profession?
        self.faction    = None  # for diplomacy
        self.fov_map    = None  # libtcod fov_map object
        self.senseEvents= None
        self.purse      = None  # value of currency held
        self.ai         = None  # can remain None
        
    #   values for multiple types of things
        self.inv        = None  # inventory
        
    def __hash__(self):
        return self.id
    def __eq__(self,other):
        return id(self) == id(other) #(self.name==other.name)
    def __setattr__(self,attr,val):
        self.__dict__[attr]=val
        self.observers_notify(attr,val)
    
    @classmethod
    def get_new_id(cls):
        cls.new_id +=1
        return cls.new_id
    
    
    #def __repr__(self):         return self.name
        








            
#
#   Stats and Attributes
#
class Stats():  # Stats and attributes of a Thing
    
    def __init__(self,owner):
        self.owner      = owner
        self.mods       = {}    # temp stat modifiers - dict of dicts
            # - example stat mod: {100014 : {'dfn':4,'spd':-2}  }
            #                     { modID : {relevant modifiers}}
            # - modID is a globally unique identifier
            # - all mods are stackable using local function get()
        
            # Base stats
        self.sight      = 0
        self.hearing    = None
        self.nrg        = 0     # energy, capacity to do actions
        self.spd        = None  # energy restored per turn
        self.asp        = None  # attack speed; mods energy cost of attacking
        self.msp        = None  # move speed; mods energy cost of moving
        self.carry      = None  # carrying capacity
        self.atk        = None  # attack
        self.dmg        = None  # damage
        self.dfn        = None  # defense
        self.arm        = None  # armor
        self.hp         = 0     # current life
        self.hpmax      = 0     # maximum life
        self.mp         = 0     # current mana
        self.mpmax      = 0     # maximum mana
        self.resfire    = 0     # resist fire and heat
        self.resbio     = 0     # resist hazards (bio, chem, rads)
        self.reselec    = 0     # resist electricity
        self.temp       = 0     # temperature (fire damage)
        self.elec       = 0     # electricity (elec damage)
        self.rads       = 0     # radiation (rad damage)
        self.expo       = 0     # exposure (chem damage)
        self.sick       = 0     # sickness (bio damage)


    def __getitem__(self,key):      return self.__dict__[key]
    def __setitem__(self,key,val):  self.__dict__[key] = val
    def __setattr__(self,attr,val):
        self.__dict__[attr]=val
        self.owner.observers_notify()
    
    # calculated stats and attributes #
    # Add base stat with any active stat modifiers and return result.
    #
    def get(self,stat):
        total = getattr(self,stat)
        for mod in self.mods.values():
            if mod.get(stat): total += mod.get(stat)
        return total

    '''def quaff(self, obj):
        obj.stats.hp += 10
        rog.kill(self)
        remove from inventory
    '''
    




# Equip class:
# For nonliving things this represents where the item
# can be equipped. For living things this object
# holds a reference to (an item or None) for each slot.

class Equip():
    
    def __init__(self):
        self.head           = None
        self.back           = None
        self.body           = None
        self.mainHand       = None
        self.offHand        = None
        self.ammo           = None
        self.feet           = None
        self.jewelry        = []

    def __iter__(self):
        for var in vars(self):
            yield var
    

class _Event():
    def __init__(self, x,y, textSee, textHear, volume):
        self.x=x
        self.y=y
        self.textSee=textSee
        self.textHear=textHear
        self.volume=volume



# functions #

    # status effects #

newStatModID = 0

def effect_add(thing,mod):
    global newStatModID
    newStatModID +=1
    thing.stats.mods.update( {newStatModID : mod} )
    return newStatModID

def effect_remove(thing,modID):
    del thing.stats.mods[modID]

'''def set_fire(thing):
    rog.make(thing,FIRE)'''

def burn(thing):
    if rog.on(thing,WET):
        #rog.makenot(thing,FIRE)
        return False
    rog.hurt(thing,DMG_FIRE)
    return True

#create_creature
#this function does not set the individual monster stats
#it just creates a thing and gives it some default values
#   and initializes some stuff
def create_creature(name, typ, xs,ys, col):
    creat=Thing()
    creat.name          = name
    creat.type          = typ
    creat.mask          = typ
    creat.x             = xs
    creat.y             = ys
    creat.color         = col
    creat.material      = MAT_FLESH
    creat.isCreature    = True
    creat.inv           = []
    creat.fov_map=rog.fov_init()
    creat.path=rog.path_init_movement()
    return creat

def create_corpse(obj):
    corpse=Thing()
    corpse.name     = "corpse of {}".format(obj.name)
    corpse.type     = "%"
    corpse.mask     = corpse.type
    corpse.x        = obj.x
    corpse.y        = obj.y
    corpse.color    = obj.color
    corpse.material = obj.material
    corpse.stats.hp = int(obj.mass) + 1
    corpse.stats.resfire= obj.stats.resfire
    corpse.stats.resbio = obj.stats.resbio
    corpse.flags    = obj.flags
    return corpse

def create_ashes(obj):
    if obj.mass < 1: return
    ashes=Thing()
    ashes.name      = "ashes"
    ashes.type      = chr(247)
    ashes.mask      = ashes.type
    ashes.x         = obj.x
    ashes.y         = obj.y
    ashes.color     = COL['white']
    ashes.material  = MAT_DUST
    ashes.mass      = .5
    return ashes



















'''
def add_event(x,y, textSee, textHear, volume):
    pass
    new=_Event(x,y, textSee, textHear, volume)
    for obj in rog.list_creatures():
        obj.senseEvents.append(new)
    
        if textSee:
            if rog.can_see(obj, x,y):
                obj.seeEvents.append(textSee)
        elif volume:
            hearData=rog.can_hear(obj, x,y, volume)
            if hearData:
                obj.hearEvents.append((hearData,textHear,))'''
    
'''
def setAttributes(obj,stats):
    obj.stats.str    = stats[0]
    obj.stats.agi    = stats[1]
    obj.stats.dex    = stats[2]
    obj.stats.mnd    = stats[3]
    obj.stats.end    = stats[4]
    obj.stats.chr    = stats[5]'''



''' STATS LEVELING UP DEPENDENCY
        items = attr_mod.get(stat,None)
        if items:
            total += int( (1+self.lvl) * lvl_statMod *
                            self.__dict__[ items[0] ] * items[1] )
'''


'''
class Creature(Thing):

    def __init__(self,typ,xs,ys,col,name):
        super(Creature,self).__init__()

        self.name   = name
        self.type   = typ
        self.mask   = typ
        self.color  = col
        self.x      = xs
        self.y      = ys
        
        self.isCreature = True
        self.statMods   = {}
        self.flags      = set()
        self.inv        = []
        
    def __repr__(self):         super().__repr__()
    def __eq__(self,other):     super().__eq__(other)'''

'''
#
#   Stat Modifier Manager
#
class StatModManager():             CURRENTLY UNIMPLEMENTED
    
    data = []

    @classmethod
    def register(cls,modID,obj,timer):
        cls.data.append( [modID,obj,timer] )
    @classmethod
    def unregister(cls,modID):
        effect_remove( cls.data[modID][0], modID )
        del cls.data[modID]
    @classmethod
    def tick(cls):
        i=-1
        for mod in cls.data:
            i+=1
            modID   = mod[0]
            obj     = mod[1]
            timer   = mod[2] - 1
            if timer <= 0:
                cls.unregister(i)
            else:
                cls.register(modID,obj,timer) # overwrite entry w/ new data
'''
'''
def create_thing(ch,xs,ys):            CURRENTLY UNIMPLEMENTED
    new = Thing()
    new.mask    = ch
    new.type    = ch
    new.x       = xs
    new.y       = ys

    if ch==DOORCLOSED:
        new.name = "door"
        new.color = WHITE

    return new'''
        



'''

class Entity(Object):

    def __init__(self, *args):
        super().__init__(*args)

        #Actions.create_fovmap()
        
        for arg in args:
            name = type(arg).__name__
            # species
            if name == 'str':
                if self.species == '':
                    self.species = arg
            # faction
                elif self.faction == '':
                    self.faction = arg
        # end for
        
        self.dead = False
        
        self.ap = 0
        self.ap_regen = 0
        self.hp = 0
        self.hp_regen = 0
        self.mp = 0
        self.mp_regen = 0

        self.sight = 12
        self.hearing = 20

        self.skills = {}

    def __del__(self):
        print('entity deleted')

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            self.die()

    def calc_chance_to_hit(self, hit):
        pass

    def die(self):
        self.dead = True

        

    def do_look(self):
        self.compute_fovmap()
        #return Actions.look(self.sight, self.x, self.y)


    def can_see(self, x,y):
        return libtcod.map_is_in_fov(self.fovmap, x,y)



    def fovmap_create(self):
        self.fov_map = libtcod.map_new(GAME_WIDTH,GAME_HEIGHT)
    
    def fovmap_compute(self):
        libtcod.map_compute_fov( self.fovmap, self.x,self.y,self.sight,
                                light_walls = True,
                                 algo=libtcod.FOV_RESTRICTIVE)
        
    def fovmap_init(self):
    # Called after Map.create_fovmap()
    
        for xx in range( GAME_WIDTH):
            for yy in range( GAME_HEIGHT):
                
                libtcod.map_set_properties( self.fov_map, xx, yy,
                    (not self.get_blocks_sight(xx,yy)), True)
    
    def fovmap_update(self, x,y, value):
    # When something in the tile map changes,
    # This function must be called to update
    # The property of the changed tile.
    
        libtcod.map_set_properties( self.fov_map, xx, yy,
            value, True)



'''
