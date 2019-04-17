'''
    stuff.py
    inanimate tts to populate the world
'''

from const import *
import rogue as rog
import thing



def gore(x,y):
    tt = thing.Thing(x,y,_type=chr(T_FLUID),name='hunk of meat',color=COL['dkmagenta'])
    tt.mass=1
    rog.register_inanimate(tt)
    return tt

def wood(x,y):
    tt=thing.Thing(x,y,_type=chr(15),name="wood",color=COL['brown'],material=MAT_WOOD)
    tt.mass=20
    tt.stats.hpmax=20
    rog.givehp(tt)
    rog.register_inanimate(tt)
    return tt

def corpseShroom(x,y):
    tt=thing.Thing(x,y,_type=chr(T_FUNGUS),name="corpiscle",color=COL['red'],material=MAT_FUNGUS)
    tt.mass=2
    tt.stats.hpmax=1
    rog.givehp(tt)
    rog.register_inanimate(tt)
    return tt
