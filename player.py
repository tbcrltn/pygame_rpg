import pygame
class Player:
    
    def __init__(self, screen):
        self.x, self.y = 0, 0
        image = pygame.image.load("sprites/player3.png")
        self.image = pygame.transform.scale(image, (45, 45))
        self.player = self.image.get_rect(topleft = (300, 300))
        self.screen = screen
        self.timer = 10
        self.animation = 3
        self.anim_speed = 8
        self.moving = False
        
    def animate(self, dir):
        if self.moving:
            self.timer += 1
            if self.timer > self.anim_speed:
                self.animation += 1
                self.timer = 0
                if self.animation > 4:
                    self.animation = 1
            if dir == "down":
                if self.animation == 1:
                    new_image = pygame.image.load("sprites/player2.png")
                elif self.animation == 2 or self.animation == 4:
                    new_image = pygame.image.load("sprites/player3.png")
                elif self.animation == 3:
                    new_image = pygame.image.load("sprites/player4.png")
            if dir == "up":
                if self.animation == 1:
                    new_image = pygame.image.load("sprites/player14.png")
                elif self.animation == 2 or self.animation == 4:
                    new_image = pygame.image.load("sprites/player15.png")
                elif self.animation == 3:
                    new_image = pygame.image.load("sprites/player16.png")
            if dir == "right":
                if self.animation == 1:
                    new_image = pygame.image.load("sprites/player5.png")
                elif self.animation == 2 or self.animation == 4:
                    new_image = pygame.image.load("sprites/player6.png")
                elif self.animation == 3:
                    new_image = pygame.image.load("sprites/player8.png")
            if dir == "left":
                if self.animation == 1:
                    new_image = pygame.image.load("sprites/player10.png")
                elif self.animation == 2 or self.animation == 4:
                    new_image = pygame.image.load("sprites/player9.png")
                elif self.animation == 3:
                    new_image = pygame.image.load("sprites/player12.png")
            
        else:
            if dir == "up":
                new_image = pygame.image.load("sprites/player15.png")
            elif dir == "down":
                new_image = pygame.image.load("sprites/player3.png")
            elif dir == "left":
                new_image = pygame.image.load("sprites/player9.png")
            elif dir == "right":
                new_image = pygame.image.load("sprites/player5.png")
        
        
        scaled_image = pygame.transform.scale(new_image, (45, 45))
        self.screen.blit(scaled_image, self.player)

