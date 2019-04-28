#
# some various managers
# and parent manager objects
#

import libtcodpy as libtcod
import time
import math

from const      import *
from manager    import Manager
import rogue    as rog
import orangio  as IO
import maths
import misc
import dice







class GameStateManager(Manager):
    
    def __init__(self):
        super(GameStateManager,self).__init__()
        self._resume_game_state="normal"
    def close(self):
        super(GameStateManager,self).close()
        self.resume_game_state()
    def set_resume_state(self,new): self._resume_game_state=new
    def resume_game_state(self): rog.game_set_state(self._resume_game_state)
#





#-------------------#
# specific managers #
#-------------------#


#
# Timers
#

class Manager_Timers(Manager):

    def __init__(self):
        super(Manager_Timers, self).__init__()

        self.data=[]

    def run(self):
        super(Manager_Timers, self).run()
        
        for datum in self.data:
            datum.tick()
            
    def close(self):
        super(Manager_Timers, self).close()
        
        pass

    def add(self,obj):
        self.data.append(obj)
    def remove(self,obj):
        self.data.remove(obj)



#
# Status Meters
#
    #Status Meters are the build-up counters for status effects like fire, sickness, etc.
        
class Manager_Meters(Manager):

    def __init__(self):
        super(Manager_Meters, self).__init__()

        pass

    def run(self):
        super(Manager_Meters, self).run()

        for thing in rog.list_things():
            #print(thing.name," is getting cooled down") #TESTING
            # cool down temperature meter if not currently burning
            if (thing.stats.temp > 0 and not rog.on(thing,FIRE)):
                thing.stats.temp -= 1
            # sickness meter
            if (thing.stats.sick > 0):
                thing.stats.sick -= 1
            # exposure meter
            if (thing.stats.expo > 0):
                thing.stats.expo -= 1
            # rads meter
            #if (thing.stats.rads > 0):
            #    thing.stats.rads -= 1
        

    def close(self):
        super(Manager_Meters, self).close()
        
        pass



#
# Fires
#
    #manager for fires
    # also controls light from fire, fire spreading,
    #   messages from fires, putting out fires
    # does not control burning status effect

    #OVERHAUL FIRE SYSTEM:
    #Fire should exist on tiles and feed from the
    #fuel that's burning on that tile.
    # If an object burns to ashes, the fire in that tile is put out
    #   by this manager when it tries to spread/consume but
    #   realizes that there is no more fuel in the tile it's on.
