'''
    fluids
'''

import thing

class Fluid(thing.Thing):

    def __init__(self):
        super(Fluid, self).__init__()

        self.viscosity=1

class Smoke(Fluid):

    def __init__(self, x,y):
        super(Smoke,self).__init__()
        
        self.x=x
        self.y=y
        self.name="smoke"
        self.type=' '
        self.mask=self.type
        self.mass=0.01
        self.viscosity=.1


def fluids_flow():
    pass
