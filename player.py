'''
player.py

'''

from const      import *
from colors     import COLORS
import rogue    as rog
import orangio  as IO
import action
import debug
import monsters





#
#   constant commands
#   can be performed from anywhere in the main game loop
#

def commands_const(pc, pcAct):
    for act,arg in pcAct:        
        if act == "console":    debug.cmd_prompt(globals(), locals())
        elif act == "last cmd": debug.execute_last_cmd(globals(), locals()) 
        elif act == "quit game":rog.end()

def commands_pages(pc, pcAct):
    for act,arg in pcAct:
        if act == "message history" :
            rog.routine_print_msgHistory()  
            return
        if act == "inventory" :
            action.inventory_pc(pc,pc.inv)
            return


#
#   commands
#

directional_command = 'move'

def commands(pc, pcAct):
    
    for act,arg in pcAct:
        
        rog.update_base()   # refresh screen

        # actions that take multiple turns
        busyTask=rog.occupations(pc)
        if busyTask:
            tLeft,helpless,fxn,args=busyTask
            if tLeft:
                pc.stats.nrg=0
                rog.occupations_elapse_turn(pc)
            elif fxn is not None:
                fxn(args)
        
        #----------------#
        # convert action #
        #----------------#
        
        if act =='target':  act=directional_command
        
        
        #----------------#
        # perform action #
        #----------------#
#-----------MOUSE ACTION----------------------------#
        
        if act == 'lclick':
            mousex,mousey,z=arg
            if rog.wallat(mousex,mousey):
                return
            
            rog.path_compute(pc.path, pc.x,pc.y, rog.mapx(mousex), rog.mapy(mousey))
            #rog.occupation_set(pc,'path')

        if act == 'rclick':
            pass
        
#------------OTHER ACTION--------------------------#
        
        if act == 'move':
            dx,dy,dz=arg
            xto=pc.x + dx
            yto=pc.y + dy

            # wait
            if (xto==pc.x and yto==pc.y):
                pc.stats.nrg = 0
                return

            # out of bounds
            if not ( rog.is_in_grid_x(xto) and rog.is_in_grid_y(yto) ):
                return
            
            # fight if there is a monster present
            mon = rog.monat(xto,yto)
            if (mon and mon is not pc):
                action.fight(pc,mon)
            # or move
            elif not rog.solidat(xto,yto):
                # space is free, so we can move
                if action.move(pc, dx,dy):
                    rog.view_center_player()

        if act == "bomb":
            action.bomb_pc(pc)
            return
        if act == "get":
            action.pickup_pc(pc)
            return
        #
        #
        # special actions #
        #
        
        if act == 'find player':
            rog.alert('press any key to continue...')
            rog.Input(rog.getx(pc.x), rog.gety(pc.y), mode='wait')
            rog.update_base()
            return
        if act == "look":
            rog.routine_look(pc.x,pc.y)
            return
        if act == "move view":
            rog.routine_move_view()
            return
        if act == "fixed view":
            rog.fixedViewMode_toggle()
            return  
        if act == 'select':
            print(rog.Input(0,0,20))
            return
        if act == 'exit':
            return

    # end for
# end def



#
#   init player object. Pass a Thing into the function...
#

def init(pc):
    
    # register for sense events for the message log
    rog.add_listener_sights(pc)
    rog.add_listener_sounds(pc)
    rog.view_center(pc)
    rog.givehp(pc)
    rog.givemp(pc)
#

