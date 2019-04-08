#
# action
#

from const import *
import rogue as rog
import orangio as IO
import dice
import weapons
import maths
import items




occupations={}



# player only actions #

def bomb_pc(pc): # drop a lit bomb
    rog.alert("Place bomb where? <hjklyubn>")
    args=IO.get_direction()
    if not args: return
    dx,dy,dz=args
    xx,yy=pc.x + dx, pc.y + dy
    
    if not rog.thingat(xx,yy):
        weapons.Bomb(xx,yy, 8)
        rog.drain(pc, 'nrg', NRG_BOMB)
        rog.msg("{t}{n} placed a bomb.".format(t=pc.title,n=pc.name))
    else:
        rog.alert("You cannot put that in an occupied space.")


def pickup_pc(pc):
    rog.alert("Pick up what? <hjklyubn.>")
    args=IO.get_direction()
    if not args: return
    dx,dy,dz=args
    xx,yy=pc.x + dx, pc.y + dy
    
    thing=rog.inamat(xx,yy) if (xx == pc.x and yy == pc.y) else rog.thingat(xx,yy)
    if thing:
        if not thing.isCreature:
            # pocketing the thing
            rog.drain(pc, 'nrg', NRG_POCKET)
            rog.give(pc,thing)
            rog.release_inanimate(thing)
            rog.msg("{t}{n} pockets {i}.".format(
                t=pc.title,n=pc.name,i=thing.name))
        else:
            rog.alert("You can't pick that up!")
    else:
        rog.alert("There is nothing there to pick up.")


def inventory_pc(pc,pcInv):
    if not pc.inv:
        rog.alert(ALERT_EMPTYCONTAINER)
        return
    x=2
    y=rog.view_port_y() + 2
#   items menu
    item=rog.menu("{}'s Inventory".format(pc.name), x,y, pcInv)
    
#   viewing an item
    if not item == -1:
        keysItems={}
        
    #   get available actions for this item...
        if rog.on(item,CANEAT):
            keysItems.update({"E":"Eat"})
        if rog.on(item,CANQUAFF):
            keysItems.update({"q":"quaff"})
        if rog.on(item,CANEQUIP):
            keysItems.update({"e":"equip"})
        if rog.on(item,CANUSE):
            keysItems.update({"u":"use"})
        keysItems.update({"x":"examine"})
        keysItems.update({"d":"drop"})
        keysItems.update({"t":"throw"})
        #
        
        opt=rog.menu(
            "{}".format(item.name), x,y,
            keysItems, autoItemize=False
        )
        print(opt)
        if opt == -1: return
        opt=opt.lower()
        
        rmg=False
        if   opt == "drop":     rmg=True; drop_pc(pc,item)
        elif opt == "equip":    rmg=True; equip_pc(pc,item)
        elif opt == "eat":      rmg=True; eat(pc, item)
        elif opt == "quaff":    rmg=True; quaff(pc, item)
        elif opt == "use":      rmg=True; use(pc, item)
        elif opt == "examine":  rmg=True; examine_pc(item)
        
        if rmg: rog.drain(pc, 'nrg', NRG_RUMMAGE)
#

def drop_pc(pc,item):
    rog.alert("Place {i} where? <hjklyubn.>".format(i=item.name))
    args=IO.get_direction()
    if not args: return
    dx,dy,dz=args
    
    if not rog.wallat(pc.x+dx,pc.y+dy):
        rog.drain(pc, 'nrg', NRG_RUMMAGE)
        rog.drop(pc,item, dx,dy)
        rog.msg("{t}{n} dropped {i}.".format(t=pc.title,n=pc.name,i=item.name))
    else: rog.alert("You can't put that there!")

        
def equip_pc(pc,item):
    #fornow, just wield it THIS SCRIPT NEEDS WORK>>>>...
    rog.drain(pc, 'nrg', NRG_RUMMAGE + NRG_WIELD)
    if rog.hasequip(pc,item):
        if rog.unwield(pc,item):
            rog.msg("{t}{n} wields {i}.".format(t=pc.title,n=pc.name,i=item.name))
        else: rog.alert("You are already wielding something in that hand.")
    else: rog.wield(pc,item)


def examine_pc(thing):
    rog.drain(pc, 'nrg', NRG_EXAMINE)
    rog.dbox(0,0,40,30, thing.DESCRIPTIONS[item.name])



################################################

#wait
#just stand still and do nothing
#recover your Action Points to their maximum
def wait(obj):
    obj.stats.nrg=0


#use
#"use" an item, whatever that means for the specific item
def use(obj, item):
    pass


#quaff
#drinking is instantaneous action
def quaff(obj, drink):
    rog.drain(pc, 'nrg', NRG_QUAFF) 
    drink.quaff(obj)
    rog.event_sight(obj.x,obj.y, "{t}{n} quaffs a {p}.".format(
        t=obj.title,n=obj.name,p=drink))
    rog.event_sound(obj.x,obj.y, SND_QUAFF)


