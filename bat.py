import pygame
import math
class Bat:
    def __init__(self, player, screen, x, y):
        self.player = player
        self.x = x
        self.y = y
        self.image = pygame.image.load("sprites/bat1.png")
        self.animdelay = 6
        self.timer = 0
        self.current_image = 1
        self.screen = screen
        self.bat = self.image.get_rect(center = (self.x, self.y))
        self.speed = 1.7


    def animate(self):
        if self.timer > self.animdelay:
            self.current_image+=1
            if self.current_image > 3:
                self.current_image = 1
            self.timer = 0
        else:
            self.timer += 1


        self.bat = self.image.get_rect(center = (self.x, self.y))
        self.image = pygame.image.load(f"sprites/bat{self.current_image}.png")
        self.screen.blit(self.image, self.bat)

    def track(self):
        dist_x = abs(self.x - self.player.player.centerx)
        dist_y = abs(self.y - self.player.player.centery)
        if dist_x < 300 and dist_y < 300:
            dx, dy = self.target(self.x, self.y, self.player.player.centerx, self.player.player.centery)
            self.x += dx * self.speed
            self.y += dy * self.speed
    def target(self, start_x, start_y, target_x, target_y):
        dist_x = target_x - start_x
        dist_y = target_y - start_y
        distance = math.sqrt((dist_x**2)+(dist_y**2))
        if distance != 0:
            dx = dist_x/distance
            dy = dist_y/distance
        return dx, dy

        