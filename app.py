import pygame
from screen import Screen


class App():
    def __init__(self, FPS=60):
        self.FPS = 60
        pygame.init()
        self.clock = pygame.time.Clock()
        self.set_screen(1024, 768)

    def set_screen(self, width, height):
        self.screen = Screen(width, height)

    def add_world(self, world):
        self.world = world

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_f:
                        self.screen.switch_full()
                    if event.key == pygame.K_LEFT:
                        self.world.players[0].go_left()
                    if event.key == pygame.K_RIGHT:
                        self.world.players[0].go_right()
                    if event.key == pygame.K_SPACE:
                        self.world.players[0].jump()
                    # if event.key == pygame.K_KP4:
                    #     self.world.players[1].go_left()
                    # if event.key == pygame.K_KP6:
                    #     self.world.players[1].go_right()
                    # if event.key == pygame.K_KP8:
                    #     self.world.players[1].jump()
                    if event.key == pygame.K_q:
                        self.world.players[1].go_left()
                    if event.key == pygame.K_d:
                        self.world.players[1].go_right()
                    if event.key == pygame.K_z:
                        self.world.players[1].jump()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.world.players[0].stop()
                    if event.key == pygame.K_RIGHT:
                        self.world.players[0].stop()
                    # if event.key == pygame.K_KP4:
                    #     self.world.players[1].stop()
                    # if event.key == pygame.K_KP6:
                    #     self.world.players[1].stop()
                    if event.key == pygame.K_q:
                        self.world.players[1].stop()
                    if event.key == pygame.K_d:
                        self.world.players[1].stop()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.world.update(self.screen)
            self.clock.tick(self.FPS)
            self.screen.affiche(self.world)
        pygame.quit()
