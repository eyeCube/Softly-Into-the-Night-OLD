'''
    game.py
    
    various classes + functions for global dealings
    
'''

import libtcodpy as libtcod
import time
import textwrap

from const      import *
import rogue as rog
import ai
import colors
import misc
import player
import debug

    
timer = debug.Timer()



'''
                    # Functions #
                    
'''

#
# play it!
# primary gameplay loop
#
def play(pc, pcAct):
    timer.reset()
    
    rog.release_souls()
    rog.compute_fovs() # maybe we should just recalc manually...
    
    # monster turn #
    
    if pc.stats.nrg <= 0:
        
        rog.turn_pass()
        rog.managers_perturn_run()
        
        for mon in rog.list_creatures():
            if rog.on(mon,DEAD): continue
            
            ai.tick(mon)
            spd=mon.stats.get('spd')
            rog.gain(mon,'nrg',spd, Max=spd)
            
        return
    
    # player turn #

    rog.pc_listen_sights()
    rog.pc_listen_sounds()
    rog.clear_listeners()
    
    rog.game_update()
    timer.print()
    
    player.commands(pc, pcAct)
    player.commands_pages(pc, pcAct)
    
    


'''
                    # Class definitions #
                    
'''


#
# Global Settings
#

class GlobalSettings():
    
    settingsFile = "settings.txt"
    
    _errorSettingsCorrupted="ERROR: Settings file '{f}' corrupted. (a) Fix the syntax error, OR (b) delete '{f}' and restart the game to reset to default settings.".format(f=settingsFile)
    _alertSettingsNotFound="ALERT: Settings file '{}' not found. Creating file from defaults...".format(settingsFile)
    _settingsCreated="Settings file '{}' created.".format(settingsFile)
    
    # Used for writing a new settings file from default settings #
    
    DEFAULTS = {
        "WINDOW WIDTH"  : 80,
        "WINDOW HEIGHT" : 50,
        "TILESET"       : "tileset_12x16.png",
        "RENDERER"      : libtcod.RENDERER_SDL,
        "FPSMAX"        : 60,
        "SHOWFPS"       : 0,
    }

    COMMENTS = {
        "RENDERER"      : '''Renderer 0, 1, or 2; 2 is slowest, but most compatible.
0 - GLSL
1 - OPENGL
2 - SDL''',
        "#DEEP"         : "Colors. RGB Values 0-255. Feel free to change!",
    }

    ##
    
    def __init__(self):
        self.file = GlobalSettings.settingsFile
        
    def apply(self):
        try:
            self._apply()
        except:
            print(GlobalSettings._errorSettingsCorrupted)
            raise
        
    def read(self):
        self.colors={}
        try:
            with open(self.file, 'r') as file:
                for line in file:
                    self.lastLine=line
                    if misc.file_is_line_comment(line):
                        continue
                    self.parse_line(line)
            print("Settings loaded from '{}'".format(self.file) )

        except FileNotFoundError:
            print(GlobalSettings._alertSettingsNotFound)
            self.write_defaults()
            print(GlobalSettings._settingsCreated)
            self.read()
        except:
            print(GlobalSettings._errorSettingsCorrupted)
            print("Last line read from '{}': {}".format(self.file, self.lastLine))
            raise

    def _apply(self):       # apply settings globally
        
        # window settings #
        libtcod.console_set_custom_font(self.tileset,
            libtcod.FONT_TYPE_GREYSCALE |
            libtcod.FONT_LAYOUT_ASCII_INROW, TILES_PER_ROW,TILES_PER_COL)
        libtcod.console_init_root(self.window_width,self.window_height,
                                  GAME_TITLE, False, renderer=self.renderer)
        libtcod.sys_set_fps(self.fpsmax)
        
        # colors #
        for k,v in self.colors.items():
            colors.COLORS.update({k:v})
        # colored strings
        colors.colored_strings=[]
        for item in self._colored_strings:
            colors.colored_strings.append(item)
    
    def parse_line(self,line):              #<- store settings in this object
        strng = self.parse_setting(line)
        
        if "RENDERER" in line:
            self.renderer = int(strng)
        elif "WINDOW WIDTH" in line:
            self.window_width = int(strng)
        elif "WINDOW HEIGHT" in line:
            self.window_height = int(strng)
        elif "FPSMAX" in line:
            self.fpsmax = int(strng)
        elif "SHOWFPS" in line:
            self.showfps = bool(int(strng))
        elif "TILESET" in line:
            self.tileset = strng
        elif "COLORED STRINGS" in line:
            self._colored_strings=[]
            elements = strng.split(";")
            for element in elements:
                if not element: continue
                self._colored_strings.append(element.split(","))
        elif "#" in line:           #<- all colors, and only colors, begin with '#'
            self.parse_color(line, strng)

    def write_defaults(self):       # create new settings.txt file from defaults
        
        def write_line(file, k,v):
            comment=self.COMMENTS.get(k, None)
            if comment:
                comment=comment.replace('\n','\n// ')
                file.write('// {}\n'.format(comment))
            newline = "{:20s}= {}\n\n".format(k,v)
            file.write(newline)
            
        with open(self.file, 'w+') as file:
            file.write('// {}\n\n'.format(self.file))
            for k,v in GlobalSettings.DEFAULTS.items():
                write_line(file, k,v)
        #   default Colors
            for k,v in colors.COLORS.items():   
                k="#" + k.upper()
                write_line(file, k,v)
            write_line(file, "COLORED STRINGS", colors.colored_strings)
    
    def parse_setting(self,line):
        pos= 1 + line.find("=")
        while line[pos]==' ': pos+=1
        return line[pos:-1]

    def parse_color(self, line, strng):
        i=1
        while not (line[i] == " " or line[i] == "="):
            i += 1
        k=line[1:i]
        k=k.lower()                 #<- lowercase colors
        strng=strng.replace(' ','') # get rid of spaces
        lis=strng.split(',')
        r,g,b=lis
        self.colors.update({k:libtcod.Color(int(r),int(g),int(b))})
    




