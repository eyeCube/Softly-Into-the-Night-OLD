'''
rogue.py

the glue

'''


import libtcodpy as libtcod
import math

from const      import *
import orangio  as IO
import action
import debug
import dice
import fluids
import game
import items
import levels
import lights
import misc
import monsters
import managers
import maths
import player
import thing
import tilemap
from colors import COLORS as COL




IDENTIFIER = {
    ord(' ')        : "nothing",
    FLOOR           : "a cold stone floor",
    WALL            : "a rough stone wall",
    STAIRDOWN       : "a staircase leading down",
    STAIRUP         : "a staircase leading up",
    T_FOOD          : "some foodstuffs",
    T_STONE         : "a rock or stone",
    T_CORPSE        : "a corpse or skeleton",
    ord("?")        : "a silhouette or light",
    }
for k,v in monsters.bestiary.items():
    if isinstance(k, str):
        IDENTIFIER.update({ord(k) : v[0]})
    else:
        IDENTIFIER.update({k : v[0]})
def identify(t):
    return IDENTIFIER.get(t,"???")
        


def d_level(): return 1




#---------#
# classes #
#---------#


class Ref():        # stores global references to objects
    ctrl        = None  # global controller
    con         = None  # consoles
    data        = None
    Map         = None
    clock       = None
    update      = None
    settings    = None
    view        = None
    log         = None  # messages
    pc          = None
    environ     = None
    manager     = None  # current active game state manager
    savedGame   = None
    et_managers = {}    # per turn managers that tick at end of each turn
    bt_managers = {}    # per turn managers that tick at beginning of each turn
    c_managers  = {}    # const managers, ran manually
    


#------------------------------------#
#  some functions of global objects  #
#------------------------------------#

    # window
def create_window(w,h): Ref.window=game.Window(w,h)
def window_w():         return Ref.window.root.w
def window_h():         return Ref.window.root.h
def view_port_x():      return Ref.window.scene.x
def view_port_y():      return Ref.window.scene.y
def view_port_w():      return Ref.window.scene.w
def view_port_h():      return Ref.window.scene.h
def hud_x():            return Ref.window.hud.x
def hud_y():            return Ref.window.hud.y
def hud_w():            return Ref.window.hud.w
def hud_h():            return Ref.window.hud.h
def msgs_x():           return Ref.window.msgs.x
def msgs_y():           return Ref.window.msgs.y
def msgs_w():           return Ref.window.msgs.w
def msgs_h():           return Ref.window.msgs.h
def set_hud_left():     Ref.window.set_hud_left()
def set_hud_right():    Ref.window.set_hud_right()


    # controller
def create_controller():    Ref.control=game.Controller()
def end():                  Ref.control.end()
def game_state():           return Ref.control.state
def game_is_running():      return Ref.control.isRunning
def game_set_state(state="normal"):
    print("$---Game State changed from {} to {}".format(game_state(), state))
    Ref.control.set_state(state)
def game_resume_state():    return Ref.control.resume_state
def set_resume_state(state):Ref.control.set_resume_state(state)


    # console - init AFTER window init
def create_consoles():      Ref.con=game.Console(window_w(),window_h())
    # get global consoles for drawing to
def con_game():             return Ref.con.game
def con_final():            return Ref.con.final


    # update
def create_update():    Ref.update=game.Update()
def update_base():      Ref.update.base()
#def update_pcfov():     Ref.update.pcfov()
def update_game():      Ref.update.game()
def update_msg():       Ref.update.msg()
def update_hud():       Ref.update.hud()
def update_final():     Ref.update.final()
#apply all updates if applicable
def game_update():      Ref.update.update()


    # map
def create_map():
    Ref.Map=tilemap.TileMap(ROOMW,ROOMH)
    Ref.Map.init_specialGrids()
    Ref.Map.init_terrain()
def map():          return Ref.Map
def tile_get(x,y):          return Ref.Map.get_char(x,y)
def tile_change(x,y,char):
    updateNeeded=Ref.Map.tile_change(x,y,char)
    if updateNeeded:
        update_all_fovmaps()
def map_reset_lighting():   Ref.Map.grid_lighting_init()
def tile_lighten(x,y,value):Ref.Map.tile_lighten(x,y,value)
def tile_darken(x,y,value): Ref.Map.tile_darken(x,y,value)
def tile_set_light_value(x,y,value):Ref.Map.tile_set_light_value(x,y,value)
def get_light_value(x,y):   return Ref.Map.get_light_value(x,y)
def map_generate(Map,level): levels.generate(Map,level)
def identify_symbol_at(x,y):
    asci = libtcod.console_get_char(0, getx(x),gety(y))
    char = "{} ".format(chr(asci)) if (asci < 128 and not asci==32) else ""
    desc=IDENTIFIER.get(asci,"???")
    return "{}{}".format(char, desc)
def grid_remove(obj): #kill thing
    Ref.Map.remove_thing(obj)
def grid_insert(obj): #add thing
    Ref.Map.add_thing(obj)
