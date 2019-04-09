'''
    orangIO
    (Orange I/O)
    
    By: Jacob Timothy Wharton

    This is what I had to write to get input working the way
        I wanted it to work in libtcodpy... but it works now!!
    

    To add a new command into the game, add it into the key_bindings.txt
    defaults below. Add Shift+ or Ctrl+ or Alt+ or any combo thereof.
    Delete the key_bindings.txt file from the game's directory to
    have the game recreate it using the defaults.
    - Do not use spaces.
    - To do special keys, including SPACE, refer to the TEXT_TO_KEY dict.
    - Take note of the placement you put the command into the text file.
    Put that command into the dict COMMANDS in the SAME ORDER that you put
    it into key_bindings.
    - Put the command into player.commands or player.const_commands.
    
'''


import libtcodpy as libtcod
import time
import textwrap

from const      import *
from colors     import COLORS as COL
import managers
import maths
import misc
import word



key = libtcod.Key()
mouse = libtcod.Mouse()

NUM_ALT_CMDS = 3    # number of alternate key codes for each command.



file_keyBindings='key_bindings.txt'

# backup key bindings file:
KEYBINDINGS_TEXT_DEFAULT = '''//file name: {filename}

//  A "comment on comments"...
//All empty lines, and all lines beginning with "//"
//(without parentheses), are considered to be comments
//by the file reader, and are thus ignored.

//  Key Bindings Information
//Bindings are not case-sensitive.
//In order to remove one binding, set it to: NONE 
//Bindings may begin with any combination of shift, ctrl,
//and alt keys, followed by a plus (+) symbol:
//  Shift+ or Ctrl+ or Alt+
//Example key bindings:
//  CTRL+ALT+DELETE
//  shift+=
//  f
//  Ctrl+A
//The action bound to the last combo will function if and
//only if the a button is pressed WHILE the Ctrl button
//is being held, and neither Alt nor Shift are also being
//pressed down; if the Alt button is also being held, for
//instance, the input will be treated as "Ctrl+Alt+a",
//which is different from "Ctrl+a".
//Left and right Ctrl  are treated as the same;
//Left and right Alt   are treated as the same;
//Left and right Shift are treated as the same;

//NOTE: NumLock is currently unsupported. The numpad keys only
//work if you DO NOT have NumLock on. Keep it off during play.

//---------\\
// Bindings |
//---------//

// North
k
KP8
UP

// West
h
KP4
LEFT

// South
j
KP2
DOWN

// East
l
KP6
RIGHT

// Northwest
y
KP7
NONE

// Southwest
b
KP1
NONE

// Southeast
n
KP3
NONE

// Northeast
u
KP9
NONE

// Towards Self
.
KP5
NONE

// Up
Shift+,
NONE
NONE

// Down
Shift+.
NONE
NONE

// Get
g
,
NONE

// Light Bomb
Shift+b
NONE
NONE

// Examine
x
Shift+/
NONE

// Move view
v
NONE
NONE

// Fixed view mode
Shift+v
NONE
NONE

// Show player location (find player)
Ctrl+f
NONE
NONE

// Quit Game
Alt+q
NONE
NONE

//---------\\
//  MENUS   |
//---------//

// Select
SPACE
ENTER
NONE

// Exit
ESCAPE
NONE
NONE

// Page Up
PAGEUP
NONE
NONE

// Page Down
PAGEDOWN
NONE
NONE

// Home
HOME
NONE
NONE

// End
END
NONE
NONE

// Delete
DELETE
NONE
NONE

// Insert
INSERT
NONE
NONE

// Backspace
BACKSPACE
NONE
NONE

// Message History
Shift+h
NONE
NONE

// Inventory
i
NONE
NONE

//---------\\
// ADVANCED |
//---------//

// Shell / command prompt / console
Ctrl+`
NONE
NONE

// Execute last console command (during play)
Ctrl+Shift+`
NONE
NONE

// 

//
'''.format(filename=file_keyBindings)





