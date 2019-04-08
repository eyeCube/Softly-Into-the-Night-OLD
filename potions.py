'''
    potions
'''

import math

from const import *
import rogue as rog
import thing
from colors import COLORS as COL


MATMODS_ACID_DMG={
    MAT_FLESH   : 1
    MAT_FUNGUS  : 1
    MAT_VEGGIE  : 1
    MAT_STONE   : .1
    MAT_WOOD    : .25
    MAT_PAPER   : 1
    MAT_CLOTH   : .25
}


def makepot_acid():
    pot=thing.Thing()
    pot.type        = POTION
    pot.mask        = POTION
    pot.stats.hp    = 1
    pot.mass        = 0.2
    pot.color       = COL['yellow']
    pot.material    = MAT_GLASS
    pot.stats.resfire   = 90
    pot.stats.resbio    = 100
    rog.register_inanimate(pot)
    pot.quaff=quaff_acid
    return pot


def quaff_acid(pot, obj):
    if obj.material == MAT_IRON:
        rog.rust(obj)
        return
    dmg=10
    matMod=MATMODS_ACID_DMG.get(obj.material, 0)
    rog.se_add(obj, SE_GRADUALDMG, math.ceil(matMod*dmg))