def grid_lights_insert(obj):    Ref.Map.grid_lights[obj.x][obj.y].append(obj)
def grid_lights_remove(obj):    Ref.Map.grid_lights[obj.x][obj.y].remove(obj)
def grid_fluids_insert(obj):    Ref.Map.grid_fluids[obj.x][obj.y].append(obj)
def grid_fluids_remove(obj):    Ref.Map.grid_fluids[obj.x][obj.y].remove(obj)

    
    # view
def create_view():
    Ref.view=game.View( view_port_w(),view_port_h(), ROOMW,ROOMH)
def view_nudge(dx,dy):      Ref.view.nudge(dx,dy)
def view_nudge_towards(obj):Ref.view.follow(obj)
def view_center(obj):       Ref.view.center(obj.x, obj.y)
def view_center_player():   Ref.view.center(Ref.pc.x, Ref.pc.y)
def view_center_coords(x,y):Ref.view.center(x,y)
def view_x():       return  Ref.view.x
def view_y():       return  Ref.view.y
def view_w():       return  Ref.view.w
def view_h():       return  Ref.view.h
def view_max_x():   return  ROOMW - Ref.view.w #constraints on view panning
def view_max_y():   return  ROOMH - Ref.view.h
def fixedViewMode_toggle(): Ref.view.fixed_mode_toggle()


    # clock
def create_clock():     Ref.clock=game.Clock()
def turn_pass():        Ref.clock.turn_pass()
def get_turn():         return Ref.clock.turn


    # player
def create_player(sx,sy):
    pc = player.chargen()
    port(pc, sx,sy)
    player.init(pc)
    Ref.pc = pc
    return pc
def pc(): return Ref.pc


    # gamedata
def create_data():      Ref.data=game.GameData()
def dlvl():             return Ref.data.dlvl() #current dungeon level of player
# level up / down : functions change the player's dungeon level.
def level_up():         Ref.data.dlvl_update(Ref.data.dlvl() + 1)
def level_down():       Ref.data.dlvl_update(Ref.data.dlvl() - 1)


    # log
def create_log():       Ref.log=game.MessageLog()
def logNewEntry():      Ref.log.drawNew()
def msg(txt, col=None):
    if col is None: #default text color
        col=COL['white']
    Ref.log.add(txt, str(get_turn()) )
def msg_clear():
    clr=libtcod.console_new(msgs_w(), msgs_h())
    libtcod.console_blit(clr, 0,0, msgs_w(),msgs_h(),  con_game(), 0,0)
    libtcod.console_delete(clr)

# send message that may or may not be received by player.
# may include sight and sound info.
# volume is how many tiles away it can be heard with avg hearing
# 0 volume means no sound
'''def send(ev):
#   seeing
    if can_see(Ref.pc, ev.x,ev.y):
        if ev.textSee == "":
            return
        msg(ev.textSee)
        return
#   hearing
    if not ev.volume: return
    manager=Ref.c_managers['sounds']
    hearData=can_hear(Ref.pc, ev.x,ev.y, ev.volume)
    if hearData:
        xf,yf,vol=hearData
        manager.add(xf,yf, vol, ev.textHear)'''

def add_msgs_from_sounds():
    manager.run()


    # settings      
def settings():     return Ref.settings
def init_settings():
    Ref.settings=game.GlobalSettings()
    Ref.settings.read()
    Ref.settings.apply()
    return Ref.settings


    # saved game
def create_savedGame():
    Ref.savedGame=game.SavedGame()
    Ref.savedGame.loadSavedData()


    # environment
def create_environment():   Ref.environ=game.Environment()
def release_souls():        Ref.environ.release_souls()
def genocide(typ):
    for mon in list_creatures():
        if mon.type == typ:
            kill(mon)
    Ref.environ.genocide(typ)

    # constant managers, ran each turn
def create_perturn_managers():
    #end of turn (end of monster's turn)
    Ref.et_managers.update({'fire'      : managers.Manager_Fires()})
    Ref.et_managers.update({'fluids'    : managers.Manager_Fluids()})
    #beginning of turn (beginning of monster's turn)
    Ref.bt_managers.update({'timers'    : managers.Manager_Timers()})
    Ref.bt_managers.update({'status'    : managers.Manager_Status()})
    Ref.bt_managers.update({'meters'    : managers.Manager_Meters()})
    
    # constant managers, manually ran
def create_const_managers():
    Ref.c_managers.update({'fov'        : managers.Manager_FOV()})
    Ref.c_managers.update({'events'     : managers.Manager_Events()})
    Ref.c_managers.update({'sights'     : managers.Manager_SightsSeen()})
    Ref.c_managers.update({'sounds'     : managers.Manager_SoundsHeard()})




#------------------------#
# functions from modules #
#------------------------#

# orangio

def init_keyBindings():
    IO.init_keyBindings()


# game


