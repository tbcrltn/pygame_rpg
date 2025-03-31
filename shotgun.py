import pygame

class Shotgun():
    def __init__(self, player, screen):
        self.bullets = []
        self.bulletdx = []
        self.bulletdy = []
        self.player = player
        self.screen = screen
        self.speed = 13




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
            elif bullet.y > 700 or bullet.x < 0:
                self.destroy(bullet)



    def shoot(self, dir):
        if dir == "right":
            dx1 = self.speed 
            dy1 = 0
            dx2 = self.speed
            dy2 = 5
            dx3 = self.speed
            dy3 = -5
        elif dir == "left":
            dx1 = -self.speed 
            dy1 = 0
            dx2 = -self.speed
            dy2 = 5
            dx3 = -self.speed
            dy3 = -5
        elif dir == "up":
            dx1 = 0
            dy1 = -self.speed
            dx2 = 5
            dy2 = -self.speed
            dx3 = -5
            dy3 = -self.speed
        elif dir == "down":
            dx1 = 0
            dy1 = self.speed
            dx2 = 5
            dy2 = self.speed
            dx3 = -5
            dy3 = self.speed

        for x in range(3):
            self.bullets.append(pygame.Rect(325, 325, 5, 5))

        self.bulletdx.append(dx1)
        self.bulletdx.append(dx2)
        self.bulletdx.append(dx3)
        self.bulletdy.append(dy1)
        self.bulletdy.append(dy2)
        self.bulletdy.append(dy3)

    def destroy(self, bullet):
        try:
            index = self.bullets.index(bullet)
            self.bullets.pop(index)
            self.bulletdx.pop(index)
            self.bulletdy.pop(index)
        except: pass