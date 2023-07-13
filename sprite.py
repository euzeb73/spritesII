import pygame
import glob

class Sprite(pygame.sprite.Sprite):
    def __init__(self,action,dir,reducratio=3):
        super().__init__()
        self.action = action
        self.images = []
        self.index=-1
        self.animslowingfact=1
        self.dir=dir #Répertoire
        self.change_size(reducratio)
        
        
    def load_images(self):
        list_imgs = glob.glob("{}/{}*.png".format(self.dir,self.action)) #liste des fichiers image
        temp_imgs=[]
        self.images = []
        for img in list_imgs:
            #On charge et réduit l'image
            image=pygame.image.load(img)
            width=image.get_width()
            height=image.get_height()
            image=pygame.transform.smoothscale(image,(int(width/self.reducratio),int(height/self.reducratio)))
            #On stocke les images dans une liste
            if len(img) == len(list_imgs[0]): #de 0 à 9
                self.images.append(image)
            else: #de 10 à plus mais moins de 100...
                temp_imgs.append(image)
        self.images+=temp_imgs
        self.index = 0
        self.recttight=self.images[0].get_bounding_rect()
        self.rect=self.images[0].get_rect()
    
    def change_size(self,reducratio):
        self.reducratio=reducratio #par rapport au fichier d'origine facteur pour diminuer la taille du sprite
        self.load_images()
        self.update_img(False)

    def update_img(self,faceleft):
        imagenum=int(self.index/self.animslowingfact)
        if imagenum == len(self.images)-1:
            self.index = 0
        else:
            self.index += 1
        if faceleft:
            self.image = pygame.transform.flip(self.images[imagenum],True,False)
        else:
            self.image = self.images[imagenum]
        #pour gérer la différence entre le rectangle au plus petit et celui de l'image
        self.recttight=self.image.get_bounding_rect() #au plus près des pixels visibles

    def update_pos(self,x,y):
        ''' x,y est la position du coin inférieur gauche'''
        # xshift=recttight[0]-rectimg[0] #on fixe le pooint à gauche
        xshift=self.recttight[0]
        # yshift=recttight[1]+recttight[3]-rectimg[1]-rectimg[3] #on fixe le point en bas du sprite
        yshift=self.recttight[1]
        self.rect=self.image.get_rect()
        self.rect[0]=x-xshift
        self.rect[1]=y-yshift-self.recttight[3]
        self.recttight[0]=x # Pour garder un rectangle autour du sprite au bon endroit
        self.recttight[1]=y-self.recttight[3] 
        