'''
#
# func textbox
#
# display text box with border and word wrapping
#
    Args:
    x,y,w,h     location and size
    text        display string
    border      border style. None = No border
    wrap        whether to use automatic word wrapping
    margin      inside-the-box text padding on top and sides
    con         console on which to blit textbox, should never be 0
                    -1 (default) : draw to con_game()
    disp        display mode: 'poly','mono'

'''
def dbox(x,y,w,h,text='', wrap=True,border=0,margin=0,con=-1,disp='poly'):
    if con==-1: con=con_game()
    misc.dbox(x,y,w,h,text, wrap=wrap,border=border,margin=margin,con=con,disp=disp)
    
def makeConBox(w,h,text):
    con = libtcod.console_new(w,h)
    dbox(0,0, w,h, text, con=con, wrap=False,disp='mono')
    return con



# printing functions #

#@debug.printr
def refresh():  # final to root and flush
    libtcod.console_blit(con_final(), 0,0,window_w(),window_h(),  0, 0,0)
    libtcod.console_flush()
#@debug.printr
def render_gameArea(pc) :
    con = Ref.Map.render_gameArea(pc, view_x(),view_y(),view_w(),view_h() )
    #libtcod.console_clear(con_game())
    libtcod.console_clear(con_game())
    libtcod.console_blit(con, view_x(),view_y(),view_w(),view_h(),
                         con_game(), view_port_x(),view_port_y())
#@debug.printr
def render_hud(pc) :
    con = misc.render_hud(hud_w(),hud_h(), pc, get_turn(), d_level() )
    libtcod.console_blit(con,0,0,0,0, con_game(),hud_x(),hud_y())
#@debug.printr
def blit_to_final(con,xs,ys, xdest=0,ydest=0): # window-sized blit to final
    libtcod.console_blit(con, xs,ys,window_w(),window_h(),
                         con_final(), xdest,ydest)
#@debug.printr
def alert(text=""):    # message that doesn't go into history
    dbox(msgs_x(),msgs_y(),msgs_w(),msgs_h(),text,wrap=False,border=None,con=con_final())
    refresh()


#-------------#
# "Fun"ctions #
#-------------#

# tilemap
def thingat(x,y):       return Ref.Map.thingat(x,y) #Thing object
def thingsat(x,y):      return Ref.Map.thingsat(x,y) #list
def inanat(x,y):        return Ref.Map.inanat(x,y) #inanimate Thing at
def monat (x,y):        return Ref.Map.monat(x,y) #monster at
def solidat(x,y):       return Ref.Map.solidat(x,y) #solid Thing at
def wallat(x,y):        return (not Ref.Map.get_nrg_cost_enter(x,y) ) #tile wall
def fluidsat(x,y):      return Ref.et_managers['fluids'].fluidsat(x,y) #list
def lightsat(x,y):      return Ref.Map.lightsat(x,y) #list
def fireat(x,y):        return Ref.et_managers['fire'].fireat(x,y)

def cost_enter(x,y):    return Ref.Map.get_nrg_cost_enter(x,y)
def cost_leave(x,y):    return Ref.Map.get_nrg_cost_leave(x,y)
def cost_move(xf,yf,xt,yt,data):
    return Ref.Map.path_get_cost_movement(xf,yf,xt,yt,data)

def is_in_grid_x(x):    return (x>=0 and x<ROOMW)
def is_in_grid_y(y):    return (y>=0 and y<ROOMH)
def is_in_grid(x,y):    return (x>=0 and x<ROOMW and y>=0 and y<ROOMH)
def in_range(x1,y1,x2,y2,Range):    return (maths.dist(x1,y1, x2,y2) <= Range + .34)

# view
def getx(x):        return x + view_port_x() - view_x()
def gety(y):        return y + view_port_y() - view_y()
def mapx(x):        return x - view_port_x() + view_x()
def mapy(y):        return y - view_port_y() + view_y()

# terraforming
def dig(x,y):
    #dig a hole in the floor if no solids here
    #else dig the wall out
    #use rogue's tile_change func so we update all FOVmaps
    tile_change(x,y,FLOOR)
def singe(x,y): #burn tile
    if Ref.Map.get_char(x,y) == FUNGUS:
        tile_change(x,y,FLOOR)

# Thing functions
def is_creature(obj):   return obj.isCreature
def is_solid(obj):      return obj.isSolid
def make(obj,flag):     obj.flags.add(flag)
def makenot(obj,flag):  obj.flags.remove(flag)
def copyflags(toObj,fromObj): #use this to set an object's flags to that of another object.
    for flag in fromObj.flags:
        make(toObj, flag)
def has_equip(obj,item):return item in obj.equip
def on  (obj,flag):     return (flag in obj.flags)
def give(obj,item):
    if on(item,FIRE):
        burn(obj, FIREBURN)
        cooldown(item)
        obj.inv.add(item)
def take(obj,item):
    obj.inv.remove(item)
def mutate(obj):
    thing.mutate(obj)
    event_sight(obj.x,obj.y,"{t}{n} mutated!".format(t=obj.title,n=obj.name))
def has_sight(obj):
    if (obj.stats.get('sight') and not on(obj,BLIND)): return True
    return False
def port(obj,x,y): # move thing to absolute location, update grid and FOV
    grid_remove(obj)
    obj.x=x; obj.y=y;
    grid_insert(obj)
    update_fov(obj)
