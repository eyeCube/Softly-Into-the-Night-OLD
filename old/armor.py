
import const

ARMR = T_ARMOR
HELM = T_HELMET

FLSH = MAT_FLESH
LETH = MAT_LEATHER
CLTH = MAT_CLOTH
WOOD = MAT_WOOD
BONE = MAT_BONE
CARB = MAT_CARBON
PLAS = MAT_PLASTIC
METL = MAT_METAL

#GEAR
    #Columns:
    #   $$$$$   cost
    #   KG      mass
    #   Dur     durability
    #   Mat     material
    #   DV      Dodge Value
    #   AV      Armor Value
    #   Msp     Move Speed
    #   Vis     Vision
    #   FIR     Fire Resist
    #   BIO     Bio Resist
    #
GEAR = {
#--Name-----------------------Type,$$$$$, KG,   Dur, Mat, (DV, AV, MSp, Vis,FIR,BIO,)
    #Armor
"Skin Suit"                 :(ARMR,450,   15.0, 90,  FLSH,( 2,  2, -9,   0,  0,  10,), ),
"Boiled Leather Plate"      :(ARMR,975,   12.0, 180, LETH,(-1,  4, -6,   0,  5,  5,), ),
"Cloak"                     :(ARMR,520,   6.0,  150, CLTH,( 4,  1, -3,   0,  10, 10,), ),
"Wood Armor"                :(ARMR,610,   19.0, 160, WOOD,(-6,  5, -12,  0, -10, 10,), ),
"Bone Armor"                :(ARMR,3490,  28.0, 475, BONE,(-4,  7, -18,  0,  15, 10,), ),
"Carbide Armor"             :(ARMR,8250,  22.5, 400, CARB,(-3,  8, -12,  0,  20, 20,), ),
"Metal Gear"                :(ARMR,74990, 27.5, 1200,METL,(-4,  10,-18,  0,  5,  5,), ),
"Full Metal Suit"           :(ARMR,125000,35.0, 1200,METL,(-5,  12,-21,  0,  5,  10,), ),
"Hazard Suit"               :(ARMR,69445, 40.0, 75,  PLAS,(-12, 3, -40,  0,  30, 50,), ),
"Wetsuit"                   :(ARMR,5600,  8.0,  50,  PLAS,( 0,  0, -6,   0,  30, 5,), ),
"Fire Blanket"              :(ARMR,1400,  12.0, 135, CLTH,(-3,  1, -9,   0,  30, 15,), ),
"Burn Jacket"               :(ARMR,8500,  20.0, 180, CLTH,(-5,  2, -12,  0,  50, 15,), ),
    #Helmets
"Bandana"                   :(HELM,40,    0.1,  30,  CLTH,( 2,  0,  0,   0,  5,  10,), ),
"Skin Mask"                 :(HELM,180,   1.25, 20,  FLSH,( 1,  1,  0,  -1,  0,  5,), ),
"Wood Mask"                 :(HELM,60,    1.0,  60,  WOOD,(-1,  1, -3,  -1, -5,  5,), ),
"Skull Helm"                :(HELM,1950,  2.8,  125, BONE,(-3,  2, -6,  -2,  5,  5,), ),
"Carbide Mask"              :(HELM,4850,  1.8,  225, CARB,(-1,  2, -3,  -2,  5,  10,), ),
"Carbide Helm"              :(HELM,8450,  2.5,  250, CARB,(-2,  3, -6,  -2,  10, 10,), ),
"Metal Mask"                :(HELM,11000, 2.2,  375, METL,(-3,  4, -3,  -2,  0,  5,), ),
"Metal Helm"                :(HELM,13500, 3.0,  500, METL,(-4,  5, -6,  -2,  0,  5,), ),
"Gas Mask"                  :(HELM,19450, 2.5,  40,  PLAS,(-2,  1, -3,  -2,  10, 30,), ),
"Respirator"                :(HELM,6490,  1.7,  35,  PLAS,(-3,  0, -6,   0,  20, 15,), ),

    }






















