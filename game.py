import pygame
from player import Player
from map import Tile
from pytmx.util_pygame import load_pygame
import time
import gif_pygame

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((700,700))
        self.player = Player(self.screen)
        self.player_dir = "down"
        self.player_speed = 5
        self.tile_group = pygame.sprite.Group()
        self.obj_group = pygame.sprite.Group()
        self.colliders = []
        self.interactive_objs = []
        self.interact = []
        self.new_map_pos = []
        self.map = 1
        self.tmx_data = load_pygame("maps/map1.tmx")
        self.dx = 0
        self.dy = 0
        self.start_x = 300
        self.start_y = 300
        self.playerx = -self.start_x
        self.playery = -self.start_y
        self.font_init()
        self.keys = []
        self.key_rect = []
        self.new_key(180, 870)
        self.load_map(self.start_x, self.start_y)
        print(self.interactive_objs)


    def run_game(self):
        pygame.init()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            print(f"Player @ {-self.playerx}, {-self.playery}")
            self.tile_group.draw(self.screen)
            self.player.animate(self.player_dir)
            self.obj_group.draw(self.screen)
            self.move()
            self.check_interactive_collision()
            self.draw_keys()
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
        elif keys[pygame.K_SPACE] or keys[pygame.K_e]:
            self.check_interaction()
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
        for collider in self.interactive_objs:
            collider.y += self.dy
            collider.x += self.dx
        for key in self.key_rect:
            key.x += self.dx
            key.y += self.dy


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
                for collider in self.interactive_objs:
                    collider.x -= self.dx
                    collider.y -= self.dy
                for key in self.key_rect:
                    key.x -= self.dx
                    key.y -= self.dy
                self.playerx -= self.dx
                self.playery-= self.dy
        self.playerx += self.dx
        self.playery += self.dy

    def check_interaction(self):
        for box in self.interactive_objs:
            if self.player.player.colliderect(box):
                print(f"colliding with box {self.interactive_objs.index(box)}")
                self.map = self.interact[self.interactive_objs.index(box)]
                map_pos = self.interactive_objs.index(box)
                print(self.map)
                self.new_map(self.map, map_pos)
    def check_interactive_collision(self):
        for box in self.interactive_objs:
            if self.player.player.colliderect(box):
                self.display_interaction()
            
                

                    
        
    def load_map(self, x, y):
        self.start_y = y
        self.start_x = x
        self.playerx = -x
        self.playery = -y
        for layer in self.tmx_data.layers:
            if layer.name in ("GROUND", "GROUND2"):
                for x, y, surf in layer.tiles():
                    pos = (x*50-self.start_x, y*50-self.start_y)
                    Tile(pos= pos, surface = surf, groups = self.tile_group)
            elif layer.name in ("OBJ"):
                for x, y, surf in layer.tiles():
                    pos = (x*50-self.start_x, y*50-self.start_y)
                    Tile(pos= pos, surface = surf, groups = self.obj_group)
            elif layer.name == "Collide":
                for obj in layer:
                    scale_factor = 50/32
                    object = pygame.Rect(obj.x*scale_factor - self.start_x, obj.y*scale_factor - self.start_y, obj.width*scale_factor, obj.height*scale_factor)
                    self.colliders.append(object)
            elif layer.name == "Interactive":
                counter = 0
                for obj in layer:
                    counter += 1
                    scale_factor = 50/32
                    object = pygame.Rect(obj.x*scale_factor - self.start_x, obj.y*scale_factor - self.start_y, obj.width*scale_factor, obj.height*scale_factor)
                    if counter == 1 and self.map == 1:
                        self.interactive_objs.append(object)
                        self.interact.append(2)
                        self.new_map_pos.append((1680, 1660))
                    elif counter == 1 and self.map == 2:
                        self.interactive_objs.append(object)
                        self.interact.append(1)
                        self.new_map_pos.append((3330, 260))
                        print(counter)
                    elif counter == 2 and self.map == 2:
                        self.interactive_objs.append(object)
                        self.interact.append(3)
                        self.new_map_pos.append((180,265))
                    elif counter == 1 and self.map == 3:
                        self.interactive_objs.append(object)
                        self.interact.append(2)
                        self.new_map_pos.append((1680,870))
            
    def new_map(self, map, map_pos):
        timer = 1
        self.player_dir = "down"
        map = str(map)
        self.tmx_data = load_pygame(f"maps/map{map}.tmx")
        player = self.new_map_pos[map_pos]
        print(player)
        self.obj_group.empty()
        self.tile_group.empty()
        self.interactive_objs = []
        self.interact = []
        self.new_map_pos = []
        self.colliders = []
        self.load_map(player[0], player[1])
        time.sleep(timer)
    def font_init(self):
        pygame.font.init()
        self.font = pygame.font.Font("fonts/pixel.ttf", 20)
        self.text = self.font.render("INTERACT [SPACE] OR [E]", False, "black")
    def display_interaction(self):
        
        self.screen.blit(self.text, (20, 680))
    def draw_keys(self):
        for key in self.keys:
            x = self.key_rect[self.keys.index(key)].x
            y = self.key_rect[self.keys.index(key)].y
            key.render(self.screen, (x, y))
    def new_key(self, x, y):
        key = gif_pygame.load("sprites/key.gif")
        self.keys.append(key)
        key_rect = key.get_rect(center = (x, y))
        self.key_rect.append(key_rect)
                    