class Manager_Fires(Manager):

    def __init__(self):
        super(Manager_Fires, self).__init__()

        self.fires={}
        self.lights={}

    def run(self):
        super(Manager_Fires, self).run()

        removeList=[]
        for x,y in self.fires:
            _fluids = rog.fluidsat(x,y)
            _things = rog.thingsat(x,y)
            _exit=False

            #tiles that put out fires or feed fires
            '''
            wet floor flag


            '''

            #fluids that put out fires or feed fires
            '''for flud in _fluids:
                if flud.extinguish:
                    self.remove(x,y)
                    _exit=True
                    continue
                if flud.flammable:
                    self.fire_spread(x,y)
                    continue
                    '''

            if _exit: continue

            #check for no fuel condition
            if not _things: 
                removeList.append((x,y,))
                continue

            #BURN THINGS ALIVE (or dead)
            food=0  #amount of fuel gained by the fire
            for obj in _things: #things that might fuel the fire
                textSee=""
                canBurn=False
                if rog.burn(obj, FIREBURN):
                    canBurn=True
                if canBurn: #burn it
                    if obj.material == MAT_WOOD:
                        rog.event_sound(x,y, SND_FIRE)
                        food += 10
                    elif obj.material == MAT_FLESH:
                        food += 2
                    elif obj.material == MAT_VEGGIE:
                        food += 3
                    elif obj.material == MAT_SAWDUST:
                        food += 50
                    elif obj.material == MAT_PAPER:
                        food += 50
                    elif obj.material == MAT_CLOTH:
                        food += 20
                    elif obj.material == MAT_LEATHER:
                        food += 1
                    elif obj.material == MAT_FUNGUS:
                        food += 1
                    elif obj.material == MAT_PLASTIC:
                        food += 1
                if not obj.isCreature:
                    if rog.on(obj,DEAD):
                        textSee="{t}{n} is destroyed by fire.".format(
                            t=obj.title,n=obj.name)
                        rog.event_sight(x,y, textSee)
                        continue
                    #else: textSee=""
                #else:
                    #textSee="{t}{n} burns.".format(t=obj.title,n=obj.name)
                rog.event_sight(x,y, textSee)
            #end for (things)

            if food < 5:
                if dice.roll(food) == 1:
                    removeList.append((x,y,))
            else:
                if food >= 10:
                    iterations = 1+int((food - 10)/3)
                    self.fire_spread(x,y,iterations)
                    
        #end for (fires)
                    
        for xx,yy in removeList:
            self.remove(xx,yy)
                    
    #end def
            
    def close(self):
        super(Manager_Fires, self).close()
        
        pass

    def fireat(self, x,y):  return self.fires.get((x,y,), False)
    def fires(self):        return self.fires.keys()

    # set a tile on fire
    def add(self, x,y):
        if self.fireat(x,y): return
        self.fires.update({ (x,y,) : True })
        light=rog.create_light(x,y, 10, owner=None)
        self.lights.update({(x,y,) : light})
        
        #obj.observer_add(light)
        #self.lights.update({obj : light})
        
    # remove a fire from a tile
    def remove(self, x,y):
        if not self.fireat(x,y): return
        del self.fires[(x,y,)]
        light=self.lights[(x,y,)]
        rog.release_light(light)
        obj=rog.thingat(x,y)
        '''if obj:
            textSee="The fire on {n} is extinguished.".format(n=obj.name)
            rog.event_sight(obj.x,obj.y, textSee)
            #rog.event_sound(obj.x,obj.y, SND_DOUSE)'''

    # look nearby a burning tile to try and set other stuff on fire
    def fire_spread(self, xo, yo, iterations):
        #heat=FIREBURN #could vary based on what's burning here, etc...
        for ii in range(iterations):
            index = dice.roll(8) - 1
            x,y = DIRECTION_FROM_INT[index]
            fuel=rog.thingat(xo + x, yo + y)
            if fuel:
                self.add(xo + x, yo + y)



#
# Status
#
    #manager for all status effects
class Manager_Status(Manager):
    #default durations for statuses
    DURATIONS = {
        FIRE    : 99999,
        SICK    : 500,
        ACID    : 25,
        IRRIT   : 200,
        PARAL   : 5,
        COUGH   : 20,
        VOMIT   : 50,
        BLIND   : 100,
        DEAF    : 100,
        }

    def __init__(self):
        super(Manager_Status, self).__init__()

        self.statuses={
            #example:
            #SICK   : {obj1:DURATION,},
            FIRE    : {},
            SICK    : {},
            IRRIT   : {},
            PARAL   : {},
            COUGH   : {},
            VOMIT   : {},
            BLIND   : {},
            DEAF    : {},
            }
        

    def add(self, obj, status, dur=-1):
        #don't let it overwrite a status effect with a lesser duration...!
        if dur == -1: #default duration
            dur = Manager_Status.DURATIONS[status]
        self.statuses[status].update({obj:dur})
        rog.make(obj, status) #add flag
    def remove(self, obj, status):
        if obj in self.statuses[status]:
            del self.statuses[status][obj]
            rog.makenot(obj, status) #remove flag

    def run(self):
        super(Manager_Status, self).run()

        #iterate through only the things that have status effects,
        #   and do those effects
        for status,dic in self.statuses.items():
            for obj, dur in dic.items():
                self._tick(obj, status)
                #tick down the timer
                self._updateTimer(obj, status, dur - 1)

    #status effects may have timers
    def _updateTimer(self, obj, status, dur):
        if dur <= 0:
            self.remove(obj, status)
        else:
            self.add(obj, status, dur)
#do an effect to an object. This works this way so that you don't have to
#check every single thing in the game world;
#  - "hey, 4 of destiny. Are you sick? Are you on fire? Are you irritated? Are you paralyzed? etc....
#  - Hey inert rock. Are you sick? Are you on fire?
# Blah... blah... too many checks!! Just check ones who need checking.
    def _tick(self, obj, status):
        if status == SICK:
            pass
        
        elif status == FIRE:
            if obj.stats.temp < BURNTEMP: #cooled down too much to keep burning
                self.remove(obj, status)
                return
            rog.hurt(obj, FIREHURT)
            #create a fire at the location of burning things
            if rog.on(obj,ONGRID):
                rog.set_fire(obj.x,obj.y)
            
        elif status == IRRIT:
            pass
        
        elif status == PARAL:
            if dice.roll(20) <= ROLL_SAVE_PARAL:
                self.remove(obj, status)
                
        elif status == COUGH:
            pass
        
        elif status == VOMIT:
            pass
        
        elif status == BLIND:
            pass
        
        elif status == DEAF:
            pass
        






