import pygame





class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale(surface, (50, 50))
        self.rect = self.image.get_rect(topleft = pos)








