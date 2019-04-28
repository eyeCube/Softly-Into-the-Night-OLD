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
import dice




'''
HP_PERLVL   = 5
HP_PEREND   = 5
MP_PERMND   = 5
SPD_PERAGI  = 
'''






# obj class:
# In-game object; items, monsters, the player, etc.

class Thing(Observable):
    new_id = -1
    
    def __init__(self, x=None,y=None,z=0,_type=None,name=None,
                 color=None,material=None):
        super(Thing,self).__init__()

        if _type is not None:
            if type(_type) == int:
                _type = chr(_type) #ensure type is string
        
        self.id=Thing.get_new_id()
        
        self.name           = name  # unique or generic
        self.title          = "the "
        self.pronouns   = ("it","it","its",)
        self.color      = color  # drawing color
        self.bgcolor    = COL['black']
        self.flags      = set()
        self.skills     = {}
        self.equip      = Equip()
        self.stats      = Stats(self)
        self.statMods   = {}    # when equipped by someone else
        self.inv        = None  # inventory
        self.isSolid    = False # cannot be moved through if solid
        self.isCreature = False
        self.x          = x     # position in the game world
        self.y          = y
        self.z          = z
        self.type       = _type  # char represents type/species
        self.mask       = _type  # char displayed to screen
        self.mass       = 0         # KG
        self.material   = material  # what's it made of?
        self.nutrition  = None  # amount of hunger recovery
        
    #   values for creatures
        self.ai         = None
        self.mutations  = None  # number of mutations this obj has undergone
        self.gender     = None
        self.job        = None  # what class/profession?
        self.faction    = None  # for diplomacy
        self.fov_map    = None  # libtcod fov_map object
        self.senseEvents= None
        self.purse      = None  # value of currency held
        self.satiation  = None  # fullness / hunger tracker

    #   inanimate things
        self.ammoType   = None  # which type of ammo does it use?
        self.equipType  = None  # which slot can it be equipped in?
        
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
class Stats:  # Stats and attributes of a obj
    
    def __init__(self,owner):
        self.owner      = owner
        self.mods       = {}    # temp stat modifiers - dict of dicts
            # - example stat mod: {100014 : {'dfn':4,'spd':-2}  }
            #                     { modID : {relevant modifiers}}
            # - modID is a globally unique identifier
            # - all mods are stackable using local function get()
        
            # Base stats
        self.sight      = 0
        self.hearing    = 0
        self.range      = 0     # maximum range
        self.nrg        = 0     # energy, capacity to do actions
        self.spd        = 0     # energy restored per turn
        self.asp        = 0     # attack speed; mods energy cost of attacking
        self.msp        = 0     # move speed; mods energy cost of moving
        self.carry      = 0     # carrying capacity maximum
        self.atk        = 0     # attack
        self.dmg        = 0     # damage
        self.dfn        = 0     # defense
        self.arm        = 0     # armor
        self.hp         = 0     # current life
        self.hpmax      = 0     # maximum life
        self.mp         = 0     # current mana
        self.mpmax      = 0     # maximum mana
        self.element    = 0     # what type of damage does it deal?
        self.resfire    = 0     # resist fire and heat
        self.resbio     = 0     # resist hazards (bio, chem, rads)
        self.reselec    = 0     # resist electricity
        self.temp       = 0     # temperature (fire damage)
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
# holds a reference to a Slot object for each equip slot.
# Slot default data is an empty slot.
# Use Slot functions to interact with each individual Slot.
# NOTE: This is only a data storage object, and does not contain
#   functionality for equipping / dequipping items to creatures.
class Equip:
    
    def __init__(self):
        self.mainHand       = Slot()
        self.offHand        = Slot()
        self.head           = Slot()
        self.body           = Slot()
        self.back           = Slot()
        self.ammo           = Slot()
        #self.feet           = None
        #self.jewelry        = []

    def __iter__(self):
        for var in vars(self):
            yield var



# Slot class:
# equip slot for creatures' Equip object
#   -tracks item equipped in the slot as well as
#       the stat effect mod ID relating to that item
# NOTE: adding an item into this slot does not properly equip the item,
#   in and of itself. Functionality for equipping / dequipping
#       is handled elsewhere.
#   Before setting the slot data, a stat effect mod must be
#       generated and applied to the obj. The stat mod must be
#       cleared when the Slot is cleared.
class Slot:
    def __init__(self):
        self.item = None    #pointer to item that's equipped in this slot
        self.modID = None   #ID to the stat modifier this object uses
    #return whether the slot is empty
    def isEmpty(self):      return (self.item==None)
    def getItem(self):      return self.item
    def getModID(self):     return self.modID
    def setSlot(self,item,modID):
        self.item = item
        self.modID = modID
    # clear the slot of its item/mod, and return the item that was in the slot
    def clear(self):
        item=self.item
        self.item = None
        self.modID = None
        return item
    

class _Event:
    def __init__(self, x,y, textSee, textHear, volume):
        self.x=x
        self.y=y
        self.textSee=textSee
        self.textHear=textHear
        self.volume=volume



#-----------#
# functions #
#-----------#

    # Slot #
#relate equipType const to the name of the Slot objects in the Equip __dict__
def getSlotName(equipType):
    if equipType==EQ_MAINHAND:
        return "mainHand"
    elif equipType==EQ_OFFHAND:
        return "offHand"
    elif equipType==EQ_BODY:
        return "body"
    elif equipType==EQ_HEAD:
        return "head"
    elif equipType==EQ_BACK:
        return "back"

    # stat modifiers effects #