def drop(obj,item,dx=0,dy=0):
    take(obj,item)
    item.x=obj.x + dx
    item.y=obj.y + dy
    register_inanimate(item)
def givehp(obj,val=9999):   obj.stats.hp+=val; caphp(obj)
def givemp(obj,val=9999):   obj.stats.mp+=val; capmp(obj)
def caphp (obj):    obj.stats.hp=min(obj.stats.hp,obj.stats.get('hpmax'))
def capmp (obj):    obj.stats.mp=min(obj.stats.mp,obj.stats.get('mpmax'))
#train (improve) skill
def train (obj,skill):
    obj.skills.update({skill : max(SKILLMAX, obj.skills.get(skill,0)+1) })
#set stat
def setStat (obj,stat,val):
    setattr(obj.stats, stat, val)
#gain (improve) stat
def gain (obj,stat,val=1,Max=999):
    stats=obj.stats
    setattr(stats, stat, min(Max, getattr(stats, stat) + val))
#drain (damage) stat
def drain (obj,stat,val=1):
    old = getattr(obj.stats,stat)
    setattr(obj.stats,stat, old-val )
    if (stat=='hpmax'): caphp(obj)
    if (stat=='mpmax'): capmp(obj)
#damage hp
def hurt(obj, dmg):
    dmg = round(dmg)
    if dmg < 0: return
    obj.stats.hp -= dmg
    if obj.stats.hp <= 0:
        kill(obj)
#damage mp
def sap(obj, dmg):
    dmg = round(dmg)
    obj.stats.mp -= dmg
    if obj.stats.mp <= 0:
        zombify(obj)
#deal fire damage
def burn(obj, dmg):
    if on(obj,WET):
        makenot(obj, WET)
        #steam=create_fluid(obj.x, obj.y, "steam")
        return False
    thing.burn(obj, dmg)
    return True
def cooldown(obj, temp=999):
    thing.cooldown(obj, temp)
#deal bio damage
def disease(obj, dmg): thing.disease(obj, dmg)
#deal chem damage
def exposure(obj, dmg): thing.exposure(obj, dmg)
#deal rad damage
def irradiate(obj, dmg): thing.irradiate(obj, dmg)
#deal electric damage
def electrify(obj, dmg): thing.electrify(obj, dmg)
#paralyze
def paralyze(obj, turns): thing.paralyze(obj, turns)
#cough
def cough(obj, dmg): thing.cough(obj, dmg)
#mutate
def mutate(obj): thing.mutate(obj)
def kill(obj): #remove a thing from the world
    if on(obj,DEAD): return
    make(obj,DEAD)
    #drop inventory
    if obj.inv:
        for tt in obj.inv:
            drop(obj, tt)
    #creatures
    if obj.isCreature:
        #create a corpse
        if dice.roll(100) < monsters.corpse_recurrence_percent[obj.type]:
            create_corpse(obj)
    #inanimate things
    else:
        #burn to ashes
        if on(obj,FIRE):
            if (obj.material==MAT_FLESH
                or obj.material==MAT_WOOD
                or obj.material==MAT_FUNGUS
                or obj.material==MAT_VEGGIE
                or obj.material==MAT_LEATHER
                ):
                create_ashes(obj)
    #remove dead thing
    clear_status_all(obj)
    if on(obj,ONGRID):
        if obj.isCreature:
            Ref.environ.kill(obj)
        else:
            release_inanimate(obj)



#----------------------#
#        Events        #
#----------------------#

def event_sight(x,y,text):
    if not text: return
    Ref.c_managers['events'].add_sight(x,y,text)
def event_sound(x,y,data):
    if (not data): return
    volume,text=data
    Ref.c_managers['events'].add_sound(x,y,text,volume)
def listen_sights(obj):     return  Ref.c_managers['events'].get_sights(obj)
def listen_sounds(obj):     return  Ref.c_managers['events'].get_sounds(obj)
def add_listener_sights(obj):       Ref.c_managers['events'].add_listener_sights(obj)
def add_listener_sounds(obj):       Ref.c_managers['events'].add_listener_sounds(obj)
def remove_listener_sights(obj):    Ref.c_managers['events'].remove_listener_sights(obj)
def remove_listener_sounds(obj):    Ref.c_managers['events'].remove_listener_sounds(obj)
def clear_listen_events_sights(obj):Ref.c_managers['events'].clear_sights(obj)
def clear_listen_events_sounds(obj):Ref.c_managers['events'].clear_sounds(obj)

def pc_listen_sights():
    pc=Ref.pc
    lis=listen_sights(pc)
    if lis:
        for ev in lis:
            Ref.c_managers['sights'].add(ev)
        manager_sights_run()
def pc_listen_sounds():
    pc=Ref.pc
    lis=listen_sounds(pc)
    if lis:
        for ev in lis:
            Ref.c_managers['sounds'].add(ev)
        manager_sounds_run()
def clear_listeners():      Ref.c_managers['events'].clear()


#------------------------#
# Stats Functions + vars #
#------------------------#

def effect_add(obj,mod):        # Stat mod create
    effID=thing.effect_add(obj,mod)
    return effID
