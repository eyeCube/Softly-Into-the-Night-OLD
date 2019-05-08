'''
    items.py
    
'''

import rogue as rog


# Inventory class
# stores items
# WARNING: do not allow items to change their mass while inside an inventory.
#   remove the items, alter them, then put them back in the inventory.
class Inventory:
    def __init__(self, size):
        self.size=size      #maximum mass capacity
        self.totalMass = 0  #current amount of mass stored in the inventory
        self.data=[]
    def __iter__(self):
        yield from self.data
    @property
    def items(self): return self.data
    def add(self, item): #try to add an item. Return success
        if self.totalMass + item.mass <= self.size: #check if enough room
            self.data.append(item)
            self.totalMass += item.mass
            return True
        else:
            return False
    def remove(self, item): #try to remove an item. Return success
        if item in self.data:
            self.data.remove(item)
            self.totalMass -= item.mass
            return True
        else:
            return False



#-----------#
# Functions #
#-----------#


def can_be_used(item):
    return rog.on(item,CANUSE)










