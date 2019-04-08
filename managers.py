#
# some various managers
# and parent manager objects
#

import libtcodpy as libtcod
import time
import math

from const      import *
import rogue    as rog
import orangio  as IO
import maths
import misc






'''
#
# abstract Manager class
#
# 
# A manager is an object that has functions for handling a complex task,
# which is carried out using its 'run()' function.
# give it some starting data, then call 'run()' inside a while loop.
# check the output of the manager with the property 'result'.
# finish the execution by calling 'close()'.
#
#     * Only the 'run', 'close', and 'result' functions should be called
    outside of the manager.
      * The manager only accesses its own functions through its 'run' method.
      * You can intercept the 'run' function at the end of each iteration
    in your while loop, simply by writing code following the 'run()' call.
    This is one of the useful things about managers.
#
'''

class Manager(object):
    
    def __init__(self):
        self._result=None
    def set_result(self,new):       self._result=new
    @property
    def result(self):           return self._result
    def run(self, *args,**kwargs):
        self.set_result(None)
    def close(self):
        pass
#

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
# Fires
#

class Manager_Fires(Manager):

    def __init__(self):
        super(Manager_Fires, self).__init__()

        self.thingsOnFire=[]
        self.lights={}

    def add(self, obj):     self.thingsOnFire.append(obj)
    def remove(self, obj):  self.thingsOnFire.remove(obj)

    def run(self):
        super(Manager_Fires, self).run()

        for obj in self.thingsOnFire:
            x,y=obj.x,obj.y
            if rog.burn(obj):
                if not obj.isCreature:
                    if rog.on(obj,DEAD):
                        textSee="{t}{n} burns to ashes.".format(
                            t=obj.title,n=obj.name)
                        rog.event_sight(x,y, textSee)
                        continue
                    else: textSee=""
                else:
                    textSee="{t}{n} burns.".format(t=obj.title,n=obj.name)
                rog.event_sight(x,y, textSee)
                rog.event_sound(x,y, SND_FIRE)
                self.fire_spread(obj)
            else:
                self.remove(obj)
            
    def close(self):
        super(Manager_Fires, self).close()
        
        pass

    # make an object be on fire
    def set_fire(self, obj):
        if rog.on(obj,FIRE): return
        rog.make(obj,FIRE)
        self.add(obj)
        light=rog.create_light(obj.x,obj.y, 10, owner=obj)
        obj.observer_add(light)
        self.lights.update({obj : light})

    # put an object's fire out
    def douse(self, obj):
        rog.makenot(obj,FIRE)
        light=self.lights[obj]
        rog.release_light(light)
        obj.observer_remove(light)
        self.remove(obj)
        textSee="The fire on {n} is extinguished.".format(n=obj.name)
        rog.event_sight(obj.x,obj.y, textSee)
        rog.event_sound(obj.x,obj.y, SND_DOUSE)

    # look nearby a burning object to try and set other stuff on fire
    def fire_spread(self, fromObj):
        xo=fromObj.x
        yo=fromObj.y
        heat=fromObj.mass
        for x in range(max(0,xo - 1), min(ROOMW, xo + 1)):
            for y in range(max(0,yo - 1), min(ROOMH, yo + 1)):
                thing=rog.thingat(x,y)
                if thing:
                    self.burn(thing, heat)

    def burn(self, obj, heat):
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
        y=0
    #   draw title and box
        misc.rectangle(self.con, 0,0, self.w,self.h, 0)
        title="< {} >".format(self.name)
        tx=math.floor( (self.w - len(title)) /2)
        libtcod.console_print(self.con, tx, 0, title)
    #   draw options
        for key,item in self.keysItems.items():
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









