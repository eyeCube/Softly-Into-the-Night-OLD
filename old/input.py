























''' Adding volume from similar sound types... maybe not the best idea!???
            newVol=round(ev.volume*0.2) + cVol
            self.sounds.update({k : (newVol, lis,)})'''
            #n=misc.get_num_from_char(key.text.decode())

'''
class InputManager():
    def __init__(self,x,y,w,h,default,mode):
        # init
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.default = default
        self.mode = mode
        self.init_time   = time.time()
        
        self.text        = default   # displayed string
        self.field       = []        # string of letters from which 'text' is created
        for letter in text: self.field.append(letter)
        
        self.update          = True
        self.update_text     = True
        self.update_clear    = False
        
        self.console         = libtcod.console_new(w, h)
        # cursor
        self.cursor = Cursor()
        self.cursor_type         = 0         # options to change cursor display
        self.cursor_blink_delay  = 0.30      # seconds
        self.cursor_blink_time   = 0         # timestamp for blinking cursor
        self.cursor_pos          = len(field)
        self.cursor_visible      = True
        self.insert_mode         = False


    def update(self):
        if self.update:

            if self.update_text:
                self.text = ''.join(self.field)
                if self.update_clear:   libtcod.console_clear(self.console)
                libtcod.console_print_ex(self.console,0,0,
                    libtcod.BKGND_NONE,libtcod.LEFT, self.text)
            
                libtcod.console_blit(self.console, 0,0, self.w,self.h,
                                     0, self.x,self.y)
            
            cursor.setpos(self.x+self.cursor_pos,self.y)
            cursor.draw()
            
            libtcod.console_flush()
            update = clear_text = update_text = False


    def get_input(self):
        reply = None
        if libtcod.console_is_key_pressed(key.vk):
            reply = VK_TO_CHAR.get(key.vk, None)
        
        elif key.vk == libtcod.KEY_TEXT:
            decoded = key.text.decode()
            if (ord(decoded) >= 128 or decoded == '%'):
                continue    # Prevent weird error-causing ASCII input
            else: reply = decoded
        return reply


    def process_input(self,reply):
        
        if reply:

            # wait mode #
            
            if mode=="wait": return reply
            
            # Update screen and reset cursor blinker
            update= update_text= update_clear= cursor_visible= True # let user know their input was received
            cursor_blink_time = time.time() + cursor_blink_delay #  doing a longer cursor blink than usual

            # text mode #
            
            if mode=="text":
                if time.time() - init_time < .05: continue  # get rid of any input in the buffer
                #
                # special input functions
                #
                if libtcod.console_is_key_pressed(key.vk):
                    
                    ans = ord(reply)
                    if (ans == K_ENTER):    break
                    if (ans == K_ESCAPE):   break
                
                    if (ans == K_BACKSPACE) :
                        clear_text = True
                        if (cursor_pos == w - 1 and len(field) == w):
                            del field[ cursor_pos]  # Then acts like delete
                        elif (cursor_pos > 0 and len(field) >= cursor_pos) :
                            del field[ cursor_pos - 1]
                            cursor_pos -= 1
                            
                    elif (ans == K_DELETE) :
                        clear_text = True
                        if len(field) > cursor_pos: del field[ cursor_pos]
                    
                    elif (ans == K_LEFT) :
                        if cursor_pos > 0:  cursor_pos -= 1
                        
                    elif (ans == K_RIGHT) :
                        if (cursor_pos < w - 1 and cursor_pos < len(field)):
                            cursor_pos += 1
                    
                    elif (ans == K_INSERT) :            
                        insert_mode = not insert_mode
                #
                # text input
                #
                elif key.vk == libtcod.KEY_TEXT:
                    
                            # insert mode
                            
                    if ( len(field)==w or insert_mode ) :
                        if len(field) - 1 < cursor_pos:
                            field.append(reply)
                        else:
                            field[cursor_pos] = reply
                            
                            # normal mode
                    else:   
                        first_half = field[:cursor_pos]
                        second_half = field[cursor_pos:]
                        field = []
                        for c in first_half:
                            field.append(c)
                        field.append( reply)
                        for c in second_half:
                            field.append(c)
                    
                    # move cursor
                    if cursor_pos < w - 1:
                        cursor_pos +=1
                    #
                #
            #
        #

            
    def run(self):
            
        while True:
            
            libtcod.sys_sleep_milli(5) # checking for input 200 times per second is enough so just sleep a little
            
            time_stamp = time.time()
            if time_stamp - cursor_blink_time >= cursor_blink_delay:
                cursor_blink_time = time_stamp
                update = True
                cursor_visible = not cursor_visible
            
            self.update()
            
            
            # Check for keyboard event
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS,key,mouse)
            
            self.process_input(self.get_input())
            
        # end while

        
        return text



'''



