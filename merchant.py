import pygame


class Merchant:
    def __init__(self, x, y, screen, maps):
        self.x = x
        self.y = y
        self.screen = screen
        self.map = maps
        self.image = pygame.image.load("sprites/merchant.png")
        self.merchant = pygame.transform.scale(self.image, (80, 80))
        self.load(0, 0)

    def draw(self, playerx, playery):
        if self.map == 1:
            

            self.load(playerx, playery)
            self.screen.blit(self.merchant, self.merchant_rect)
    def interactive_collider(self):
        return self.merchant_rect

    def collider(self):
        return self.collide_rect   
    def load(self, playerx, playery):
        if self.map == 1:
            dist_x = -playerx - 300
            dist_y = -playery - 300
            self.merchant_rect = self.merchant.get_rect(center = (self.x - dist_x, self.y - dist_y))
            self.collide_rect = self.merchant.get_rect(center = (self.x - dist_x+20, self.y - dist_y+40))
            self.collide_rect.width = 40
            self.collide_rect.height = 40
