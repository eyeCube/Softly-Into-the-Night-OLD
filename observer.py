#
# observer
#


import rogue as rog






# generic classes #


class Observer():
    def update(self):
        pass


class Observable():
    
    def __init__(self):
        super(Observable,self).__init__()
        
        self.observers = []
        
    def observers_notify(self, *args,**kwargs):
        for observer in self.observers:
            observer.update(*args,**kwargs)
            
    def observer_add(self,obs):     self.observers.append(obs)
    def observer_remove(self,obs):  self.observers.remove(obs)
    def observers_delete(self):     self.observers = []



# specific observers #


class Observer_playerChange(Observer):
    def update(self, *args,**kwargs):
        super(Observer_playerChange, self).update()
        '''if not args: return
        print(args)
        if (args[0] == 'x'
            or args[0] == 'y'
            or args[0] == 'stats.nrg'
        ): '''
        rog.update_game()
        rog.update_hud()
        


























