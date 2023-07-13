import pygame
import random
from movbod import Bullet
from fruits import Fruits,Fruitsdic

class World():
    def __init__(self,player):
        self.players=[]
        self.movbods=[] #Moving bodies
        self.ground=700
        self.add_player(player)
        self.bg='field.jpeg'
        # self.bg='fond.jpg'
        self.enemyclock=pygame.time.get_ticks() #time in ms
        self.enemyperiod=2000 #en ms la période moyenne pour spwan les ennemis
        self.bonusclock=pygame.time.get_ticks() #time in ms
        self.bonusperiod=self.enemyperiod*5 #en ms la période moyenne pour spwan les ennemis
        
    def add_movbod(self,movbod):
        self.movbods.append(movbod)
    
    def add_player(self,player):        
        n=len(self.players)
        if n<2:
            self.players.append(player)
        player.x=0
        player.y=self.ground
        self.add_movbod(player)
        

    def generate_enemies(self,screen):
        current_time=pygame.time.get_ticks() #time in ms
        if current_time - self.enemyclock>random.gauss(self.enemyperiod,self.enemyperiod*0.1):            
            self.enemyclock=current_time
            #####
            # Faire une classe enemy et des sous classe pour chaque type
            # Faire une sous classe hache de la classe bullet avec tout les paramètres
            #####
            ax=Bullet()
            self.add_movbod(ax)
            ax.add_sprites('hache')
            ax.change_size(1.25) #taille
            ax.change_animspeed(4) #un peu moins vite
            height=ax.sprite.recttight[3]
            width=ax.sprite.recttight[2]
            ax.y=min(self.ground-random.gauss(height,0.3*height),self.ground)
            ax.x=screen.width-width
            ax.faceleft=True
            ax.speed=random.gauss(10,3)
            ax.update()

    def generate_bonus(self,screen):
        current_time=pygame.time.get_ticks() #time in ms
        if current_time - self.bonusclock>random.gauss(self.bonusperiod,self.bonusperiod*0.1):            
            self.bonusclock=current_time
            fruitlist=list(Fruitsdic().bonus.keys())
            i=random.randint(0,len(fruitlist)-1)
            fruit=Fruits(fruitlist[i])
            self.add_movbod(fruit)
            width=fruit.sprite.recttight[2]
            ph=min(self.players[0].height,self.players[1].height) #à réécrire en fonction de la hauteur de saut
            fruit.y=min(self.ground-random.gauss(2*ph,0.5*ph),self.ground)
            fruit.x=random.uniform(0,screen.width-width)

    def handle_collision(self,target):
        for movbod2 in self.movbods:
            if target is not movbod2 and movbod2.damage!=0:
                if pygame.sprite.collide_mask(target.sprite,movbod2.sprite):
                    damage=movbod2.damage
                    if damage>0 and target.hitable: #pour les collisions avec les bullets
                        target.invicible_clock=pygame.time.get_ticks()
                        target.hitable=False
                        target.life-=damage
                    elif damage<0: #Pour les bonus pas d'invincibilité
                        target.life-=damage

                    movbod2.kill()
                    self.movbods.remove(movbod2)
        

    def update(self,screen):
        self.generate_enemies(screen)
        self.generate_bonus(screen)
        for movbod in self.movbods:
            movbod.update()
            if movbod.x+movbod.width > screen.width:
                movbod.hit_right(self)
            if movbod.x < 0:
                movbod.hit_left(self)
        for player in self.players:
            self.handle_collision(player)