def effect_remove(obj,modID):   # Stat mod delete
    thing.effect_remove(obj,modID)



#---------------#
#     Lists     #
#---------------#

class Lists():
    creatures   =[]     # living things
    inanimates  =[]     # nonliving
    lights      =[]
    fluids      =[]
    
    @classmethod
    def things(cls):
        lis1=set(cls.creatures)
        lis2=set(cls.inanimates)
        return lis1.union(lis2)

# lists functions #

def list_creatures():           return Lists.creatures
def list_inanimates():          return Lists.inanimates
def list_things():              return Lists.things()
def list_lights():              return Lists.lights
def list_fluids():              return Lists.fluids
def list_add_creature(obj):     Lists.creatures.append(obj)
def list_remove_creature(obj):  Lists.creatures.remove(obj)
def list_add_inanimate(obj):    Lists.inanimates.append(obj)
def list_remove_inanimate(obj): Lists.inanimates.remove(obj)
def list_add_light(obj):        Lists.lights.append(obj)
def list_remove_light(obj):     Lists.lights.remove(obj)
def list_add_fluid(obj):        Lists.fluids.append(obj)
def list_remove_fluid(obj):     Lists.fluids.remove(obj)




#----------------#
#       FOV      #
#----------------#

#THIS CODE NEEDS TO BE UPDATED. ONLY MAKE AS MANY FOVMAPS AS NEEDED.
def fov_init():  # normal type FOV map init
    fovMap=libtcod.map_new(ROOMW,ROOMH)
    libtcod.map_copy(Ref.Map.fov_map,fovMap)  # get properties from Map
    return fovMap
#@debug.printr
def fov_compute(obj):
    libtcod.map_compute_fov(
        obj.fov_map, obj.x,obj.y, obj.stats.get('sight'),
        light_walls = True, algo=libtcod.FOV_RESTRICTIVE)
def update_fovmap_property(fovmap, x,y, value): libtcod.map_set_properties( fovmap, x,y,value,True)
def compute_fovs():     Ref.c_managers['fov'].run()
def update_fov(obj):    Ref.c_managers['fov'].add(obj)
# circular FOV function
def can_see(obj,x,y):
    if (get_light_value(x,y) == 0 and not on(obj,NVISION)):
        return False
    return ( in_range(obj.x,obj.y, x,y, obj.stats.get('sight')) #<- circle-ize
             and libtcod.map_is_in_fov(obj.fov_map,x,y) )
#copies Map 's fov data to all creatures - only do this when needed
#   also flag all creatures for updating their fov maps
def update_all_fovmaps():
    for creat in list_creatures():
        if has_sight(creat):
            fovMap=creat.fov_map
            libtcod.map_copy(Ref.Map.fov_map,fovMap)
            update_fov(tt)
#******maybe we should overhaul this FOV system!~*************
        #creatures share fov_maps. There are a few fov_maps
        #which have different properties like x-ray vision, etc.
        #the only fov_maps we have should all be unique. Would save time.
        #update_all_fovmaps only updates these unique maps.
        #this would probably be much better, I should do this for sure.



#----------------#
#      Paths     #
#----------------#

def can_hear(obj, x,y, volume):
    if not obj.stats.get('hearing'): return False
    dist=maths.dist(obj.x, obj.y, x, y)
    maxHearDist=volume*obj.stats.get('hearing')/AVG_HEARING
    if (obj.x == x and obj.y == y): return (0,0,maxHearDist,)
    if dist > maxHearDist: return False
    # calculate a path
    path=path_init_sound()
    path_compute(path, obj.x,obj.y, x,y)
    pathSize=libtcod.path_size(path)
    if dist >= 2:
        semifinal=libtcod.path_get(path, 0)
        xf,yf=semifinal
        dx=xf - obj.x
        dy=yf - obj.y
    else:
        dx=0
        dy=0
    path_destroy(path)
    loudness=(maxHearDist - pathSize - (pathSize - dist))
    if loudness > 0:
        return (dx,dy,loudness)

def path_init_movement():
    pathData=0
    return Ref.Map.path_new_movement(pathData)
def path_init_sound():
    pathData=0
    return Ref.Map.path_new_sound(pathData)
def path_destroy(path):     libtcod.path_delete(path)
def path_compute(path, xfrom,yfrom, xto,yto):
    libtcod.path_compute(path, xfrom,yfrom, xto,yto)
def path_step(path):
    x,y=libtcod.path_walk(path, True)
    return x,y



#----------------#
#     Things     #
#----------------#

def create_stuff(ID, x,y):
    tt = stuff.create(x,y, ID)
    register_inanimate(tt)
    return tt
def release_thing(obj):
    grid_remove(obj)
def register_inanimate(obj):
    print("registering {} at {},{}".format(obj.name,obj.x,obj.y))
    make(obj,ONGRID)
    grid_insert(obj)
    list_add_inanimate(obj)
def release_inanimate(obj):
    makenot(obj,ONGRID)
    grid_remove(obj)
    list_remove_inanimate(obj)



#---------------#
#   Inventory   #
#---------------#

