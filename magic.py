import pygame

class Magic():
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
        
        dx1 = self.speed 
        dy1 = 0
        dx2 = self.speed
        dy2 = 5
        dx3 = self.speed
        dy3 = -5
        
        dx4 = -self.speed 
        dy4 = 0
        dx5 = -self.speed
        dy5 = -5
        dx6 = -self.speed
        dy6 = 5
        

        for x in range(6):
            self.bullets.append(pygame.Rect(325, 325, 5, 5))

        self.bulletdx.append(dx1)
        self.bulletdx.append(dx2)
        self.bulletdx.append(dx3)
        self.bulletdy.append(dy1)
        self.bulletdy.append(dy2)
        self.bulletdy.append(dy3)
        self.bulletdx.append(dx4)
        self.bulletdx.append(dx5)
        self.bulletdx.append(dx6)
        self.bulletdy.append(dy4)
        self.bulletdy.append(dy5)
        self.bulletdy.append(dy6)


    def destroy(self, bullet):
        try:
            index = self.bullets.index(bullet)
            self.bullets.pop(index)
            self.bulletdx.pop(index)
            self.bulletdy.pop(index)
        except: pass