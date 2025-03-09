import pygame
from player import Player
from obj import *
import pytmx
class Game:
    def __init__(self):
        self.map = pytmx.load_pygame("map.json")
        self.screen = pygame.display.set_mode((self.map.width * self.map.tilewidth, self.map.height * self.map.tileheight))
        self.player = Player(self.screen)
        self.player_dir = "down"
        self.player_speed = 5


    def run_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        

            self.draw_map()
            
            
            self.player.animate(self.player_dir)
            self.move()
            pygame.time.Clock().tick(60)
            pygame.display.flip()
        pygame.quit()

    
    
    
    def draw_map(self):
        for layer in self.map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.map.get_tile_image_by_gid(gid)
                    if tile:
                        self.screen.blit(tile, (x*self.map.tilewidth, y*self.map.tileheight))
    
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_dir = "up"
            self.player.moving = True
            self.move_camera("down")
        elif keys[pygame.K_DOWN]:
            self.player_dir = "down"
            self.player.moving = True
            self.move_camera("up")
        elif keys[pygame.K_LEFT]:
            self.player_dir = "left"
            self.player.moving = True
            self.move_camera("right")
        elif keys[pygame.K_RIGHT]:
            self.player_dir = "right"
            self.player.moving = True
            self.move_camera("left")
        else:
            self.player.moving = False

    def move_camera(self, dir):
        pass