TEXT_TO_KEY = {     # translate text into key constants
    'none'      : -1
    ,'kp0'      : libtcod.KEY_KP0
    ,'kp1'      : libtcod.KEY_KP1
    ,'kp2'      : libtcod.KEY_KP2
    ,'kp3'      : libtcod.KEY_KP3
    ,'kp4'      : libtcod.KEY_KP4
    ,'k5p'      : libtcod.KEY_KP5
    ,'kp6'      : libtcod.KEY_KP6
    ,'kp7'      : libtcod.KEY_KP7
    ,'kp8'      : libtcod.KEY_KP8
    ,'kp9'      : libtcod.KEY_KP9
    ,'up'       : libtcod.KEY_UP
    ,'down'     : libtcod.KEY_DOWN
    ,'right'    : libtcod.KEY_RIGHT
    ,'left'     : libtcod.KEY_LEFT
    ,'space'    : libtcod.KEY_SPACE
    ,'tab'      : libtcod.KEY_TAB
    ,'enter'    : libtcod.KEY_ENTER
    ,'escape'   : libtcod.KEY_ESCAPE
    ,'backspace': libtcod.KEY_BACKSPACE
    ,'insert'   : libtcod.KEY_INSERT
    ,'delete'   : libtcod.KEY_DELETE
    ,'home'     : libtcod.KEY_HOME
    ,'end'      : libtcod.KEY_END
    ,'pagedown' : libtcod.KEY_PAGEDOWN
    ,'pageup'   : libtcod.KEY_PAGEUP
    ,'f1'       : libtcod.KEY_F1
    ,'f2'       : libtcod.KEY_F2
    ,'f3'       : libtcod.KEY_F3
    ,'f4'       : libtcod.KEY_F4
    ,'f5'       : libtcod.KEY_F5
    ,'f6'       : libtcod.KEY_F6
    ,'f7'       : libtcod.KEY_F7
    ,'f8'       : libtcod.KEY_F8
    ,'f9'       : libtcod.KEY_F9
    ,'f10'      : libtcod.KEY_F10
    ,'f11'      : libtcod.KEY_F11
    ,'f12'      : libtcod.KEY_F12
}

VK_TO_CHAR = {      # translate key consants into a char
    libtcod.KEY_KP0     : '0',
    libtcod.KEY_KP1     : '1',
    libtcod.KEY_KP2     : '2',
    libtcod.KEY_KP3     : '3',
    libtcod.KEY_KP4     : '4',
    libtcod.KEY_KP5     : '5',
    libtcod.KEY_KP6     : '6',
    libtcod.KEY_KP7     : '7',
    libtcod.KEY_KP8     : '8',
    libtcod.KEY_KP9     : '9',
    libtcod.KEY_KPDEC   : '.',
    
    libtcod.KEY_UP          : chr(K_UP),
    libtcod.KEY_DOWN        : chr(K_DOWN),
    libtcod.KEY_RIGHT       : chr(K_RIGHT),
    libtcod.KEY_LEFT        : chr(K_LEFT),
    libtcod.KEY_BACKSPACE   : chr(K_BACKSPACE),
    libtcod.KEY_DELETE      : chr(K_DELETE),
    libtcod.KEY_INSERT      : chr(K_INSERT),
    libtcod.KEY_PAGEUP      : chr(K_PAGEUP),
    libtcod.KEY_PAGEDOWN    : chr(K_PAGEDOWN),
    libtcod.KEY_HOME        : chr(K_HOME),
    libtcod.KEY_END         : chr(K_END),
    libtcod.KEY_ENTER       : chr(K_ENTER),
    libtcod.KEY_KPENTER     : chr(K_ENTER),
    libtcod.KEY_ESCAPE      : chr(K_ESCAPE),
}

'''
# IMPORTANT!!
# Order of commands must match order in the key_bindings.txt file. #
'''
COMMANDS = {        # translate commands into actions
    'north'         : {'target': (0, -1,  0,) },
    'west'          : {'target': (-1, 0,  0,) },
    'south'         : {'target': (0,  1,  0,) },
    'east'          : {'target': (1,  0,  0,) },
    'northwest'     : {'target': (-1, -1, 0,) },
    'southwest'     : {'target': (-1, 1,  0,) },
    'southeast'     : {'target': (1,  1,  0,) },
    'northeast'     : {'target': (1, -1,  0,) },
    'self'          : {'target': (0,  0,  0,) },
    'up'            : {'target': (0,  0, -1,) },
    'down'          : {'target': (0,  0,  1,) },
    'get'           : {'get': True},
    'bomb'          : {'bomb': True},
    'look'          : {'look': True},
    'move view'     : {'move view': True},
    'fixed view'    : {'fixed view': True},
    'find player'   : {'find player': True},
    'quit'          : {'quit game': True},
    
    'select'        : {'select': True},
    'exit'          : {'exit': True},
    'pgup'          : {'page up': True},
    'pgdn'          : {'page down': True},
    'home'          : {'home': True},
    'end'           : {'end': True},
    'delete'        : {'delete': True},
    'insert'        : {'insert': True},
    'backspace'     : {'backspace': True},
    'msg history'   : {'message history': True},
    'inventory'     : {'inventory': True},
    
    'console'       : {'console': True},
    'last cmd'      : {'last cmd': True},
}






