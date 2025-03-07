import pygame



def update_object(obj, dir):
    obj.update(dir)




class Dirt:
    def __init__(self, x, y, width, height, screen, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.speed = speed
        image = pygame.image.load("sprites/dirt.png")
        self.dirt = pygame.transform.scale(image, (50, 50))
        self.dirt_rect = self.dirt.get_rect(topleft = (self.x, self.y))
    def draw(self):
        num_tiles_x = int(self.width/50)
        num_tiles_y = int(self.height/50)
        for x in range(num_tiles_x):
            dist_x = x * 50
            for y in range(num_tiles_y):
                dist_y = y * 50
                self.screen.blit(self.dirt, (self.dirt_rect.x+dist_x, self.dirt_rect.y+ dist_y))
    def update(self, dir):
        if dir == "up":
            self.dirt_rect.y -= self.speed
        if dir == "down":
            self.dirt_rect.y += self.speed
        if dir == "right":
            self.dirt_rect.x += self.speed
        if dir == "left":
            self.dirt_rect.x -= self.speed





    
    