def init_inventory(obj, capacity):
    obj.inv=items.Inventory(capacity)



#------------#
#   Fluids   #
#------------#

def create_fluid(x,y,name):
    fluid = fluids.create_fluid(x,y,name)
    register_fluid(fluid)
'''def port_fluid(fluid, xto, yto):
    grid_fluids_remove(fluid)
    fluid.x=xto
    fluid.y=yto
    grid_fluids_insert(fluid)
def flow_fluid(fluid, xto, yto, amt): #fluids should be object instances?
    grid_fluids_remove(fluid)
    fluid.x=xto
    fluid.y=yto
    grid_fluids_insert(fluid)'''
def register_fluid(obj):
    grid_fluids_insert(obj)
    list_add_fluid(obj)
def release_fluid(obj):
    grid_fluids_remove(obj)
    list_remove_fluid(obj)
    
#fluid containers
def init_fluidContainer(obj, size):
    make(obj,HOLDSFLUID)
    obj.fluidContainer = fluids.FluidContainer(size)



#---------------#
#   Equipment   #
#---------------#

#equipping things
def equip(obj,item,equipType): # equip an item in 'equipType' slot
    slotName = thing.getSlotName(equipType)
    slot = obj.equip.__dict__[slotName]
    if not on(item,CANEQUIP): #can't be equipped
        return None
    if not item.equipType == equipType: #can't be wielded in mainhand
        return None
    if not slot.isEmpty(): #already wielding something
        return None
    #add special effects; light, etc.
    #add stat effects
    effID = effect_add(obj,item.statMods)
    #put item in slot
    slot.setSlot(item, effID)
    return effID
def deequip(obj,equipType): # remove equipment from slot 'equipType'
    slotName = thing.getSlotName(equipType)
    slot = obj.equip.__dict__[slotName]
    if slot.isEmpty(): #nothing equipped here
        return None
    #remove any special effects; light, etc.
    #remove stat effects
    effect_remove(obj, slot.getModID() )
    #remove item from slot
    item = slot.clear()
    return item

# build equipment and place in the world
def create_weapon(name,x,y):
    weap=gear.create_weapon(name,x,y)
    register_inanimate(weap)
    return weap
def create_gear(name,x,y):
    obj=gear.create_gear(name,x,y)
    register_inanimate(obj)
    return obj



#---------------------#
#  creature/monsters  #
#---------------------#

#register and release functions do not perform checks to ensure proper calling
#must ensure manually that you insert an object of type Thing
#if a creature already exists in the tile of obj's position,
#   then this function will produce errors.
#likewise make sure you do not try to release an entity
#   that was not first registered.
#Always call proper release that corresponds with the register function
#   in order to remove an object from the game.
def register_creature(obj):
    make(obj,ONGRID)
    grid_insert(obj)
    list_add_creature(obj)
def release_creature(obj):
    makenot(obj,ONGRID)
    release_thing(obj)
    list_remove_creature(obj)
    remove_listener_sights(obj)
    remove_listener_sounds(obj)
#call this to create a monster from the bestiary
def create_monster(typ,x,y,col,mutate=3): #init from monsters.py
    if monat(x,y):
        return None #tile is occupied by a creature already.
    monst = monsters.create_monster(typ,x,y,col,mutate)
    init_inventory(monst, monst.stats.carry)
    givehp(monst)
    register_creature(monst)
    return monst 
#call this to build a creature from scratch, not using monsters.py
#call create_monster instead if you want to use a template from the bestiary
#this function does not initialize all creature parameters
def create_creature(name, typ, x,y, col): #init basic creature stuff
    if monat(x,y):
        return None #tile is occupied by a creature already.
    creat = thing.create_creature(name,typ,x,y,col)
    register_creature(creat)
    return creat
def create_corpse(obj):
    corpse = thing.create_corpse(obj)
    register_inanimate(corpse)
    return corpse
def create_ashes(obj):
    ashes = thing.create_ashes(obj)
    register_inanimate(ashes)
    return ashes


#-------------#
# occupations #
#-------------#

def playableJobs(): return Ref.savedGame.playableJobs
def occupations(obj): return action.occupations.get(obj, None)
def occupations_elapse_turn(obj):
    tLeft,helpless,fxn,args=action.occupations[obj]
    action.occupations.update({ obj : (fxn,args,tLeft - 1,helpless,) })
def occupation_add(obj,turns,helpless,fxn,args):
    action.occupations.update({ obj : (fxn,args,turns,helpless,) })
def occupation_remove(obj):     del action.occupations[obj]


#----------------#
#    lights      #
#----------------#

def create_light(x,y, value, owner=None):
    light=lights.Light(x,y, value, owner)
    light.fov_map=fov_init()
    register_light(light)
    if owner:   #light follows owner if applicable
        owner.observer_add(light)
    return light

def register_light(light):
    light.shine()
    grid_lights_insert(light)
    list_add_light(light)
def release_light(light):
    light.unshine()
    if light.owner:
        light.owner.observer_remove(light)
    grid_lights_remove(light)
    list_remove_light(light)