#move
#returns True if move was successful, else False
#do not drain Action Points unless move was successful
def move(obj,dx,dy):  # locomotion
    xto=obj.x+dx
    yto=obj.y+dy
    terrain_cost=rog.cost_move(obj.x,obj.y,xto,yto, None)
    if terrain_cost == 0:  return False     # 0 means we can't move there
    mult = 1.41 if (dx + dy) % 2==0 else 1  # diagonal extra cost
    modf=NRG_MOVE
    nrg_cost=round(modf*mult*terrain_cost*AVG_SPD/max(1, obj.stats.get('msp')))
    rog.drain(obj, 'nrg', nrg_cost)
    rog.port(obj, xto, yto)
    return True


#
# fight
#
# Arguments:
# attkr,dfndr:  attacker, defender
# adv:          advantage attacker has over defender
# dtyp:         damage type:            
#                 - 'die' is a die roll,
#                 - 'crit' does max * extra damage

def fight(attkr,dfndr,adv=0):
    nrg_cost = round( NRG_ATTACK*AVG_SPD/max(1, attkr.stats.get('asp')) )
    attkr.stats.nrg -= nrg_cost

    die=20
    acc=attkr.stats.get('atk')
    dv=dfndr.stats.get('dfn')
    hit = False
    if (dice.roll(die + acc + adv - dv) >= dice.roll(die)):
#    if (dice.roll(COMBATROLL) + acc + adv >=
#        dice.roll(COMBATROLL) + dv ):
        hit = True
        
        dmg = max(0, attkr.stats.get('dmg') - dfndr.stats.get('arm') )
        #hpmax_before=dfndr.stats.hpmax
        rog.hurt(dfndr, dmg)
        killed = rog.on(dfndr,DEAD)
        
    
    # should first do a check to see if player can sense fight happening
    message = True
    a=attkr.name; n=dfndr.name; t1=attkr.title; t2=dfndr.title; x='.';
    
    #noise(attkr.x,attkr.y,10)
    # make a message describing the fight
    if message:
        if hit==False: v="misses"
        elif dmg==0: v='cannot penetrate'; x="'s armor!"
        elif killed: v='kills'
        else: v='hits'
        rog.event_sight(
            dfndr.x,dfndr.y,
            "{t1}{a} {v} {t2}{n}{x}".format(a=a,v=v,n=n,t1=t1,t2=t2,x=x)
        )
        rog.event_sound(dfndr.x,dfndr.y, SND_FIGHT)
    
# end def


# not necessarily creature actions #

def explosion(bomb):
    con=libtcod.console_new(ROOMW, ROOMH)
    rog.msg("{t}{n} explodes!".format(t=bomb.title, n=bomb.name))
    fov=rog.fov_init()
    libtcod.map_compute_fov(
        fov, bomb.x,bomb.y, bomb.r,
        light_walls = True, algo=libtcod.FOV_RESTRICTIVE)
    
    for x in range(bomb.r*2 + 1):
        for y in range(bomb.r*2 + 1):
            xx=x + bomb.x - bomb.r
            yy=y + bomb.y - bomb.r
            if not libtcod.map_is_in_fov(fov, xx,yy):
                continue
            if not rog.is_in_grid(xx,yy): continue
            dist=maths.dist(bomb.x,bomb.y, xx,yy)
            if dist > bomb.r: continue
            
            thing=rog.thingat(xx, yy)
            if thing:
                if rog.on(thing,DEAD): continue
                
                if thing.isCreature:
                    decay=bomb.dmg/bomb.r
                    dmg= bomb.dmg - round(dist*decay) - thing.stats.get('arm')
                    rog.hurt(thing, dmg)
                    if dmg==0: hitName="not damaged"
                    elif rog.on(thing,DEAD): hitName="killed"
                    else: hitName="hit"
                    rog.msg("{t}{n} is {h} by the blast.".format(
                        t=thing.title,n=thing.name,h=hitName) )
                else:
                    # explode any bombs caught in the blast
                    if (thing is not bomb
                            and hasattr(thing,'explode')
                            and dist <= bomb.r/2 ):
                        thing.timer=0
























''' SCRIPT TO SHOW BOMB DAMAGE AND DECAY

            decay=bomb.dmg/bomb.r
            dmg= bomb.dmg - round(dist*decay)
            libtcod.console_put_char_ex(con, xx, yy, chr(dmg+48), WHITE,BLACK)
            
    libtcod.console_blit(con,rog.view_x(),rog.view_y(),rog.view_w(),rog.view_h(),
                         0,rog.view_port_x(),rog.view_port_y())
    libtcod.console_flush()
    r=rog.Input(0,0,mode="wait")
    '''


'''if (not killed and not hpmax_before == dfndr.stats.hpmax):
            x=", injuring {pronoun}".format(pronoun=pronoun)
'''

'''
#TEST
if (obj.x==x and obj.y==y):
    obj.stats.sight +=1
    if obj.stats.sight >= 9:
        obj.stats.sight=9
else: obj.stats.sight = 5
#'''
