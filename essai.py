from app import App
from world import World
from movbod import Abigaelle,Lucky
from sprite import Sprite

#Lucky
Luc=Lucky()
# Lucky=Player()
# Lucky.add_sprites('spirit')
# Lucky.change_size(1.8)
# Lucky.jumptop=20
# Lucky.speed=15

#Abigaelle
Abi=Abigaelle()
# Abigaelle=Player()
# Abigaelle.add_sprites('gdton')
# Abigaelle.change_size(1.8)
# Abigaelle.change_animspeed(10,['Jump'])
# Abigaelle.jumptop=8
# Abigaelle.speed=30

monde=World(Luc)
monde.add_player(Abi)
Abi.x=100

appli=App()
appli.add_world(monde)
appli.run()