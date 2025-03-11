import pygame
from player import Player
from map import *
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((700,700))
        self.player = Player(self.screen)
        self.player_dir = "down"
        self.player_speed = 5
        self.tile_group = pygame.sprite.Group()
        self.obj_group = pygame.sprite.Group()
        self.colliders = []
        self.tmx_data = load_pygame("maps/map1.tmx")
        self.dx = 0
        self.dy = 0
        self.start_x = 300
        self.start_y = 300
        

        self.load_map()
        print(self.colliders)


    def run_game(self):
        pygame.init()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.tile_group.draw(self.screen)
            self.player.animate(self.player_dir)
            self.obj_group.draw(self.screen)
            self.move()
            pygame.time.Clock().tick(60)
            pygame.display.flip()
        pygame.quit()

    
    
    
    def move(self):
        self.dx, self.dy = 0,0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_dir = "up"
            self.dy = self.player_speed
            self.player.moving = True
        elif keys[pygame.K_DOWN]:
            self.player_dir = "down"
            self.dy = -self.player_speed
            self.player.moving = True
        elif keys[pygame.K_LEFT]:
            self.player_dir = "left"
            self.dx = self.player_speed
            self.player.moving = True
        elif keys[pygame.K_RIGHT]:
            self.player_dir = "right"
            self.dx = -self.player_speed
            self.player.moving = True
        else:
            self.player.moving = False



        for tile in self.tile_group:
            tile.rect.x += self.dx
            tile.rect.y += self.dy
        for obj in self.obj_group:
            obj.rect.x += self.dx
            obj.rect.y += self.dy
        for collider in self.colliders:
            collider.y += self.dy
            collider.x += self.dx


        for collider in self.colliders:
            if self.player.player.colliderect(collider):
                for tiles in self.tile_group:
                    tiles.rect.x -= self.dx
                    tiles.rect.y -= self.dy
                for obj in self.obj_group:
                    obj.rect.x -= self.dx
                    obj.rect.y -= self.dy
                for collider in self.colliders:
                    collider.x -= self.dx
                    collider.y -= self.dy
                    
        
    def load_map(self):
        for layer in self.tmx_data.layers:
            if layer.name in ("GROUND", "GROUND2"):
                for x, y, surf in layer.tiles():
                    pos = (x*50-self.start_x, y*50-self.start_y)
                    Tile(pos= pos, surface = surf, groups = self.tile_group)
            if layer.name in ("OBJ"):
                for x, y, surf in layer.tiles():
                    pos = (x*50-self.start_x, y*50-self.start_y)
                    Tile(pos= pos, surface = surf, groups = self.obj_group)

        for obj in self.tmx_data.objects:
            scale_factor = 50/32
            object = pygame.Rect(obj.x*scale_factor - self.start_x, obj.y*scale_factor - self.start_y, obj.width*scale_factor, obj.height*scale_factor)
            self.colliders.append(object)




    
                    