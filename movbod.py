import glob

import pygame

from sprite import Sprite


class Moving_body():
    def __init__(self):
        self.x=0 #position en pixels du coin inf gauche
        self.y=0
        self.sprites=dict() #dictionnaire de sprites contenant les actions possibles
        self.actions=self.sprites.keys()
        self.action='Idle'
        self.moving=False
        self.faceleft=False
        self.speed=5 #vitesse horizontale (nb de pixels à chaque appui)
        self.width=10
        self.height=10
        self.damage=0 #permet d'entrer en collision sans enlever de vie

    def add_sprites(self,directory):
        '''charger les sprites situés dans le répertoire dic'''
        actions_files=glob.glob("{}/*(1).png".format(directory))
        spritesdic=dict()
        for file in actions_files:
            action=file.split(' ')[0].split('\\')[1]
            sprite=Sprite(action,directory)
            sprite.animslowingfact=3
            spritesdic[action]=sprite
        self.sprites=spritesdic
        self.sprite=spritesdic[self.action]
        self.actions=self.sprites.keys()

    def kill(self):
        for sprite in self.sprites.values():
            sprite.kill()
    
    def change_size(self,reducratio):
        '''change la taille de tous les sprites'''
        for action in self.actions:
            self.sprites[action].change_size(reducratio)

    def change_animspeed(self,animspeed,spritesaction=[]):
        '''change la vitesse danim pour les sprites dde la liste spritesaction
        ou pour tous si pas d'argument ou liste vide'''
        if spritesaction:
            for sprite in spritesaction:
                self.sprites[sprite].animslowingfact=animspeed
        else:
            for sprite in self.sprites.values():
                sprite.animslowingfact=animspeed

    def change_action(self,action):
        self.action=action
        self.sprite=self.sprites[self.action]
        self.sprite.index=0
    def go_left(self):
        if self.action!='Walk' and self.action!='Jump':
            self.change_action('Walk')
        self.moving=True
        self.faceleft=True
        self.update()
    def go_right(self):
        if self.action!='Walk' and self.action!='Jump':
            self.change_action('Walk')
        self.moving=True
        self.faceleft=False
        self.update()
    
    def stop(self):
        if self.action!='Idle' and self.action!='Jump':
            self.change_action('Idle')
        self.moving=False
        self.update()

    def hit_right(self,world):
        pass
    def hit_left(self,world):
        pass

    def update(self):  
        if self.moving:
            if self.faceleft:
                self.x-=self.speed
            else:
                self.x+=self.speed
        if self.action=='Jump':
            if self.jumpcount<self.jumptop:
                self.y-=self.speed
            elif self.jumpcount>self.jumptop:
                if self.y<self.startingalt:
                    self.y+=self.speed
                elif self.moving:
                    self.change_action('Walk')
                else:
                    self.change_action('Idle')
            self.jumpcount+=1
        self.sprite.update_img(self.faceleft)
        self.width=self.sprite.recttight[2]
        self.height=self.sprite.recttight[3]
        self.sprite.update_pos(self.x,self.y) #position coin inf gauche

class Bullet(Moving_body):
    '''Pour les projectiles, détruits quand ils sortent de l'écran'''
    #####
    # Faire une classe enemy et des sous classe pour chaque type
    # Faire une sous classe hache de la classe bullet avec tout les paramètres
    #####
    def __init__(self,startx=0):
        super().__init__()
        self.x=startx
        self.moving=True
        self.action='Walk'
        self.damage=1 #Damage en cas de collision
    def hit_right(self,world):
        self.kill()
        world.movbods.remove(self)
    def hit_left(self,world):
        self.kill()
        world.movbods.remove(self)
    
    def update(self):  
        if self.moving:
            if self.faceleft:
                self.x-=self.speed
            else:
                self.x+=self.speed
        self.sprite.update_img(self.faceleft)
        self.width=self.sprite.recttight[2]
        self.height=self.sprite.recttight[3]
        self.sprite.update_pos(self.x,self.y) #position coin inf gauche

#A mettre dans un autre fichier à partir d'ici
class Character(Moving_body):
    def __init__(self):
        super().__init__()
        self.jumptop=25  #hauteur du saut en nombre de speed 25
        self.life=10
        self.hitable=True
        self.invicible_clock=0
        self.invicible_time=500 # une demi seconde
    def jump(self):
        if self.action!='Jump':
            self.change_action('Jump')
            self.jumpcount=0
            self.startingalt=self.y #plus tard sera remplacé par des tests de collision
        self.update()
    def update(self):  
        if self.moving:
            if self.faceleft:
                self.x-=self.speed
            else:
                self.x+=self.speed
        if self.action=='Jump':
            if self.jumpcount<self.jumptop:
                self.y-=self.speed
            elif self.jumpcount>self.jumptop:
                if self.y<self.startingalt:
                    self.y+=self.speed
                elif self.moving:
                    self.change_action('Walk')
                else:
                    self.change_action('Idle')
            self.jumpcount+=1
        self.sprite.update_img(self.faceleft)
        self.width=self.sprite.recttight[2]
        self.height=self.sprite.recttight[3]
        self.sprite.update_pos(self.x,self.y) #position coin inf gauche

        current_time=pygame.time.get_ticks() 
        if current_time-self.invicible_clock>self.invicible_time: #Pour gérer le temps invicible
            self.hitable=True
            self.invicible_clock=0
        if not self.hitable: #Pour indiquer qu'on est invicible
            self.sprite.image.set_alpha(100)
        else:
            self.sprite.image.set_alpha(255)


class Player(Character):
    def __init__(self):
        super().__init__()
    def hit_right(self,world):
        self.x-=self.speed
        self.sprite.recttight[0]=self.x
        # self.sprite.recttight[1]=self.y
        self.sprite.update(faceleft=False)
    def hit_left(self,world):
        self.x+=self.speed
        self.sprite.recttight[0]=self.x
        # self.sprite.recttight[1]=self.y
        self.sprite.update(faceleft=True)

class Lucky(Player):
    def __init__(self):
        super().__init__()
        # self.add_sprites('spirit')
        self.add_sprites('avgirl')
        self.change_size(1.8)
        self.jumptop=20
        self.speed=15

class Abigaelle(Player):
    def __init__(self):
        super().__init__()
        # self.add_sprites('gdton')
        self.add_sprites('png')
        self.change_size(1.8)
        # self.change_animspeed(10,['Jump'])
        self.jumptop=20
        self.speed=15