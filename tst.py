_menuList = ['a','b','c','d']
import dice
choice = dice.roll(len(_menuList))
print(_menuList[choice-1])
