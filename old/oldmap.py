











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