#
# Chargen
# Create and return the player Thing object,
#   and get/set the starting conditions for the player
#
def chargen():
    # init
    x1 = 0; y1 = 0;
    xx = 0; yy = 4;
    ww = rog.window_w(); hh = 5;

    # _printElement - local function
    # draw the string to con_game at (x1,y1) then move y vars down
    def _printElement(elemStr):
        global x1,y1
        rog.dbox(x1,y1,ROOMW,3,text=elemStr,
            wrap=False,border=None,con=rog.con_game(),disp='mono')
        rog.blit_to_final(rog.con_game(),0,0)
        rog.refresh()
        y1+=1; yy+=1;
    
    # get char data from player
    
    # name
    _name=rog.prompt(x1,y1,ww,hh,maxw=20, question="What is your name?", mode="text")
    _title = ""
    print("Name chosen: ", _name)
    _printElement("Name: {}".format(_name))
    
    # gender
    _gender = ''
    while (_gender != 'm' and _gender != 'f' and _gender != 'n'):
        _menuList={'m':'male','f':'female','n':'nonbinary','*':'random'}
        
        _gender=rog.menu("Gender Select",xx,yy,_menuList)
        if _gender == 'n':
            #select gender from list of added genders
                #[...]
            #add gender
            _genderName,_pronouns = _add_gender()
            if _genderName!='': #failed to add new gender
                _gender='' #prompt user again
        else:
            if _gender == 'm':
                _genderName = "male"
                _pronouns = ('he','him','his',)
            else:
                _genderName = "female"
                _pronouns = ('she','her','hers',)
    #set pronouns
    print("Gender chosen: ", _genderName)
    _printElement("Gender: {}".format(_genderName))
    
    # class
    libtcod.console_clear(rog.con_final())
    rog.dbox(x1,y1,ROOMW,3,text="What is your profession?",
        wrap=True,border=None,con=rog.con_final(),disp='mono')
    #rog.refresh()
    _classList={} #stores {className : (classChar, classID,)} #all classes
    _menuList={} #stores {classChar : className} #all playable classes
    for k,v in CLASSES.items(): # k=ID v=charType
        #if k not in rog.playableClasses(): continue #only playable classes
        n=monsters.bestiary[v][0]   # get name of the class
        ID=k                        # get ID of the class
        _classList.update({n:(v,ID,)})
        typ=monsters.bestiary[v][0]
        _menuList.update({v:n})
    _menuList.update({'*':'random'})
    _className = rog.menu("Class Select",xx,yy,_menuList)
    if _className == 'random':
        choice = dice.roll(len(_menuList.keys())-1) #random is not an option
        _className = _menuList[choice-1] #index goes from 0 to (choice-1)
    _type = _classList[_className][0] # get the class Char value
    _classID = _classList[_className][1]
    print("Class chosen: ", _className)
    _printElement("Class: {}".format(_className))

    # skill
    libtcod.console_clear(rog.con_final())
    rog.dbox(x1,y1,ROOMW,3,text="What skill did you learn in childhood?",
        wrap=True,border=None,con=rog.con_final(),disp='mono')
    #rog.refresh()
        #get list of all skills
    _skillName = rog.menu("Skill Select",xx,yy,SKILLS.keys())
    _skillID = SKILLS[_skillName]
    print("Skill chosen: ", _skillName)
    #should show ALL skills you're skilled in, not just the one you pick
    #for skill in jobs.getSkills(_skillID):
    _printElement("Skilled in: {}".format(_skillName))

    #stats
    _stats = {}
    #gift
    _gift = 0
    
    pc = rog.create_monster(_type,0,0,COLORS['white'])
    pc.name = _name
    pc.job = _className
    pc.gender = _genderName
    pc.pronouns = _pronouns
    pc.faction = FACT_ROGUE
    #add additional skill
    rog.train(pc,_skillID)
    return pc
#

# LOCAL FUNCTIONS

def _add_gender():
    x1=5
    y1=5
    ww=20
    hh=3
    #get new gender name
    _genderName=rog.prompt(x1,y1,ww,hh, "What is your gender?", mode="text")
    #pronouns
    #subject pronoun
    _pronoun1=rog.prompt(x1,y1,ww,hh,
        "What are your pronouns?\n\tSubject pronoun:",
        default="they",mode="text",insert=True)
    #object pronoun
    _pronoun2=rog.prompt(x1,y1,ww,hh,
        "What are your pronouns?\n\tObject pronoun:",
        default="them",mode="text",insert=True)
    #possessive pronoun
    _pronoun3=rog.prompt(x1,y1,ww,hh,
        "What are your pronouns?\n\tPossessive pronoun:",
        default="their",mode="text",insert=True)
    success=rog.prompt(x1,y1,ww,6,
"Confirm gender: "+_genderName+"\nSubject pronoun: "+_pronoun1+"\nObject pronoun: "+_pronoun2+"\nPossessive pronoun: "+_pronoun3+"\n\nConfirm (y) or Cancel (n)",
        mode='wait')
    if success:
        #add the gender into the genders text file for next game
        return (_genderName,(_pronoun1,_pronoun2,_pronoun3,),)
    else:
        return ("",())






















'''
            # TESTING INPUT
            rog.update_final()
            text = rog.Input(0,0, 40,1)
            print("returned '" + text + "'")
            
                    ## TESTING TESTING WHY DON'T YOU ARRESTING
                    rog.Ref.Map.recall_memories(rog.view_x(),rog.view_y(),rog.view_w(),rog.view_h())
                    action.move(pc,14,14)
                    rog.Ref.Map.tile_change(pc.x,pc.y,FLOOR)
                    rog.Ref.Map.tile_change(pc.x,pc.y-1,FLOOR)
                    rog.Ref.Map.tile_change(pc.x,pc.y-2,FLOOR)
                    rog.Ref.Map.tile_change(pc.x-1,pc.y-2,FLOOR)
                    rog.Ref.Map.tile_change(pc.x-1,pc.y-1,FLOOR)
                    rog.Ref.Map.tile_change(pc.x-1,pc.y,FLOOR)
                    rog.view_center(pc)
                    ##
                    '''




