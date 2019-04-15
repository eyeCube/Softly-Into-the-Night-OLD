'''
    stuff.py
    inanimate tts to populate the world
'''

from const import *
import rogue as rog
import thing

def create(name):
    if name=="wood":
        return wood()
    elif name=="blood":
        return blood()

def blood(x,y):
    tt = tt()
    tt.x = x
    tt.y = y
    tt.mask = chr(T_FLUID)
    tt.name = 'blood'
    tt.color=COL['dkmagenta']
    tt.stats.reselec=75
    tt.stats.resfire=50
    tt.stats.resbio=25
    rog.register_inanimate(tt)
    return tt

def wood(x,y):
    tt=tt()
    tt.name="wood"
    tt.mask=chr(15)
    tt.material=MAT_WOOD
    tt.x=x
    tt.y=y
    tt.mass=20
    tt.stats.hp=1250
    tt.color=COL['brown']
    
    rog.register_inanimate(tt)
    return tt