#-----------#
#  classes  #
#-----------#


#
# cursor
#
    
class Cursor():
    
    def __init__(self,x=0,y=0,rate=0.3):
        self.set_pos(x,y)
        self.time_stamp = 0
        self.blink_time = rate
        
    def set_pos(self,x,y):  self._x = x; self._y = y;
    def draw(self,con=0):   console_invert_color(con,self.x,self.y)
        
    def blink(self):
        if time.time() - self.time_stamp > self.blink_time:
            self.blink_reset_timer_off()
            return True
        else: return False
        
    def blink_reset_timer_off(self):
        self.time_stamp = time.time()
    def blink_reset_timer_on(self):
        self.time_stamp = 0
        
    @property
    def x(self): return self._x
    @property
    def y(self): return self._y






#-----------#
# functions #
#-----------#



# we add 256 here to differentiate character (text) codes from
# special key codes, like NumLock, which happens to have the same
# integer code (62) as > (greater than symbol), for example.
def key_getchar(k):     return k + 256
def key_get_pressed():      # get both vk and text in one variable
    k = libtcod.KEY_NONE
    if libtcod.console_is_key_pressed(key.vk) : k = key.vk 
    if k == libtcod.KEY_CHAR : k = key_getchar(key.c)
    return k
def key_get_special_combo(k):   # combine shift,ctrl,alt, and key press
    shift    =  key.shift
    ctrl     = (key.lctrl or key.rctrl)
    alt      = (key.lalt  or key.ralt )
    return (k, (shift, ctrl, alt,),)

def console_invert_color(con,x,y):
    col1 = libtcod.console_get_char_foreground(con,x,y)
    col2 = libtcod.console_get_char_background(con,x,y)
    libtcod.console_set_char_foreground(con, x,y, misc.color_invert(col1))
    libtcod.console_set_char_background(con, x,y, misc.color_invert(col2))

'''
def wait_for_input():
    _key,_mouse=get_raw_input()
    if libtcod.lbutton_pressed:
        if libtcod.console_has_mouse_focus():
            rog.game_set_state(rog.game_resume_state())
            '''

#
# key bindings
#

bind={}
NO_KEY=(-1,(False,False,False,),) # NULL key constant

# init_keyBindings
# call during setup to initialize the keyboard controls
def init_keyBindings():
    try:
        _init_keyBindings()
    except FileNotFoundError:
        print("'key_bindings.txt' File Not Found. Creating new file from defaults...")
        _keyBindings_writeFromDefault()
        _init_key_bindings()

#
# *DO NOT CALL THIS FUNCTION*
# call init_keyBindings instead
# _init_keyBindings
# read from a file and put key binding info into dict bind.
#
def _init_keyBindings():
        
    global bind

    codes = []  # list of key codes 0-511 (0-255 and an additional 256
                # for special key inputs like NumPad digits)
    combin = [] # list of tuples (shift,ctrl,alt) for key combinations
                
    with open(file_keyBindings, 'r') as bindings:
        for line in bindings:
            if misc.file_is_line_comment(line): continue #ignore comments
            
            #init
            line=word.remove_blankspace(line) #ignore white space
            line=line.lower() #not case-sensitive
            
            #NONE
            if "none" in line: #no key set, still need to put something in the list
                combin.append( (False,False,False,) )
                codes.append(   -1  ) # NULL key
                continue
            
            # Key combinations #
            
            delete=0
            if 'shift+' in line:
                delete+=6
                _shf = True
            else: _shf = False
            if 'ctrl+' in line:
                delete+=5
                _ctl = True
            else: _ctl = False
            if 'alt+' in line:
                delete+=4
                _alt = True
            else: _alt = False
            combinData=(_shf,_ctl,_alt,)
            if delete: line=line[delete:]
            
            if line[1] == '\n':     # character keys
                codeData=key_getchar(ord(line[0]))
            else:                   # special keys
                new = TEXT_TO_KEY.get(line[:-1],-1)
                codeData=new
            
            combin.append( combinData )
            codes.append(   codeData  )
        #
        
    print("Key bindings loaded from '{}'".format(file_keyBindings))
    
    # bind special combined key input to commands #
    
    n = NUM_ALT_CMDS
    for i,v in enumerate(COMMANDS.keys()):
        for j in range(n):
            bind.update({ (codes[i*n+j], combin[i*n+j],) : v })
#

