import pygame
from player import Player
from obj import *
import obj
import pytmx
class Game:
    def __init__(self):
            
        self.screen = pygame.display.set_mode((700, 700))
        image = pygame.image.load("sprites/grass.png")
        self.bgimage = pygame.transform.scale(image, (2000, 2000))
        self.camera = self.bgimage.get_rect(topleft = (0, 0))
        self.player = Player(self.screen)
        self.player_dir = "down"
        self.player_speed = 5
        self.dirt = Dirt(0, 300, 1000, 100, self.screen, self.player_speed)
        self.dirt1 = Dirt(0, 300, 100, 1000, self.screen, self.player_speed)
        self.dirt2 = Dirt(0, -700, 100, 1000, self.screen, self.player_speed)
        self.objs = [self.dirt, self.dirt1, self.dirt2]


    def run_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.blit(self.bgimage, self.camera)
            
            self.move()

            self.draw_objs()
            
            self.player.animate(self.player_dir)
            pygame.time.Clock().tick(60)
            pygame.display.flip()

        pygame.quit()

    
    
    
    
    
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_dir = "up"
            self.player.moving = True
            self.move_camera("down")
            self.move_objs("down")
        elif keys[pygame.K_DOWN]:
            self.player_dir = "down"
            self.player.moving = True
            self.move_camera("up")
            self.move_objs("up")
        elif keys[pygame.K_LEFT]:
            self.player_dir = "left"
            self.player.moving = True
            self.move_camera("right")
            self.move_objs("right")
        elif keys[pygame.K_RIGHT]:
            self.player_dir = "right"
            self.player.moving = True
            self.move_camera("left")
            self.move_objs("left")
        else:
            self.player.moving = False

    def move_camera(self, dir):
        if dir == "right":
            self.camera.x += self.player_speed
        if dir == "left":
            self.camera.x -= self.player_speed
        if dir == "up":
            self.camera.y -= self.player_speed
        if dir == "down":
            self.camera.y += self.player_speed
        
        if self.camera.x > 0:
            self.camera.x = -1000
        if self.camera.y > 0:
            self.camera.y = -1000
        if self.camera.x < -1000:
            self.camera.x = 0
        if self.camera.y < -1000:
            self.camera.y = 0
    

    def move_objs(self, dir):
        for object in self.objs:
            obj.update_object(object, dir)

    def draw_objs(self):
        for object in self.objs:
            object.draw()