#
# Console
# 
# global libtcod consoles
#
class Console():
    def __init__(self,w,h):
        self.final   = libtcod.console_new(w,h) # final surface blitted to 0
        self.game    = libtcod.console_new(w,h) # intermediate surface, displays HUD, messages, and the game view




#
# Controller
#
# handling state of the program
#
class Controller():
    
    def __init__(self):
        self.isRunning      = True
        self._state         = "normal"
        self._resume_state  = self._state
    
    def end(self):              self.isRunning=False
    def set_state(self,state):  self._state=state
    def set_resume_state(self,state):   self._resume_state=state
    
    @property
    def state(self):            return self._state
    @property
    def resume_state(self):     return self._resume_state


#
#
# Window
#
# Just stores relative locations and sizes of
# rendering areas on the game window
#

class Window():

    def __init__(self, w, h):
        # HUD
        HUD_X       = 0
        HUD_W       = w
        HUD_H       = 2
        HUD_Y       = h - HUD_H
        # Msgs
        MSGS_X      = 0
        MSGS_Y      = 0
        MSGS_W      = w
        MSGS_H      = 3
        # View
        VIEW_X      = 0
        VIEW_Y      = MSGS_H
        VIEW_W      = w
        VIEW_H      = h - HUD_H - MSGS_H
        
        self.root   = Box(0,0, w, h)
        self.hud    = Box( HUD_X, HUD_Y,  HUD_W, HUD_H)
        self.msgs   = Box(MSGS_X,MSGS_Y, MSGS_W,MSGS_H)
        self.scene  = Box(VIEW_X,VIEW_Y, VIEW_W,VIEW_H)

    def set_hud_left(self):
        self.hud.x = 0
        self.scene.x = self.hud.w
    def set_hud_right(self):
        self.hud.x = self.root.w - self.hud.w
        self.scene.x = 0
    def set_hud_visible(self,val):
        self.hud.visible = val

class Box():
    def __init__(self,x,y,w,h):
        self.x=x;self.y=y; self.w=w;self.h=h;
        self.visible = True
    