#-------------#
#   fires     #
#-------------#

#fire tile flag is independent of the status effect of burning
def set_fire(x,y):
    Ref.et_managers['fire'].add(x,y)
def douse(x,y): #put out a fire at a tile and cool down all things there
    if not Ref.et_managers['fire'].fireat(x,y): return
    Ref.et_managers['fire'].remove(x,y)
    for tt in thingsat(x,y):
        Ref.bt_managers['status'].remove(tt, FIRE)
        cooldown(tt)


#----------------#
#    status      #
#----------------#

#Status for being on fire separate from the fire entity and light entity.

#set status effect
    # obj       = Thing object to set the status for
    # status    = ID of the status effect
    # t         = duration (-1 is the default duration for that status)
def set_status(obj, status, t=-1):
    Ref.bt_managers['status'].add(obj, status, t)
def clear_status(obj, status):
    Ref.bt_managers['status'].remove(obj, status)
def clear_status_all(obj):
    Ref.bt_managers['status'].remove_all(obj)



#----------#
# managers #
#----------#

def managers_beginturn_run():
    for v in Ref.bt_managers.values():
        v.run()
def managers_endturn_run():
    for v in Ref.et_managers.values():
        v.run()
def manager_sights_run():   Ref.c_managers['sights'].run()
def manager_sounds_run():   Ref.c_managers['sounds'].run()

# constant managers #

def register_timer(obj):    Ref.bt_managers['timers'].add(obj)
def release_timer(obj):     Ref.bt_managers['timers'].remove(obj)

# game state managers #

def get_active_manager():       return Ref.manager
def close_active_manager():
    if Ref.manager:
        Ref.manager.close()
        Ref.manager=None
def clear_active_manager():
    if Ref.manager:
        Ref.manager.set_result('exit')
        close_active_manager()

def routine_look(xs, ys):
    clear_active_manager()
    game_set_state("look")
    Ref.manager=managers.Manager_Look(
        xs, ys, Ref.view, Ref.Map.get_map_state())
    alert("Look where? (<hjklyubn>, mouse; <select> to confirm)")
    Ref.view.fixed_mode_disable()

def routine_move_view():
    clear_active_manager()
    game_set_state("move view")
    Ref.manager=managers.Manager_MoveView(
        Ref.view, Ref.Map.get_map_state())
    alert("Direction? (<hjklyubn>; <select> to center view)")
    Ref.view.fixed_mode_disable()

def routine_print_msgHistory():
    clear_active_manager()
    game_set_state("message history")
    width   = window_w()
    height  = window_h()
    strng   = Ref.log.printall_get_wrapped_msgs()
    nlines  = 1 + strng.count('\n')
    hud1h   = 3
    hud2h   = 3
    scroll  = makeConBox(width,1000,strng)
    top     = makeConBox(width,hud1h,"Message History:")
    bottom  = makeConBox(width,hud2h,"<Up>, <Down>, <PgUp>, <PgDn>, <Home>, <End>; <select> to return")
    Ref.manager = managers.Manager_PrintScroll( scroll,width,height, top,bottom, h1=hud1h,h2=hud2h,maxy=nlines)

def Input(x,y, w=1,h=1, default='',mode='text',insert=False):
    return IO.Input(x,y,w=w,h=h,default=default,mode=mode,insert=insert)

#prompt
# show a message and ask the player for input
# mode: 'text' or 'wait'
def prompt(x,y, w,h, maxw=1, q='', default='',mode='text',insert=False,border=0):
    #libtcod.console_clear(con_final())
    dbox(x,y,w,h,text=q,
        wrap=True,border=border,con=con_final(),disp='mono')
    result=""
    while (result==""):
        refresh()
        if mode=="wait":
            xf=x+w-1
            yf=y+h-1
        elif mode=="text":
            xf=x
            yf=y+h
        result = Input(xf,yf,maxw,1,default=default,mode=mode,insert=insert)
    return result

#menu
#this menu freezes time until input given.
#keysItems can be an iterable or a dict.
    #If a dict, autoItemize must be set to False
#autoItemize: create keys for your items automagically
def menu(name, x,y, keysItems, autoItemize=True):
    manager=managers.Manager_Menu(name, x,y, window_w(),window_h(), keysItems=keysItems, autoItemize=autoItemize)
    result=None
    while result is None:
        manager.run()
        result=manager.result
    manager.close()
    if result == ' ': return None
    return manager.result
    
    
#




















'''
    ##TESTING a* A star path
    while not libtcod.path_is_empty(path):
        x,y=path_step(path)
        if x is None:
            print('A* stuck')
            break
        libtcod.console_set_char_background(con_final(), getx(x),gety(y), COL['white'])
'''
'''
def msg_printall():
        # init manager
    width   = window_w()
    strng   = Ref.log.printall_get_wrapped_msgs()
    nlines  = 1 +strng.count('\n')
    hud1h   = 3
    hud2h   = 4
    scroll  = makeConBox(width,1000,strng)
    top     = makeConBox(width,hud1h,"Message History:")
    bottom  = makeConBox(width,hud2h,'....')
        # execute manager
    manager = managers.Manager_PrintScroll( scroll,top,bottom, h1=hud1h,h2=hud2h,maxy=nlines)
    
    while not manager.result:
        manager.run()
    manager.close()
#'''