def _keyBindings_writeFromDefault():
    try:
        with open(file_keyBindings,"w+") as file:
            file.write(KEYBINDINGS_TEXT_DEFAULT)
            print("'key_bindings.txt' Created.")
    except:
        print("FATAL ERROR! Failed to create key_bindings.txt")




#
#
# get raw input
#
# checks for input
# returns key and mouse objects in a tuple
#
def get_raw_input():
    libtcod.sys_sleep_milli(1)  # prevent from checking a billion times/second

    # we use the check_for_event instead of the wait_for_event function
    # because wait_for_event is stupid and causes lots of problems
    libtcod.sys_check_for_event(
        libtcod.EVENT_KEY
        | libtcod.EVENT_MOUSE_PRESS     # we only want to know mouse press
        | libtcod.EVENT_MOUSE_RELEASE,  # or release, NOT mouse move event.
        key, mouse)
    return (key,mouse,)
#
#
# handle_mousekeys
#
# convert keyboard and mouse input into player commands
# and return the command as a dict
#
def handle_mousekeys(keymouse):
    key,mouse=keymouse
    
    # Mouse #

    if mouse.lbutton_pressed:   return {'lclick': (mouse.cx,mouse.cy,0,) }
    if mouse.rbutton_pressed:   return {'rclick': (mouse.cx,mouse.cy,0,) }
    
    # Keys #
    
    k = key_get_pressed()
    combined = key_get_special_combo(k)
    
    return COMMANDS.get(bind.get(combined, None), {})
#
#
# get direction
# player chooses a direction using key bindings or the mouse,
# returns a tuple
#
def get_direction():
    while True:
        pcAct=handle_mousekeys(get_raw_input()).items()
        for act,arg in pcAct:
            if act=="target":
                return arg
            elif act=="exit":
                rog.alert("")
                return None
            elif act=="select":
                return (0,0,0,)
            elif act=="lclick":
                mousex,mousey,z=arg
                pc=rog.Ref.pc
                dx=mousex - rog.getx(pc.x)
                dy=mousey - rog.gety(pc.y)
                if (dx >= -1 and dx <= 1 and dy >= -1 and dy <= 1):
                    return dx,dy,0

#--------------------------------------------------#




#
# Text Input Manager
#
#

# Display user-entered text field with blinking cursor
# and handle all processes thereof.

# key bindings should NEVER affect input for this function.
# that got nasty real fast in Caves of Qud...

#---------------Args----------------#
# int x,y           location on screen
# int w,h           width and height of textbox
# string default    text that appears when textbox is created
# string mode       'text' or 'wait' :
#   - text mode: normal input mode, returns text when Enter key pressed
#   - wait mode: returns first accepted key press input
# bool insert       begin in "insert" mode?
#