#
# Events
#

class Manager_Events():
    
    def __init__(self):        
        self._sights={}
        self._sounds={}
        self._listeners_sights=set()
        self._listeners_sounds=set()
    
    def add_sight(self, x,y, text):
        for obj in self._listeners_sights:
            if rog.can_see(obj, x,y):
                lis=self.get_sights(obj)
                lis.append(Event_Sight(x,y, text))
                self._sights.update({obj : lis})
    
    def add_sound(self, x,y, text, volume):
        for obj in self._listeners_sounds:
            if rog.can_see(obj, x,y):
                continue
            data=rog.can_hear(obj, x,y, volume)
            if data:
                dx,dy,volHeard=data
                if volHeard <= obj.stats.get('hearing')*0.2:
                    dx=dy=0
            #   each entity gets its own Event object,
            #   specific to its own perception.
                lis=self.get_sounds(obj)
                lis.append(Event_Sound(dx,dy, text, volHeard))
                self._sounds.update({obj : lis})
    
    def get_sights(self,obj):       return  self._sights.get(obj,[])
    def get_sounds(self,obj):       return  self._sounds.get(obj,[])
    def add_listener_sights(self,obj):      self._listeners_sights.add(obj)
    def add_listener_sounds(self,obj):      self._listeners_sounds.add(obj)
    def remove_listener_sights(self,obj):
        if obj in self._listeners_sights:
            self._listeners_sights.remove(obj)
    def remove_listener_sounds(self,obj):
        if obj in self._listeners_sounds:
            self._listeners_sounds.remove(obj)
    def clear(self):
        self._sights={}
        self._sounds={}

class Event_Sight():
    def __init__(self, x,y, text):
        self.x=x
        self.y=y
        self.text=text
class Event_Sound():
    def __init__(self, dx,dy, text, volume):
        self.dx=dx
        self.dy=dy
        self.text=text
        self.volume=volume

    
#
# Sights Seen by player
#

class Manager_SightsSeen(Manager):
    
    def __init__(self):
        super(Manager_SightsSeen,self).__init__()
        
        self.init_sights()
    
    def run(self):
        super(Manager_SightsSeen,self).run()
        
        atLeastOneMsg=False
        text=""
        for k,v in self.sights.items():
            if not v: continue
            atLeastOneMsg=True
            lis=v
            pc=rog.Ref.pc
            
            dirStr=DIRECTIONS_TERSE[k]
            if not dirStr == "self":
                text += "<{d}> ".format(d=dirStr)
            
            for strng in lis:
                text += "{}{} ".format(strng[0].upper(), strng[1:])

        if atLeastOneMsg:
            rog.msg(text)
            self.init_sights()
        
    def init_sights(self):
        self.sights={
        #   dir from: strings
            (0,0)   : [],
            (1,0)   : [],
            (1,-1)  : [],
            (0,-1)  : [],
            (-1,-1) : [],
            (-1,0)  : [],
            (-1,1)  : [],
            (0,1)   : [],
            (1,1)   : [],
        }
    
    def add(self, ev):
        k=self.get_direction(rog.Ref.pc, (ev.x,ev.y,))
        self.sights[k].append(ev.text)

    def get_direction(self, pc, coords):
        xf,yf=coords
        if (pc.x == xf and pc.y == yf):
            return 0,0
        rads=maths.pdir(pc.x,pc.y,xf,yf)
        dx=round(math.cos(rads))
        dy=round(math.sin(rads))
        return dx,dy

#
# Sounds Heard by player
#

