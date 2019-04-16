'''
    tilemap.py

    Contents:
      - class Map

'''

import time
import numpy as np
import libtcodpy as libtcod
import random
import math

import rogue as rog
from const import *
import maths
import misc
import monsters
import dice
from colors import COLORS as COL






IDENTIFIER = {
    ord(' ')        : "nothing.",
    T_FLOOR         : "a floor.",
    T_WALL          : "a wall.",
    T_STAIRDOWN     : "a staircase leading down.",
    T_STAIRUP       : "a staircase leading up.",
    T_FOOD          : "some foodstuffs.",
    T_ROCK          : "a rock or stone.",
    T_CORPSE        : "a corpse or skeleton.",
    ord("?")        : "a silhouette or light.",
    }
for k,v in monsters.bestiary.items():
    if isinstance(k, str):
        IDENTIFIER.update({ord(k) : v[0]})
    else:
        IDENTIFIER.update({k : v[0]})




#
#   Tile
#

class Tile():

    # terrains
    # args:
        # typ: character ASCII code
        # foreground color
        # background color
        # energy required to enter tile -- value 0 indicates impassible
        # additional energy required to leave tile
        # blocks sight
        # volume dampen value
        # ---blocks smell---Not used
        #

    def __init__(self, typ, fg,bg,
                 nrg_enter,nrg_leave,opaque,volume_dampen):
        
        self.char=typ
        self.fg=fg
        self.bg=bg
        self.nrg_enter=nrg_enter
        self.nrg_leave=nrg_leave
        self.opaque=opaque
        self.dampen=volume_dampen


TILES={         #                   fgcolor ,bg, costEnterLeave,opaque,damp
    T_FLOOR     : Tile(T_FLOOR,       'neutral', 'deep',    100,0,  False,1,),
    T_WALL      : Tile(T_WALL,        'orange', 'dkred',   0,  0,  True, 201,),
    T_STAIRDOWN : Tile(T_STAIRDOWN,   'accent', 'purple',  100,0,  False,2,),
    T_STAIRUP   : Tile(T_STAIRUP,     'accent', 'purple',  100,0,  False,2,),
    }
        
'''class Floor(Tile):
    def __init__(self, *args,**kwargs):
        super(Floor, self).__init__(*args,**kwargs)'''


    