newStatModID = 0

def effect_add(obj,mod):
    global newStatModID
    newStatModID +=1
    obj.stats.mods.update( {newStatModID : mod} )
    return newStatModID

def effect_remove(obj,modID):
    del obj.stats.mods[modID]


    # elemental damage #
    # cause status effects

#fire damage
def burn(obj, dmg):
    #get obj resistance
    res = obj.stats.resfire
    if rog.on(obj, WET):    
        res += 50               #wet things have ++fire res
        rog.makenot(obj,WET)    #wet things get dried
    #increase temperature
    dmg = int( dmg*(1-(res/100)) )
    obj.stats.temp += max(0, dmg )
    obj.stats.temp = min(MAXTEMP, obj.stats.temp)
    #set burning status
    if (not rog.on(obj, FIRE) and obj.stats.temp >= BURNTEMP): #should depend on material?
        rog.set_status(obj, FIRE)
#reduce temperature
def cooldown(obj, amt):
    obj.stats.temp = max(0, obj.stats.temp - amt)
#bio damage
def disease(obj, dmg):
    res = obj.stats.resbio
    #increase sickness meter
    dmg = int( dmg*(1-(res/100)) )
    obj.stats.sick += max(0, dmg )
    if obj.stats.sick >= 100:
        obj.stats.sick = 0      #reset sickness meter
        rog.set_status(obj, SICK)
#rad damage
def irradiate(obj, dmg):
    res = obj.stats.resbio
    #increase rads meter
    dmg = int( dmg*(1-(res/100)) )
    obj.stats.rads += max(0, dmg )
    if obj.stats.rads >= 100:
        obj.stats.rads = 0 # reset rads meter after mutation
        rog.mutate(obj) 
#chem damage
def exposure(obj, dmg):
    res = obj.stats.resbio
    #increase exposure meter
    dmg = int( dmg*(1-(res/100)) )
    obj.stats.expo += max(0, dmg )
    if obj.stats.expo >= 100:
        obj.stats.expo = 0          #reset exposure meter
        rog.hurt(obj, CHEM_DAMAGE)  #instant damage when expo meter fills
        _random_chemical_effect(obj) #inflict chem status effect
#elec damage  
def electrify(obj, dmg):
    res = obj.stats.reselec
    dmg *= (1-(res/100))
    dmg /= 25
    dmg = 1+int(dmg)
    rog.sap(obj, dmg) # MP damage from lightning
    if dmg >= 2:
        rog.paralyze(obj, 1) # paralysis from high damage
    if dmg >= 4:
        rog.kill(obj) # insta-death from massive electric shock

def mutate(obj):
    if not obj.isCreature: return False
    obj.mutations += 1
    if obj.mutations > 3:
        rog.kill(obj)
    return True
def paralyze(obj, turns):
    if not obj.isCreature: return False
    rog.set_paral(obj, turns)
    return True



#functions for building objs

#these functions do not register the objects in the game world.
#just create the Thing and init some default values.

#create_creature
#this function does not set the individual monster stats
#it just creates a obj and gives it some default values / init stuff
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
    creat.mutations     = 0
    creat.gender        = dice.roll(2) - 1
    creat.fov_map       = rog.fov_init()
    creat.path          = rog.path_init_movement()
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
    corpse.stats.hpmax = int(obj.mass) + 1
    corpse.stats.resfire= obj.stats.resfire
    corpse.stats.resbio = obj.stats.resbio
    corpse.flags    = obj.flags
    rog.givehp(corpse)
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
    ashes.mass      = max(0.5, int(obj.mass/20))
    ashes.stats.resfire = 100
    ashes.stats.resbio  = 100
    ashes.stats.reselec = 100
    return ashes




#-----------------#
# LOCAL FUNCTIONS #
#-----------------#

#cause some random horrible chemical warfare effect
#   only for creatures
def _random_chemical_effect(obj):
    roll = dice.roll(6)
    if roll == 1:
        power = CHEM_BLIND_POWER
        if power >= res:
            duration = dice.roll(CHEM_BLIND_TIME)
            rog.set_status(obj, BLIND, duration)
    elif roll == 2:
        power = CHEM_PARAL_POWER
        if power >= res:
            duration = dice.roll(CHEM_PARAL_TIME)
            rog.set_status(obj, PARAL, duration)
    elif roll == 3:
        power = CHEM_COUGH_POWER
        if power >= res:
            duration = dice.roll(CHEM_COUGH_TIME)
            rog.set_status(obj, COUGH, duration)
    elif roll == 4:
        power = CHEM_VOMIT_POWER
        if power >= res:
            duration = dice.roll(CHEM_VOMIT_TIME)
            rog.set_status(obj, VOMIT, duration)
    elif roll == 5:
        power = CHEM_CONFU_POWER
        if power >= res:
            duration = dice.roll(CHEM_CONFU_TIME)
            rog.set_status(obj, CONFU, duration)
    elif roll == 6:
        power = CHEM_IRRIT_POWER
        if power >= res:
            duration = dice.roll(CHEM_IRRIT_TIME)
            rog.set_status(obj, IRRIT, duration)
       

















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
class Creature(obj):

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
def create_obj(ch,xs,ys):            CURRENTLY UNIMPLEMENTED
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