class Manager_SoundsHeard(Manager):
    
    VOLCONST=400
    
    def __init__(self):
        super(Manager_SoundsHeard,self).__init__()
        
        self.init_sounds()
    
    def run(self):
        super(Manager_SoundsHeard,self).run()
        
        atLeastOneMsg=False
        text="__Hear__"
        for k,v in self.sounds.items():
            vol,lis=v
            if not vol: continue
            volTxt=self.get_volume_name(vol)
            dirStr=DIRECTIONS_TERSE[k]
            if not dirStr == "self":
                text += " <{d}>".format(d=dirStr)
            text += " ({v}) ".format(v=volTxt)
            for strng in lis:
                text += "{s}, ".format(s=strng)
            text=text[:-2] + "."
            atLeastOneMsg=True

        if atLeastOneMsg:
            rog.msg(text)
            self.init_sounds()
        
    def init_sounds(self):
        self.sounds={
        #   dir from: vol,strings
            (0,0)   : (0,[]),
            (1,0)   : (0,[]),
            (1,-1)  : (0,[]),
            (0,-1)  : (0,[]),
            (-1,-1) : (0,[]),
            (-1,0)  : (0,[]),
            (-1,1)  : (0,[]),
            (0,1)   : (0,[]),
            (1,1)   : (0,[]),
        }  
    
    def add(self, ev):
        
        k=(ev.dx,ev.dy,)
        data=self.sounds[k]
        cVol,lis=data

        if not ev.text in lis:
            lis.append(ev.text)
        maxVol=max(ev.volume, cVol)
        self.sounds.update({k : (maxVol, lis,)})
            
    def get_volume_name(self, perceivedVolume):
        pv=perceivedVolume
        vc=Manager_SoundsHeard.VOLCONST
        if pv >= vc:    return "fff"
        if pv >= vc/2:  return "ff"
        if pv >= vc/4:  return "f"
        if pv >= vc/8:  return "mf"
        if pv >= vc/16: return "mp"
        if pv >= vc/32: return "p"
        if pv >= vc/64: return "pp"
        else:           return "ppp"


#
# FOV
#

class Manager_FOV(Manager):

    def __init__(self):
        super(Manager_FOV, self).__init__()

        self.update_objs=[]

    def run(self):
        super(Manager_FOV, self).run()
        
        for obj in self.update_objs:
            rog.fov_compute(obj)
        
        self.update_objs=[]
            
    def close(self):
        super(Manager_FOV, self).close()
        
        pass
    
    # register a monster to have its FOV updated next turn
    def add(self,obj):
        if obj.stats.sight > 0:     # reject objects that can't see
            self.update_objs.append(obj)
        


#---------------------#
# game state managers #
#---------------------#


#
# Move View
#

class Manager_MoveView(GameStateManager):
    def __init__(self,view, con):
        super(Manager_MoveView, self).__init__()
        
        self.NUDGESPD   = 10
        self.view       = view
        self.con        = con
        self.refresh()
    
    def run(self, pcAct):
        super(Manager_MoveView, self).run(pcAct)
        
        for act,args in pcAct:
            if act=="target":   self.move(args)
            elif act=="select": self.set_result("select")
            elif act=="exit":   self.set_result("exit")
    
    def close(self):
        super(Manager_MoveView, self).close()
        
        rog.update_game()
        if self.result == "select":
            rog.view_center_player()
        
        
    def move(self,arg):
        dx,dy,dz = arg
        self.view.nudge(dx*self.NUDGESPD, dy*self.NUDGESPD)
        self.refresh()

    def refresh(self):
        libtcod.console_blit(self.con,
                             self.view.x, self.view.y, self.view.w, self.view.h,
                             rog.con_final(),
                             rog.view_port_x(), rog.view_port_y())
        rog.refresh()
    #
#




#
# Select Tile
#
# possible results:
#   - tuple of screen coordinates
#   - K_ESCAPE
#
# currently does nothing with its results. Used as a parent object...
#

