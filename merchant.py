import pygame


class Merchant:
    def __init__(self, x, y, screen, maps, colliders):
        self.x = x
        self.y = y
        self.screen = screen
        self.map = maps
        self.colliders = colliders
        self.image = pygame.image.load("sprites/merchant.png")
        self.merchant = pygame.transform.scale(self.image, (100, 100))

    def draw(self, playerx, playery):
        if self.map == 1:
            dist_x = -playerx - 300
            dist_y = -playery - 300
            self.merchant_rect = self.merchant.get_rect(center = (self.x - dist_x, self.y - dist_y))
            collide_rect = self.merchant.get_rect(center = (self.x - dist_x+40, self.y - dist_y+50))
            collide_rect.height = 50
            collide_rect.width = 40

            self.colliders.append(collide_rect)
            self.screen.blit(self.merchant, self.merchant_rect)
    def collider(self):
        return self.merchant_rect