class TileMap():

    def __init__(self,w,h):

        self.w = w
        self.h = h
        
            # Init root FOVmap
        self.fov_map = libtcod.map_new(w,h)

        self.con_memories = libtcod.console_new(w,h)
        self.con_map_state = libtcod.console_new(w,h)

        baseTemp=32 # room temperature
        self.grid_things =      [ [ [] for y in range(h)] for x in range(w) ]
        self.grid_terrain =     [ [ None for y in range(h)] for x in range(w) ]
        self.grid_lights=       [ [ [] for y in range(h)] for x in range(w) ]
        self.lightmap_init()
        for x in range(w):
            for y in range(h):
                self.tile_change(x,y,T_WALL)

        self.question_marks = []
    #

    #
    def COPY(self, tilemap): #copy a TileMap object into another
        for k,v in tilemap.__dict__.items():
            self.__dict__.update({k:v})

    
    def tile_change(self, x,y, typ):
        self.grid_terrain[x][y] = TILES[typ]
        libtcod.map_set_properties( self.fov_map, x, y,
            (not self.get_blocks_sight(x,y)), True)
        # UPDATE ALL FOVMAPS OF ALL CREATURES !!!!!!!!
    #
    
    def get_char(self,x,y):             return self.grid_terrain[x][y].char
    def get_color(self,x,y):            return COL[ self.grid_terrain[x][y].fg ]
    def get_bgcolor(self,x,y):          return COL[ self.grid_terrain[x][y].bg ]
    def get_blocks_sight(self,x,y):     return self.grid_terrain[x][y].opaque
    def get_nrg_cost_enter(self,x,y):   return self.grid_terrain[x][y].nrg_enter
    def get_nrg_cost_leave(self,x,y):   return self.grid_terrain[x][y].nrg_leave

    def get_audio_dampen(self,x,y):     return self.grid_terrain[x][y].dampen
    def nthings(self,x,y):              return len(self.grid_things[x][y])
    def thingat(self,x,y):
        lis = self.grid_things[x][y]
        return lis[-1] if lis else None
    def inanat(self,x,y):    # inanimate thing at tile
        thing=self.thingat(x,y)
        if not thing: return None
        gridTile=self.grid_things[x][y]
        if (thing.isCreature and len(gridTile) > 1):
            thing=gridTile[-2]
            if thing: return thing
        else: return thing
    def monat (self,x,y):    # get monster in tile (only 1 mon per tile is allowed at a time. Monster is always on top of list i.e. appended to end.)
        thing = self.thingat(x,y)
        return thing if (thing and thing.isCreature ) else None
    def solidat(self,x,y):    # get solid thing in tile i.e. things that cannot be moved through... only 1 allowed per tile
        thing = self.thingat(x,y)
        return thing if (thing and thing.isSolid ) else None
    def lightsat(self,x,y):
        return self.grid_lights[x][y]
    
    def identify_symbol(self,symbol):
        return IDENTIFIER.get(symbol,"unknown")
    #


    def discover_place(self, x,y,obj=None):
        thing = self.thingat(x,y)
        if thing and not thing.isCreature:
            libtcod.console_put_char_ex(self.con_memories, x,y, thing.mask,
                                        COL['dkgray'], COL['black'])
        else:
            libtcod.console_put_char_ex(self.con_memories, x,y, self.get_char(x,y),
                                        COL['dkgray'], COL['black'])
    
    def create_memories(self, pc):
        
        rang = pc.stats.sight
        for x in     range( max(0, pc.x-rang), min(self.w, pc.x+rang+1) ):
            for y in range( max(0, pc.y-rang), min(self.h, pc.y+rang+1) ):
                
                if rog.can_see(pc,x,y):
                    self.discover_place(x,y,self.inanat(x,y))
    

    def render_gameArea(self, pc, view_x,view_y,view_w,view_h):
        self.create_memories(pc)
        
        self.recall_memories( view_x,view_y,view_w,view_h)
        
        self.draw_distant_lights(pc, view_x,view_y,view_w,view_h)
        self.draw_what_player_sees(pc)
        return self.con_map_state
            
    def draw_what_player_sees(self, pc):
        
        rang=pc.stats.sight
        for     x in range( max(0, pc.x-rang), min(self.w, pc.x+rang+1) ):
            for y in range( max(0, pc.y-rang), min(self.h, pc.y+rang+1) ):
                canSee=False
                
                if not rog.in_range(pc.x,pc.y, x,y, rang):
                    continue
                if not libtcod.map_is_in_fov(pc.fov_map, x,y):
                    continue
                thing=self.thingat(x, y)
                if (not rog.on(pc,NVISION) and self.get_light_value(x,y) == 0):
                    self.draw_silhouettes(pc, x,y, thing)
                    continue
                
                if thing:
                    libtcod.console_put_char(
                        self.con_map_state, x,y,
                        thing.mask)
                    libtcod.console_set_char_foreground(
                        self.con_map_state, x,y, thing.color)
                    self.apply_rendered_bgcol(x,y, thing)
                else:
                    libtcod.console_put_char_ex(self.con_map_state, x,y,
                        self.get_char(x, y),
                        self.get_color(x, y), self.get_bgcolor(x, y))

    def draw_distant_lights(self, pc, view_x,view_y,view_w,view_h):
        for light in rog.list_lights():
            lx=light.x
            ly=light.y
            if (lx == pc.x and ly == pc.y): continue
            if not (lx >= view_x
                    and ly >= view_y
                    and lx <= view_x + view_w
                    and ly <= view_y + view_h
            ): continue
            libtcod.line_init(pc.x,pc.y, lx,ly)
            canSee=True
            while True:
                x,y=libtcod.line_step()
                if x == None: break;
                if self.get_blocks_sight(x,y): canSee=False;break;
            if canSee:
                libtcod.console_put_char(self.con_map_state, lx,ly, "?")
    
    def draw_silhouettes(self, pc, tx,ty, thing):
    #   extend a line from tile tx,ty to a distant tile
    #   which is in the same direction from the player.
    #   Check for lit tiles, and if we find any along the way,
    #   draw a silhouette for the location of interest.
    #   Basically, if the obj is backlit, you can see
    #   a silhouette.
        if not (thing and thing.isCreature): return
        
        dist=maths.dist(pc.x,pc.y, tx,ty)
        dx=(tx - pc.x)/dist
        dy=(ty - pc.y)/dist
        xdest=tx + int(dx*pc.stats.sight)
        ydest=ty + int(dy*pc.stats.sight)
        libtcod.line_init(tx,ty, xdest,ydest)
        while True:
            x,y=libtcod.line_step()
            if x == None: return
            if maths.dist(pc.x,pc.y, x,y) > pc.stats.sight: return
            if self.get_blocks_sight(x,y):  return
            if self.get_light_value(x,y):
                libtcod.console_put_char(self.con_map_state, tx,ty, "?")
                return

    # get and apply the proper background color
    #   for the tile containing a thing
    def apply_rendered_bgcol(self, x, y, thing):
        bgTile=self.get_bgcolor(x, y)
        if thing and rog.on(thing,FIRE):
            choices=['gold','orange','trueyellow']
            bgCol=COL[choices[dice.roll(len(choices)) - 1]]
        elif (self.get_char(x,y) == T_STAIRDOWN
                or self.get_char(x,y) == T_STAIRUP ):
            bgCol=bgTile
        elif self.nthings(x, y) >= 2: bgCol=COL['dkgreen']
        elif thing==rog.pc():
            if rog.settings().highlightPC:
                bgCol=COL[rog.settings().highlightColor]
            else: bgCol=thing.bgcolor
        elif thing: bgCol=thing.bgcolor
        else: bgCol=bgTile
        libtcod.console_set_char_background(
            self.con_map_state, x,y, bgCol)
        
    def get_map_state(self):
        self.recall_memories( 0,0,ROOMW,ROOMH)
        view=rog.Ref.view
        self.draw_what_player_sees(rog.Ref.pc)
        return self.con_map_state

    def recall_memories(self, view_x,view_y, view_w,view_h):
        libtcod.console_blit(self.con_memories, view_x,view_y,view_w,view_h,
                             self.con_map_state, view_x,view_y)
    
    # A* paths wrappers

    def path_new_movement(self, pathData):
        return libtcod.path_new_using_function(
            ROOMW, ROOMH, self.path_get_cost_movement,
            pathData, 1.41 )
    def path_new_sound(self, pathData):
        return libtcod.path_new_using_function(
            ROOMW, ROOMH, self.path_get_cost_sound,
            pathData, 1.41 )
    
    def path_delete(self, path):    libtcod.path_delete(path)
    # path data functions
    def path_get_cost_movement(self,xFrom,yFrom,xTo,yTo, data):
        return self.get_nrg_cost_enter(xTo,yTo) + self.get_nrg_cost_leave(xFrom,yFrom)
    def path_get_cost_sound(self,xFrom,yFrom,xTo,yTo, data):
        return self.get_audio_dampen(xTo,yTo)

    # lighting map

    def lightmap_init(self):
        self.grid_lighting=np.full((self.w,self.h), 0)
    def tile_lighten(self, x, y, value):
        self.grid_lighting[x][y] += value
    def tile_darken(self, x, y, value):
        self.grid_lighting[x][y] = max(0, self.grid_lighting[x][y] - value)
    def tile_set_light_value(self, x, y, value):
        self.grid_lighting[x][y]=value
    def get_light_value(self, x, y):
        return self.grid_lighting[x][y]