class Manager_SelectTile(GameStateManager):
    
    def __init__(self, xs,ys, view, con):
        super(Manager_SelectTile, self).__init__()

        self.cursor     = IO.Cursor(0,0,rate=0.3)
        self.set_pos(rog.getx(xs), rog.gety(ys))
        self.view       = view
        self.con        = con
    
    def run(self, pcAct):
        super(Manager_SelectTile, self).run(pcAct)
        
        self.cursor_blink()
        for act,arg in pcAct:
            if act=='rclick':   self.rclick(arg)
            elif act=='lclick': self.lclick(arg)
            elif act=='target': self.nudge(arg)
            elif act=='select': self.select()
            elif act=="exit":   self.set_result('exit')
    
    def close(self):
        super(Manager_SelectTile, self).close()

        pass
    
    def cursor_blink(self):
        if self.cursor.blink():
            self.cursor.draw()
            libtcod.console_flush()
    
    def lclick(self,arg):
        xto,yto,zto = arg
        if (self.x==xto and self.y==yto):
            self.select(); return
        self.port(arg)
    
    def rclick(self,*args):
        self.port(*args)
        self.select()
        
    def port(self,tupl):
        xto,yto,zto = tupl
        self.set_pos(xto,yto)
        
    def nudge(self,tupl):
        dx,dy,dz = tupl
        if (self.is_shift_in_view_bounds(dx,dy)
                or self.is_cursor_by_edge_of_room(dx,dy) ):
            self.set_pos(self.x + dx, self.y + dy)
        else:
            self.view.nudge(dx,dy)
            self.refresh()
    
    def is_shift_in_view_bounds(self, dx,dy):
        if ( (dx == -1 and self.view.x == 0)
                or (dx == 1 and self.view.x == rog.view_max_x())
                or (dy == -1 and self.view.y == 0)
                or (dy == 1 and self.view.y == rog.view_max_y()) ):
             return True
        return False
    
    def is_cursor_by_edge_of_room(self, dx,dy):
        if ( (dx == 1 and self.x < self.view.w/2)
                or (dy == 1 and self.y < self.view.h/2)
                or (dx == -1 and self.x > self.view.w/2)
                or (dy == -1 and self.y > self.view.h/2) ):
             return True
        return False
            
    def set_pos(self,xto,yto):
        self.x=xto; self.y=yto
        self.restrict_pos()
        self.cursor.set_pos(self.x,self.y)
        self.cursor.blink_reset_timer_on()
        rog.refresh()
        
    def restrict_pos(self):
        x1 = rog.view_port_x()
        x2 = x1 + rog.view_w() - 1
        y1 = rog.view_port_y()
        y2 = y1 + rog.view_h() - 1
        self.x = maths.restrict(self.x, x1,x2)
        self.y = maths.restrict(self.y, y1,y2)
        
    def select(self):
        self.set_result( (rog.mapx(self.x), rog.mapy(self.y),) )
        
    def refresh(self):
        libtcod.console_blit(self.con,
                             self.view.x, self.view.y, self.view.w, self.view.h,
                             rog.con_final(),
                             rog.view_port_x(), rog.view_port_y())
        rog.refresh()
#




#
# Look Command
#
class Manager_Look(Manager_SelectTile):

    def __init__(self, *args,**kwargs):
        super(Manager_Look, self).__init__(*args,**kwargs)
    
    def run(self, *args,**kwargs):
        super(Manager_Look, self).run(*args,**kwargs)
    
    def close(self):
        super(Manager_Look, self).close()

        if (self.result and not self.result == "exit"):
            x,y = self.result
            rog.alert( rog.identify_symbol_at(x,y) )

        


#
# Print Vertically Scrollable Text
#
# possible results come from IO.Input()
#

class Manager_PrintScroll(GameStateManager):

    def __init__(self,con_mid,width,height, con_top,con_bot,h1=3,h2=4,maxy=0):
        super(Manager_PrintScroll, self).__init__()
        
        self.con_mid    = con_mid#dle
        self.con_top    = con_top
        self.con_bot    = con_bot#tom
        self.box1h      = h1
        self.box2h      = h2
        self.maxy       = maxy
        self.width      = width
        self.height     = height
        self.box2y      = self.height-self.box2h
        self.scrollspd  = 1
        self.pagescroll = self.height -(self.box1h +self.box2h +2)
        self.y          = 0
        self.update()
    
    def run(self, pcAct):
        super(Manager_PrintScroll, self).run(pcAct)
        
        self.user_input(pcAct)
    
    def close(self):
        super(Manager_PrintScroll, self).close()
        
        self.consoles_delete()
        rog.update_final()
    
    def user_input(self, pcAct):
        for act, arg in pcAct:
            if act=="target":
                self.y += arg[1]*self.scrollspd
                self.y=maths.restrict(self.y,0,self.maxy)
            elif act=="page up":    self.y = max(0,         self.y -int(self.pagescroll))
            elif act=="page down":  self.y = min(self.maxy, self.y +int(self.pagescroll))
            elif act=="home":       self.y = 0
            elif act=="end":        self.y = max(0,         self.maxy -self.pagescroll)
            elif (act=="select" or act=="exit"): self.set_result('exit')
            self.update()
    
    def update(self):
        rog.blit_to_final(self.con_mid, 0,self.y,  0,self.box1h)
        if self.con_top: rog.blit_to_final(self.con_top, 0,0, 0,0)
        if self.con_bot: rog.blit_to_final(self.con_bot, 0,0, 0,self.box2y)
        rog.refresh()
        
    def consoles_delete(self):
        libtcod.console_delete(self.con_mid)
        if self.con_top: libtcod.console_delete(self.con_top)
        if self.con_bot: libtcod.console_delete(self.con_bot)