'''def get_exp_req(level):     # experience required to level up at a certain level
    return (level+1)*20

def level(monst):           # level up
    monst.stats.lvl     += 1
    monst.stats.atk     += 1
    monst.stats.dfn     += 1
    monst.stats.dmg     += 1
    monst.stats.hpmax   += HP_PER
    monst.stats.mpmax   += MP_PER

def award_exp(monst,exp):
    monlv = monst.stats.lvl
    monst.stats.exp += max(0, exp - monlv)
    expreq = get_exp_req(monlv)
    if monst.stats.exp >= expreq:
        monst.exp -= expreq
        level(monst)
'''



'''from gamedata
room = [[]]    # Lists of saved room data
field = []     # List of objects in the current room


def room_save(index) :
    room[index] = []
    for obj in self.field:
        self.room[index].append(obj)


def room_load(self, index) :
    self.field = []
    for obj in self.room[index]:
        self.field.append(obj)


def create_map(self, width, height) :
    self.map = map_new(width, height)
'''

    


# Skills
# might not use any skills at all
'''
i = 1
AXES        = i; i+=1;  # 
BLADES      = i; i+=1;  # swords and knives, shortblades
BLUNT       = i; i+=1;  # all blunt weapons, flails and quarterstaffs
MARKSMAN    = i; i+=1;  # bows, throwing, other ranged attacks
MEDS        = i; i+=1;  # medicine
REPAIR      = i; i+=1;  # repair armor, weapons,
SPEECH      = i; i+=1;  # and barter
SPELLS      = i; i+=1;  # spellcasting
STEALTH     = i; i+=1;  # 
TRAPS       = i; i+=1;  # find, set, and create traps

STATMODS_WRESTLING  ={'atk':4,'dfn':2,'dmg':1,'nrg':-3}
STATMODS_SWORDS     ={'atk':2,'dfn':2,'dmg':2,'nrg':-2}
STATMODS_DAGGERS    ={'atk':2,'dfn':2,'dmg':2,'nrg':-3}
STATMODS_AXES       ={'atk':2,'dmg':2,'nrg':-2}
STATMODS_CUDGELS    ={'atk':2,'dmg':2,'nrg':-2}
'''

'''
    con_box0 = Ref.log.printall_make_box0(width,strng)
    con_box1 = Ref.log.printall_make_box1(width,box1h)
    con_box2 = Ref.log.printall_make_box2(width,box2h)
    
    manager = managers.PrintScrollManager(con_box0,con_box1,con_box2)
    while True:
        reply=manager.run()
        if (reply==' ' or reply==chr(K_ESCAPE) or reply==chr(K_ENTER)):
            break
    
    width = window_w()
    height = window_h()
    box1h = 3
    box2h = 4
    box2y = window_h()-box2h
    strng = Ref.log.printall_get_wrapped_msgs()
    
    scrollspd       = 1
    pagescroll      = height -(box1h+box2h+2)
    maxy            = 1 + strng.count('\n')
    y = 0
    while True:
        blit_to_final(con_box0,0,y,0,box1h)
        blit_to_final(con_box1,0,0,0,0)
        blit_to_final(con_box2,0,0,0,box2y)
        refresh()
        
        reply=IO.Input(width-5,height-1,w=4,mode="wait",default="...")
        if   reply==chr(K_UP):       y = max(0,      y-scrollspd)
        elif reply==chr(K_DOWN):     y = min(maxy,   y+scrollspd)
        elif reply==chr(K_PAGEUP):   y = max(0,      y-int(pagescroll))
        elif reply==chr(K_PAGEDOWN): y = min(maxy,   y+int(pagescroll))
        elif reply==chr(K_HOME):     y = 0
        elif reply==chr(K_END):      y = max(0,      maxy-pagescroll)
        elif (reply==' ' or reply==chr(K_ESCAPE) or reply==chr(K_ENTER)):
            break
    
    update_final() # refresh screen when done
    libtcod.console_delete(con_box0)
    libtcod.console_delete(con_box1)
    libtcod.console_delete(con_box2)
'''

'''
def shield(obj,item): # equip an item in the offhand
    if not on(item,CANEQUIP): #can't be equipped
        return None
    if not item.equipType == EQ_OFFHAND: #can't be wielded in mainhand
        return None
    if not obj.equip.offHand.isEmpty(): #already wielding something
        return None 
    effID = effect_add(obj,item.statMods)
    obj.equip.offHand.setSlot(item, effID)
    return effID
def wearBody(obj,item): # put on body armor
    if not on(item,CANEQUIP): #can't be equipped
        return None
    if not item.equipType == EQ_BODY: #can't be worn on body
        return None
    if not obj.equip.body.isEmpty(): #already wearing something on body
        return None 
    effID = effect_add(obj,item.statMods)
    obj.equip.body.setSlot(item, effID)
    return effID'''