'''

    # temperature map
    def get_temperature(self,x,y):      return self.grid_temperature[x][y]

    def temperature_disperse(self):
        new=np.full((self.w,self.h), 0)
        for x,cols in enumerate(self.grid_temperature):
            for y,tile in enumerate(cols):
                xf=max(0, x - 1)
                yf=max(0, y - 1)
                xt=min(ROOMW - 1, x + 1)
                yt=min(ROOMH - 1, y + 1)
                for xx in range(xf,xt + 1):
                    for yy in range(yf, yt + 1):
                        give=tile/9
                        new[xx][yy] += give'''
                    
'''SHOW LIGHTING
libtcod.console_put_char(
                    self.con_map_state, x,y,
                    chr(light+48))'''

                
'''
        # draw terrain #
        for xx in range(view_w):
            for yy in range(view_h):

                x = xx + view_x
                y = yy + view_y
                
                if libtcod.map_is_in_fov(pc.fov_map,x,y):
                    
                    thing = self.thingat(x,y)
                    if thing:
                        tilething = thing if not thing.isCreature else None
                        self.discover_place(x,y,tilething)
                        libtcod.console_put_char_ex(con,x,y,
                            thing.mask, thing.color, thing.bgcolor)
                    else:
                        self.discover_place(x,y)
                        libtcod.console_put_char_ex(con,x,y,
                            self.get_discovered(x,y),
                            self.get_color(x,y), self.get_bgcolor(x,y))
                else:
                    libtcod.console_put_char_ex(con,x,y,
                        self.get_discovered(x,y),
                        DKGRAY, BLACK)
            # end for
        # end for
        #
        if pc.stats.sight ==0:
            self.discover_place(pc.x,pc.y)
            libtcod.console_put_char_ex(con, pc.x-view_x,pc.y-view_y,
                pc.mask, pc.color, pc.bgcolor)'''


'''
    @classmethod
    def update_fovmap_property(cls, x,y, value):
    # When something in the tile map changes,
    # This function must be called.
    
        libtcod.map_set_properties( cls.fov_map, xx, yy,
            value, True)

    @classmethod
    def compute_fovmap(cls,sight,x,y):
        
        libtcod.map_compute_fov( cls.fov_map, x,y,sight,
                                light_walls = True,
                                 algo=libtcod.FOV_RESTRICTIVE)
        
        return cls.fov_map
    '''

'''


entity command look():
    free action, passive action
    fovmap = compute_fovmap(


def compute_fovmap(sight,x,y,w,h):
    create map from libtcod
    for every tile in grid
        figure out if the tile can be seen through by the calling entity
        add itself to the map

        

    
    def __init__(self, w, h):
        self.width = w
        self.height = h
        
    def create_terrainmap(self):
        self.tmap = [[for j]
    
    def get_fovmap(self, x, y):
        smap = libtcod.map_new(self.width,self.height)
        blocks = self.map[x][y][1]
        
        

'''