#


'''
    Menu
    *bound_w and bound_h are the window dimensions
    *items is an iterable of strings
#   This manager's result is a selection from items
#   item in items can be a Thing() or a string
'''

class Manager_Menu(Manager):
    
    def __init__(self, name, x,y, bound_w,bound_h, keysItems, autoItemize=True): 
        super(Manager_Menu, self).__init__()
        
    #   init from args      #
    #   - keysItems: {unique id : pointer to menu item}
    #   - keysItems can be manually created and passed in
    #   or automatically created if autoItemize == True
        self.name=name
        self.x=x
        self.y=y
        self.bound_w=bound_w    # limits of where the menu can be on screen
        self.bound_h=bound_h
        self.border_w=1
        self.border_h=1
        if autoItemize:
            new={}
            for k,v in misc.itemize(keysItems):
                new.update({k:v})
            self.keysItems=new
        else: self.keysItems=keysItems
    #   get width and height from items
        widest=0
        for k,v in self.keysItems.items():
            leni=len(self.get_name(v)) + 4
            if leni > widest:
                widest=leni
        lenTitlePadding=4
        borderPadding=2
        lenn=len(self.name) + borderPadding + lenTitlePadding
        if lenn > widest: widest=lenn
        self.w=widest
        self.h=len(self.keysItems)
        self.w += self.border_w*2
        self.h += self.border_h*2
    #   make sure it doesn't go off-screen
        self.x -= max(0, self.x + self.w - self.bound_w)
        self.y -= max(0, self.y + self.h - self.bound_h)
    #   draw
        self.con=libtcod.console_new(self.w, self.h)
        self.draw()
    #   clear buffer
        IO.get_raw_input()
    
    def run(self):
        super(Manager_Menu, self).run()
        
        libtcod.sys_sleep_milli(5)
        key,mouse=IO.get_raw_input()
        
    #   mouse
        if mouse.lbutton_pressed:
            self.refresh()
            index=mouse.cy - self.y - self.border_h
            if (index >= 0 and index < self.h - self.border_h*2):
                result=tuple(self.keysItems.values())[index]
                self.set_result(result)
        
    #   key
        if libtcod.console_is_key_pressed(key.vk):
            if key.vk == libtcod.KEY_ESCAPE:
                self.set_result(-1)
        if key.vk == libtcod.KEY_TEXT: # select
            self.refresh()
            n=self.keysItems.get(key.text,None) #.decode()
            if n: self.set_result(n)
    
    def close(self):
        super(Manager_Menu, self).close()
        
        libtcod.console_delete(self.con)
        rog.refresh()
        
    def draw(self):
        def sorter(val):
            k,v = val
            #if (ord(k) < (65+26) and ord(k) >= 65): #this code makes capital and lowercase appear in inconsistent orders in the list...
            #    k=chr(ord(k)+32) #offset CAPS chars to make capital and lowercase equal (with capital coming second)
            return k
        y=0
    #   draw title and box
        misc.rectangle(self.con, 0,0, self.w,self.h, 0)
        title="<{}>".format(self.name)
        tx=math.floor( (self.w - len(title)) /2)
        libtcod.console_print(self.con, tx, 0, title)
    #   draw options
        lis=list(self.keysItems.items())
        lis.sort(key=sorter)
        for key,item in lis:
            name=self.get_name(item)
            libtcod.console_print(
                self.con, 1, y + 1, '({i}) {nm}'.format(i=key, nm=name) )
            y += 1
        libtcod.console_blit(
            self.con, 0,0, self.w, self.h,
            0, self.x, self.y
        )
        libtcod.console_flush()

    def get_name(self,item):
        return item.name if hasattr(item,'name') else item
    def refresh(self):
        self.draw()
        



























''' Adding volume from similar sound types... maybe not the best idea!???
            newVol=round(ev.volume*0.2) + cVol
            self.sounds.update({k : (newVol, lis,)})'''
            #n=misc.get_num_from_char(key.text.decode())

