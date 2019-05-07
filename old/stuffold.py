






'''
#gibs
def gore(x,y):
    tt = thing.Thing(x,y,_type=chr(T_GORE),name='hunk of meat',
                     color=COL['red'])
    tt.mass=1
    hp(tt, 1)
    rog.register_inanimate(tt)
    return tt

#wood
def sawdust(x,y):
    tt=thing.Thing(x,y,_type=chr(T_DUST),name="sawdust",
                   color=COL['brown'],material=MAT_SAWDUST)
    tt.mass=0.5
    hp(tt, 1)
    rog.register_inanimate(tt)
    return tt
def wood(x,y):
    tt=thing.Thing(x,y,_type=chr(T_WOOD),name="wood",
                   color=COL['brown'],material=MAT_WOOD)
    tt.mass=2
    hp(tt, 10)
    rog.register_inanimate(tt)
    return tt
def log(x,y):
    tt=thing.Thing(x,y,_type=chr(T_LOG),name="log",
                   color=COL['brown'],material=MAT_WOOD)
    tt.mass=20
    hp(tt, 100)
    rog.register_inanimate(tt)
    return tt

#flora
def tree(x,y):
    tt=thing.Thing(x,y,_type=chr(T_TREE),name="tree",
                   color=COL['green'],material=MAT_WOOD)
    tt.mass=200
    hp(tt, 30)
    rog.init_inventory(tt)
    giveRandom(tt, wood, 1, 6)
    rog.register_inanimate(tt)
    return tt
def corpseShroom(x,y):
    tt=thing.Thing(x,y,_type=chr(T_FUNGUS),name="corpiscle",
                   color=COL['red'],material=MAT_FUNGUS)
    tt.mass=2
    hp(tt, 1)
    _food(tt, 10)
    rog.register_inanimate(tt)
    return tt

#containers
def jug(x,y):
    tt=thing.Thing(x,y,_type=chr(T_BOTTLE),name="empty jug",
                   color=COL['brown'],material=MAT_GLASS)
    tt.mass=1
    hp(tt, 1)
    rog.init_fluidContainer(tt, 10)
    rog.register_inanimate(tt)
    return tt
'''









