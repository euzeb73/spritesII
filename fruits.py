import pygame
from movbod import Bullet

class Fruitsdic():
    def __init__(self):
        self.bonus=dict()
        self.bonus['pomme']=1
        self.bonus['carotte']=2
        self.bonus['ananas']=5
        self.bonus['cerise']=4

class Fruits(Bullet):
    def __init__(self,name='pomme'):
        super().__init__()
        self.moving=False
        self.action='Idle'
        self.add_sprites(name)
        self.change_size(3)
        dic=Fruitsdic()
        self.damage=-1*dic.bonus[name]
        self.update()


        