'''
class InputManager():
    def __init__(self,x,y,w,h,default,mode):
        # init
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.default = default
        self.mode = mode
        self.init_time   = time.time()
        
        self.text        = default   # displayed string
        self.field       = []        # string of letters from which 'text' is created
        for letter in text: self.field.append(letter)
        
        self.update          = True
        self.update_text     = True
        self.update_clear    = False
        
        self.console         = libtcod.console_new(w, h)
        # cursor
        self.cursor = Cursor()
        self.cursor_type         = 0         # options to change cursor display
        self.cursor_blink_delay  = 0.30      # seconds
        self.cursor_blink_time   = 0         # timestamp for blinking cursor
        self.cursor_pos          = len(field)
        self.cursor_visible      = True
        self.insert_mode         = False


    def update(self):
        if self.update:

            if self.update_text:
                self.text = ''.join(self.field)
                if self.update_clear:   libtcod.console_clear(self.console)
                libtcod.console_print_ex(self.console,0,0,
                    libtcod.BKGND_NONE,libtcod.LEFT, self.text)
            
                libtcod.console_blit(self.console, 0,0, self.w,self.h,
                                     0, self.x,self.y)
            
            cursor.setpos(self.x+self.cursor_pos,self.y)
            cursor.draw()
            
            libtcod.console_flush()
            update = clear_text = update_text = False


    def get_input(self):
        reply = None
        if libtcod.console_is_key_pressed(key.vk):
            reply = VK_TO_CHAR.get(key.vk, None)
        
        elif key.vk == libtcod.KEY_TEXT:
            decoded = key.text.decode()
            if (ord(decoded) >= 128 or decoded == '%'):
                continue    # Prevent weird error-causing ASCII input
            else: reply = decoded
        return reply


    def process_input(self,reply):
        
        if reply:

            # wait mode #
            
            if mode=="wait": return reply
            
            # Update screen and reset cursor blinker
            update= update_text= update_clear= cursor_visible= True # let user know their input was received
            cursor_blink_time = time.time() + cursor_blink_delay #  doing a longer cursor blink than usual

            # text mode #
            
            if mode=="text":
                if time.time() - init_time < .05: continue  # get rid of any input in the buffer
                #
                # special input functions
                #
                if libtcod.console_is_key_pressed(key.vk):
                    
                    ans = ord(reply)
                    if (ans == K_ENTER):    break
                    if (ans == K_ESCAPE):   break
                
                    if (ans == K_BACKSPACE) :
                        clear_text = True
                        if (cursor_pos == w - 1 and len(field) == w):
                            del field[ cursor_pos]  # Then acts like delete
                        elif (cursor_pos > 0 and len(field) >= cursor_pos) :
                            del field[ cursor_pos - 1]
                            cursor_pos -= 1
                            
                    elif (ans == K_DELETE) :
                        clear_text = True
                        if len(field) > cursor_pos: del field[ cursor_pos]
                    
                    elif (ans == K_LEFT) :
                        if cursor_pos > 0:  cursor_pos -= 1
                        
                    elif (ans == K_RIGHT) :
                        if (cursor_pos < w - 1 and cursor_pos < len(field)):
                            cursor_pos += 1
                    
                    elif (ans == K_INSERT) :            
                        insert_mode = not insert_mode
                #
                # text input
                #
                elif key.vk == libtcod.KEY_TEXT:
                    
                            # insert mode
                            
                    if ( len(field)==w or insert_mode ) :
                        if len(field) - 1 < cursor_pos:
                            field.append(reply)
                        else:
                            field[cursor_pos] = reply
                            
                            # normal mode
                    else:   
                        first_half = field[:cursor_pos]
                        second_half = field[cursor_pos:]
                        field = []
                        for c in first_half:
                            field.append(c)
                        field.append( reply)
                        for c in second_half:
                            field.append(c)
                    
                    # move cursor
                    if cursor_pos < w - 1:
                        cursor_pos +=1
                    #
                #
            #
        #

            
    def run(self):
            
        while True:
            
            libtcod.sys_sleep_milli(5) # checking for input 200 times per second is enough so just sleep a little
            
            time_stamp = time.time()
            if time_stamp - cursor_blink_time >= cursor_blink_delay:
                cursor_blink_time = time_stamp
                update = True
                cursor_visible = not cursor_visible
            
            self.update()
            
            
            # Check for keyboard event
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS,key,mouse)
            
            self.process_input(self.get_input())
            
        # end while

        
        return text



'''









