
from const import *


FLSH = MAT_FLESH
VEGG = MAT_VEGGIE
FUNG = MAT_FUNGUS

NASTY= TASTE_NASTY
BITTR= TASTE_BITTER
SWEET= TASTE_SWEET
SALTY= TASTE_SALTY
SAVOR= TASTE_SAVORY


#
# Columns:
#   $$$         cost
#   KG          mass
#   Mat         material
#   Taste       flag describing the flavor
#   Food        How many units of food recovery / hunger satiation
#   P           poison value
#   C           flag: Can be Cooked
#   S           flag: Can be Salted
#
FOOD = {
#--Name-------------------$$$,  KG,   Mat,  Taste,Food, Chew,P, C,S,
"Corpse Button"         :(1,    0.03, FUNG, NASTY,  1,   2,  3, 1,1,),
"Hack Leaf"             :(1,    0.02, VEGG, BITTR,  1,   2,  0, 1,1,),
"Juniper Berry"         :(3,    0.01, VEGG, SWEET,  1,   1,  0, 0,0,),
"Coke Nut"              :(12,   0.02, WOOD, BITTR,  2,   2,  1, 1,1,),
"Silly Fruit"           :(8,    0.04, VEGG, SWEET,  3,   1,  0, 0,0,),
"Mole Rat Meat"         :(10,   0.15, FLSH, SAVOR,  4,   3,  0, 1,1,),
"Dwarf Giant Cap"       :(25,   0.05, FUNG, SAVOR,  6,   3,  0, 0,1,),
"Eel Meat"              :(20,   0.50, FLSH, SAVOR,  9,   1,  0, 0,1,),
"Human Meat"            :(40,   1.00, FLSH, SAVOR,  10,  4,  1, 1,1,),
"Infant Meat"           :(80,   0.50, FLSH, SAVOR,  12,  2,  0, 1,1,),
"Giant Cap"             :(100,  0.35, FUNG, SAVOR,  20,  6,  0, 0,1,),
    }

