class TextInputManager(managers.Manager):
    
    def __init__(self, x,y, w,h, default,mode,insert):
        
        # init
        self.console    = libtcod.console_new(w, h)
        self.init_time  = time.time()
        
        self.x=x
        self.w=w
        self.y=y
        self.h=h
        self.mode=mode
        self.text=default
        self.default=default
        
        self.keyInput=''
        
        self.redraw_cursor  = True
        self.render_text    = True
        self.flush          = False
        
        self.key=key
        self.mouse=mouse
        
        self.cursor=Cursor()
        self.cursor.set_pos(x,y)
        self.insert_mode=insert #replace the character under the cursor or shift it aside?
        
        #ignore buffer
        get_raw_input()


    def set_result(self,val):
        if val == '': val=self.default
        if val == '': val='0'
        super(TextInputManager,self).set_result(val)
    
    def run(self):
        super(TextInputManager, self).run()
        
        libtcod.sys_sleep_milli(5)  # checking for input 200 times per second is enough so just sleep a little
        
        self.update()
        
        libtcod.sys_check_for_event(    # check don't wait.
            libtcod.EVENT_KEY
            | libtcod.EVENT_MOUSE_PRESS     # we only want to know mouse press
            | libtcod.EVENT_MOUSE_RELEASE,  # or release, NOT mouse move event.
            self.key, self.mouse)
        
        self.get_char()
        self.mouse_events()
        self.keyboard_events()
    
    def close(self):
        ##do not inherit
        libtcod.console_delete(self.console)
    
    def update(self):
        
        self.flush=False
        
        if self.cursor.blink():
            self.redraw_cursor=True
            
        if self.render_text:
            self.update_render_text()
            self.redraw_cursor=True
            
        if self.redraw_cursor:
            self.cursor.draw()
            self.flush=True
            
        if self.flush:
            libtcod.console_flush()
        
        self.redraw_cursor  =False
        self.render_text    =False
        self.flush          =False

    def keyboard_events(self):
        
        if self.keyInput:

            if self.mode == "wait": self.set_result(self.keyInput)

            self.redraw_cursor=True
            self.cursor_blinkOn()

            if self.mode == "text":
                self.input_vk()
                self.input_text()

    def mouse_events(self):
        
        if self.mouse.lbutton_pressed:
            self.cursor_blinkOn()
            self.putCursor(self.mouse.cx - self.x)
            self.blit_console()
            self.flush=True


    def input_vk(self):
        
        if not libtcod.console_is_key_pressed(self.key.vk):
            return

        cpos=self.cursor_pos
        ans=ord(self.keyInput)

        # returning a result
        if (ans == K_ENTER):    self.set_result(self.text)
        if (ans == K_ESCAPE):   self.set_result(self.default)

        # deleting
        if (ans == K_BACKSPACE) :
            self.render_text=True
            self.putCursor(cpos - 1)
            self.delete()
        elif (ans == K_DELETE) :
            self.render_text=True
            self.delete()
        # moving
        elif (ans == K_LEFT)    : self.move(cpos - 1)
        elif (ans == K_RIGHT)   : self.move(cpos + 1)
        
        # insert mode
        elif (ans == K_INSERT)  : self.insert_mode = not self.insert_mode


    def input_text(self):

        if not self.key.vk == libtcod.KEY_TEXT:
            return
        
        ans=self.keyInput
        if self.cursor_pos < len(self.text): # insert or replace
            self.render_text=True
            first_half = self.text[:self.cursor_pos]
            second_half = self.text[self.insert_mode + self.cursor_pos:]
            self.text='{}{}{}'.format(first_half, ans, second_half)
        else:   # append
            self.text += ans
            self.put_next_char(ans)
            self.blit_console()
            self.flush=True

        # truncate
        if (len(self.text) > self.w):
            self.text = self.text[:self.w]
        
        # move cursor
        self.putCursor(self.cursor_pos + 1)
        #


    def move(self, new):
        libtcod.console_set_char_foreground(
            0, self.x + self.cursor_pos, self.y, COL['white'])
        libtcod.console_set_char_background(
            0, self.x + self.cursor_pos, self.y, COL['black'])
        self.flush=True
        self.putCursor(new)

    def update_render_text(self):
        libtcod.console_clear(self.console)
        libtcod.console_print_ex(
            self.console,0,0,
            libtcod.BKGND_NONE,libtcod.LEFT,
            self.text )
        self.blit_console()
    
    def get_char(self):
        reply=''
        if libtcod.console_is_key_pressed(self.key.vk):
            reply = VK_TO_CHAR.get(self.key.vk, None)
        
        elif self.key.vk == libtcod.KEY_TEXT:
            tx = self.key.text #.decode()
            if (ord(tx) >= 128 or tx == '%'):
                return ''    # Prevent problem-causing input
            else: reply=tx
        self.keyInput=reply

    def delete(self):
        self.text=self.text[:self.cursor_pos] + self.text[1+self.cursor_pos:]
        
    def put_next_char(self,new):
        libtcod.console_put_char_ex(
            self.console, self.cursor_pos,0, new,
            COL['white'],COL['black']
        )
    def blit_console(self):
        libtcod.console_blit(
            self.console,   0,0,self.w,self.h,
            0,      self.x,self.y
        )    
    '''def ignore_buffer(self):
        return (time.time() - self.init_time < .05)'''
    def putCursor(self,new):
        pos=maths.restrict( new, 0, min(self.w - 1, len(self.text)) )
        self.cursor.set_pos(self.x + pos, self.y)
    def cursor_blinkOn(self):   self.cursor.blink_reset_timer_on()
    
    @property
    def cursor_pos(self):   return self.cursor.x


















            #if (cursor_visible or insert_mode or len(field)==w ):
                
                #cursor.draw(0,cursor_type)


'''
        xc = self.x; yc = self.y;
        if cursor_type == 0:
            char = libtcod.console_get_char(con,xc,yc)
            libtcod.console_put_char_ex(Cursor.con_char, 0,0, char,BLACK,WHITE)
        libtcod.console_blit(Cursor.con_char, 0,0,1,1,     # source
                             con, xc,yc)  # dest
'''




'''for k,v in COMMANDS.items():
    if (combined == bind[k] or combined == bind_alt[k]):
        action = v
        break'''    
'''elif (cursor_type == 1):
                    cursor_char=char_insert if (insert_mode or len(field) == w) else char_normal
                    libtcod.console_put_char(con_cursor, 0,0, cursor_char,
                                             libtcod.BKGND_NONE)'''