#
# Environment
#
class Environment():

    def __init__(self):
        self._genocides     = []
        self._tokill        = []
    
    def genocide(self,typ):     self._genocides.append(typ)
    def kill(self,mon):         self._tokill.append(mon)
    def release_souls(self): # unregister entities that have died
        if self._tokill:
            for mon in self._tokill:
                rog.release_creature(mon)
            self._tokill=[]




#
# View
#
class View():
    def __init__(self,w,h,roomw,roomh):
        self.x=0; self.y=0; self.w=w;self.h=h; self.roomw=roomw;self.roomh=roomh
        self.followSpd=10
        self._fixed_mode=False
    def fixed_mode_toggle(self):    self._fixed_mode=not self._fixed_mode
    def fixed_mode_disable(self):   self._fixed_mode=False
    def fixed_mode_enable(self):    self._fixed_mode=True
        
    def nudge(self,dx,dy):
        if self._fixed_mode: return
        self.x += dx; self.y += dy;
        #self.limit_pos()
    
    def follow(self,obj):
        if self._fixed_mode: return
        if obj.x > self.x + self.w*2/3 -1:      self.nudge(self.followSpd,0)
        elif obj.x <= self.x + self.w*1/3 -1:   self.nudge(-self.followSpd,0)
        if obj.y - self.y >= self.h*1/2 +5:
            self.nudge(0,int(self.followSpd/2))
        elif obj.y - self.y < self.h*1/2 -5:
            self.nudge(0,int(-self.followSpd/2))
        
    def limit_pos(self):
        self.x = min(self.x, self.roomw - self.w)
        self.y = min(self.y, self.roomh - self.h)
        self.x = max(self.x, 0)
        self.y = max(self.y, 0)

    def center(self,x,y):
        if self._fixed_mode: return
        self.x = x - int(self.w/2)
        self.y = y - int(self.h/2)
        #self.limit_pos()



#
# Clock
#
# Time and Turns
#
class Clock():
    def __init__(self):
        self._turn      = 0
        self._gametime  = 0
        self._timestamp = time.time()
    def turn_pass(self):
        self._turn +=1
        self._gametime += (time.time() - self._timestamp)
    @property
    def turn(self):         return self._turn



#
# Update
#
# keeps track of what needs updating
#
class Update():
    def __init__(self):
        self.updates = {
            'pcfov'     : True,
            'game'      : True,
            'hud'       : True,
            'msg'       : True,
            'final'     : True,
            'base'      : True,
            }
    
    def pcfov(self):    self.updates.update({'pcfov':True})
    def game(self):     self.updates.update({'game' :True})
    def hud(self):      self.updates.update({'hud'  :True})
    def msg(self):      self.updates.update({'msg'  :True})
    def final(self):    self.updates.update({'final':True})
    def base(self):     self.updates.update({'base' :True})

    def activate_all_necessary_updates(self):
        if (self.updates['game']) :   self.final()
        if (self.updates['final']):   self.base()
    
    def get_updates(self):
        lis = []
        for k,v in self.updates.items():
            if v==True: lis.append(k)
        return lis

    def set_all_to_false(self):
        for k in self.updates.keys():   self.updates.update({k:False})
    



#
# Message Log
#
class MessageLog():
    def __init__(self):
        self.msgs               = []
        self.msg_newEntry       = True
    
    def print(self,index):
        x = rog.msgs_x();y = rog.msgs_y(); w = rog.msgs_w();h = rog.msgs_h()
        rog.dbox(x,y,w,h,self.msgs[index], border=None,margin=0)

    def drawNew(self):
        self.msg_newEntry = True
        if self.msgs: self.print(-1)
        
    def capitalize(self, text): return text[0].upper() + text[1:]
    
    def msg_format_start(self, text, turn):
        return "[{}] {}".format(turn,text)
    
    def add(self, text, turn):
        if len(text) == 0: return False
        rog.update_msg()
        new=self.capitalize(text)
        if (self.msg_newEntry):
            self.msg_newEntry = False
            self.msgs.append( self.msg_format_start(new, turn) )
        else:
            self.msgs[-1] += new
        
    def printall_get_wrapped_msgs(self):
        w = rog.msgs_w()
        return '\n'.join( textwrap.fill( msg, w-2) for msg in reversed(self.msgs) )
    #
    


#-------------------------------------------------------------------------#
    



















