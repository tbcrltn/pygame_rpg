import pygame

class Pistol:

    def __init__(self, player, screen):
        self.bullets = []
        self.bulletdx = []
        self.bulletdy = []
        self.player = player
        self.screen = screen
        self.speed = 10

    

    def draw(self):
        for bullet in self.bullets:
            pygame.draw.rect(self.screen, "blue", bullet)
            index = self.bullets.index(bullet)
            dx = self.bulletdx[index]
            dy = self.bulletdy[index]
            bullet.x += dx
            bullet.y += dy 
            if bullet.x > 700 or bullet.x < 0:
                self.destroy(bullet)
            elif bullet.y > 700 or bullet.y < 0:
                self.destroy(bullet)

    def shoot(self, dir):
        if dir == "up":
            dy = -self.speed
            dx = 0
        elif dir == "down":
            dy = self.speed
            dx = 0
        elif dir == "right":
            dy = 0
            dx = self.speed
        elif dir == "left":
            dy = 0
            dx = -self.speed
        self.bulletdx.append(dx)
        self.bulletdy.append(dy)
        self.bullets.append(pygame.Rect(325, 325, 5, 5))

    def destroy(self, bullet):
        try:
            index = self.bullets.index(bullet)
            self.bullets.pop(index)
            self.bulletdx.pop(index)
            self.bulletdy.pop(index)
        except: pass
    