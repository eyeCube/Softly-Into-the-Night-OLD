#
# ai
#
# functions for dealing with artificial intelligence
#

import math

import rogue as rog
from const import *
import maths
import action
import dice




#
# AI function
#
# choose and perform one action
#

def tick(obj):
    ai=obj.ai   # get ai function
    if not ai: return
    while obj.stats.nrg > 0:
        ai(obj)

#
# Monster desires to move in particular directions
#

class Desires():
    
    def __init__(self, default=0, wander=7):
        self.data=[
            [ default + dice.roll(wander) for j in range(3)]
            for i in range(3)
        ]
    def get(self,x,y):  return self.data[x+1][y+1]
    def add_for(self, x,y, val):        self.data[x+1] [y+1]  += val
    def add_against(self, x,y, val):
        self.data[-x+1][-y+1] += val
        # add desire to move AWAY from a direction. Implemented as
        # a positive desire in the opposite direction rather than
        # a negative desire in the given direction.
    


    
#AI - stateless
def stateless(bot):
    
    # desire to move in a particular coordinate
    desires=Desires(wander=7)

    # listen to events
    '''lis=rog.listen(bot)
    if lis:
        for ev in lis:
            if rog.can_see(bot,ev.x,ev.y):
                continue
            # hearing
            if not ev.volume: continue
            if rog.can_hear(bot, ev.x,ev.y, ev.volume):
                interest=5
                _add_desire_direction(
                    desires, bot.x,bot.y, ev.x,ev.y, interest)
        rog.clear_listen_events(bot)'''
    
    # iterate through each tile in sight and see what is there...
    # is there a better way to do this?
    sight=bot.stats.sight
    
    for x in range(     bot.x - sight,  bot.x + sight + 1 ):
        for y in range( bot.y - sight,  bot.y + sight + 1 ):
            if (not rog.is_in_grid(x,y) #out of bounds
                    or (x == bot.x and y == bot.y) ): #ignore self
                continue
            if not rog.can_see(bot,x,y): continue #bot can't see it
            
            here = rog.thingat(x,y)
            
            if here:
                
                # decide what it is and what to do about it
                if rog.is_creature(here):
                    if rog.on(here,DEAD): continue #no interest in dead things

                    interest=0

                    #desire to fight
                    if here.faction == FACT_ROGUE:
                        interest=1000
                    #desire to run away
                    #elif here.type == '@':
                    #   interest=-1000
                    #grouping behavior
                    elif here.type == bot.type:
                        interest = 5
                    if (interest > 0):
                        _add_desire_direction(
                            desires, bot.x,bot.y, x,y, interest
                            )
                    elif (interest < 0):
                        _add_fear_direction(
                            desires, bot.x,bot.y, x,y, interest
                            )
                #if thing is inanimate
                else:
                    #food desire if hungry
                    #treasure desire
                    pass
                
    # pick the direction it wants to move in the most
    highest=-999
    for i in range(3):
        for j in range(3):
            new=desires.get(j-1, i-1)
            if new > highest:
                highest=new
                coords=(j-1, i-1,)
    dx, dy =coords
    xto=bot.x + dx
    yto=bot.y + dy
    
    # out of bounds
    if not rog.is_in_grid(xto, yto):
        return
    
    # fight if there is a monster present
    mon = rog.monat(xto, yto)
    if (mon and mon is not bot):
        if not mon.type == bot.type: ##TEMPORARY
            action.fight(bot, mon)
            return
    # or move
    elif not rog.solidat(xto, yto):
        if action.move(bot, dx,dy):
            return

    # if no action was done, just wait
    action.wait(bot)



#LOCAL FUNCTIONS

#_add_desire_direction
# desire to move in the given direction
# desires = Desires object instance
# interest = amount that it cares about moving in this direction
def _add_desire_direction(desires, xf,yf, xt,yt, interest):
    if not interest: return
    dx,dy = _get_dir_xy(xf,yf,xt,yt)
    desires.add_for(dx,dy, interest)
#_add_fear_direction
# desire to move in the opposite direction
# desires = Desires object instance
# interest = amount that it cares about moving away from this direction
def _add_fear_direction(desires, xf,yf, xt,yt, interest):
    if not interest: return
    dx,dy = _get_dir_xy(xf,yf,xt,yt)
    desires.add_against(dx,dy, interest)
#_get_desire_xy
# return the direction from (xf,yf) to (xt,yt)
def _get_dir_xy(x1,y1,x2,y2):
    rads=maths.pdir(x1,y1, x2,y2)
    dx=round(math.cos(rads))
    dy=round(math.sin(rads))
    return (dx,dy,)
    

















