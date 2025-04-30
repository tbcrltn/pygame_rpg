import pygame
from player import Player
from map import Tile
from pytmx.util_pygame import load_pygame
import time
import gif_pygame
from merchant import Merchant
from pistol import Pistol
from shotgun import Shotgun
from magic import Magic
from bat import Bat

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((700,700))
        self.player = Player(self.screen)
        self.player_dir = "down"
        self.player_speed = 5
        self.coins = 5
        self.health = 5
        self.init_tiles()
        self.dx = 0
        self.dy = 0
        self.start_x = 300
        self.start_y = 300
        self.playerx = -self.start_x
        self.playery = -self.start_y
        self.font_init()
        self.keys = []
        self.key_rect = []
        self.map_keys()
        self.load_chests()
        self.player_keys = 0
        self.init_merchant()
        self.init_enemies()
        self.load_map(self.start_x, self.start_y)
        self.create_keys()
        
        


    def run_game(self):
        pygame.init()
        self.running = True
        while self.running:
            self.check_events()
            print(f"Player @ {-self.playerx}, {-self.playery}")
            self.tile_group.draw(self.screen)
            self.pistolobj.draw()
            self.shotgunobj.draw()
            self.player.animate(self.player_dir)
            self.obj_group.draw(self.screen)
            self.check_interactive_collision()
            self.draw_keys()
            self.draw_chests()
            self.merchant.draw(self.playerx, self.playery)
            self.magicobj.draw()
            self.display_keys_held()
            self.display_money()
            self.display_health()
            self.check_key_collision()
            self.chest_collision()
            self.check_merchant_interaction()
            self.check_merchant_collision()
            self.check_bat_collision()
            self.shoot_pistol()
            self.shoot_shotgun()
            self.use_magic()
            self.bullet_collision()
            self.move()
            self.health = round(self.health)
            pygame.time.Clock().tick(60)
            pygame.display.flip()
        pygame.quit()
    def init_tiles(self):
        self.tile_group = pygame.sprite.Group()
        self.obj_group = pygame.sprite.Group()
        self.colliders = []
        self.interactive_objs = []
        self.interact = []
        self.new_map_pos = []
        self.map = 1
        self.tmx_data = load_pygame("maps/map1.tmx")

    def init_merchant(self):

        self.pistol = False
        self.shotgun = False
        self.magic = True
        self.merchant = Merchant(315, 2170, self.screen, self.map)
        self.pistolobj = Pistol(self.player, self.screen)
        self.shotgunobj = Shotgun(self.player, self.screen)
        self.magicobj = Magic(self.player, self.screen)
        self.shooting_timer = 100
        self.purchased_timer = 100
        self.using_timer = 100
        self.merchant_time_delay = 40
        self.shotgunowned = False
        self.pistolowned = False
    
    def init_enemies(self):
        self.bats = []
        self.new_bat(1605, 345)
        self.new_bat(2515, 795)


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def move(self):
        self.dx, self.dy = 0,0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_dir = "up"
            self.dy = self.player_speed
            self.player.moving = True
        elif keys[pygame.K_DOWN]:
            self.player_dir = "down"
            self.dy = -self.player_speed
            self.player.moving = True
        elif keys[pygame.K_LEFT]:
            self.player_dir = "left"
            self.dx = self.player_speed
            self.player.moving = True
        elif keys[pygame.K_RIGHT]:
            self.player_dir = "right"
            self.dx = -self.player_speed
            self.player.moving = True
        elif keys[pygame.K_e]:
            self.check_interaction()
        else:
            self.player.moving = False



        for tile in self.tile_group:
            tile.rect.x += self.dx
            tile.rect.y += self.dy
        for obj in self.obj_group:
            obj.rect.x += self.dx
            obj.rect.y += self.dy
        for collider in self.colliders:
            collider.y += self.dy
            collider.x += self.dx
        for collider in self.interactive_objs:
            collider.y += self.dy
            collider.x += self.dx
        for key in self.key_rect:
            key.x += self.dx
            key.y += self.dy
        for rect in self.interactive_chest_rect:
            rect.x += self.dx
            rect.y += self.dy
   
        self.playerx += self.dx
        self.playery += self.dy

        self.update_enemies(self.dx, self.dy)
        for collider in self.colliders:
            if self.player.player.colliderect(collider):
                self.collision()
    def collision(self):
        for tiles in self.tile_group:
            tiles.rect.x -= self.dx
            tiles.rect.y -= self.dy
        for obj in self.obj_group:
            obj.rect.x -= self.dx
            obj.rect.y -= self.dy
        for collider in self.colliders:
            collider.x -= self.dx
            collider.y -= self.dy
        for collider in self.interactive_objs:
            collider.x -= self.dx
            collider.y -= self.dy
        for key in self.key_rect:
            key.x -= self.dx
            key.y -= self.dy
        for rect in self.interactive_chest_rect:
            rect.x -= self.dx
            rect.y -= self.dy
        for bat in self.bats:
            bat.x -= self.dx
            bat.y -= self.dy
        self.playerx -= self.dx
        self.playery-= self.dy

    def check_interaction(self):
        for box in self.interactive_objs:
            if self.player.player.colliderect(box):
                print(f"colliding with box {self.interactive_objs.index(box)}")
                self.map = self.interact[self.interactive_objs.index(box)]
                map_pos = self.interactive_objs.index(box)
                print(self.map)
                self.new_map(self.map, map_pos = map_pos)
    def check_interactive_collision(self):
        for box in self.interactive_objs:
            if self.player.player.colliderect(box):
                self.display_interaction()
                     
        
    def load_map(self, x, y):
        self.start_y = y
        self.start_x = x
        self.playerx = -x
        self.playery = -y
        self.scale_factor = 50/32
        for layer in self.tmx_data.layers:
            if layer.name in ("GROUND", "GROUND2"):
                for x, y, surf in layer.tiles():
                    pos = (x*50-self.start_x, y*50-self.start_y)
                    Tile(pos= pos, surface = surf, groups = self.tile_group)
            elif layer.name in ("OBJ"):
                for x, y, surf in layer.tiles():
                    pos = (x*50-self.start_x, y*50-self.start_y)
                    Tile(pos= pos, surface = surf, groups = self.obj_group)
            elif layer.name == "Collide":
                for obj in layer:
                    
                    object = pygame.Rect(obj.x*self.scale_factor - self.start_x, obj.y*self.scale_factor - self.start_y, obj.width*self.scale_factor, obj.height*self.scale_factor)
                    self.colliders.append(object)

                    
            elif layer.name == "Interactive":
                interactive = 0
                for obj in layer:
                    interactive += 1
                    
                    object = pygame.Rect(obj.x*self.scale_factor - self.start_x, obj.y*self.scale_factor - self.start_y, obj.width*self.scale_factor, obj.height*self.scale_factor)
                    self.manage_interactives(interactive, object)

    def load_enemies(self):
        if self.map == 1:
            self.new_bat(1605, 345)
            self.new_bat(2515, 795)
        elif self.map == 2:
            self.new_bat(1305, 1075)
        elif self.map == 4:
            self.new_bat(2386, 431)
            self.new_bat(1596, 396)
            self.new_bat(731, 336)
    
    def manage_interactives(self, interactive, object):
        if interactive == 1 and self.map == 1:
            self.interactive_objs.append(object)
            self.interact.append(2)
            self.new_map_pos.append((1680, 1660))
        elif interactive == 1 and self.map == 2:
            self.interactive_objs.append(object)
            self.interact.append(1)
            self.new_map_pos.append((3330, 260))
        elif interactive == 2 and self.map == 2:
            self.interactive_objs.append(object)
            self.interact.append(3)
            self.new_map_pos.append((180,265))
        elif interactive == 1 and self.map == 3:
            self.interactive_objs.append(object)
            self.interact.append(2)
            self.new_map_pos.append((1680,870))
        elif interactive == 2 and self.map == 3:
            self.interactive_objs.append(object)
            self.interact.append(1)
            self.new_map_pos.append((3180, 1300))
        elif interactive == 2 and self.map == 1:
            self.interactive_objs.append(object)
            self.interact.append(3)
            self.new_map_pos.append((1175, 280))
        elif interactive == 3 and self.map == 1:
            self.interactive_objs.append(object)
            self.interact.append(4)
            self.new_map_pos.append((226, 321))
        elif interactive == 1 and self.map == 4:
            self.interactive_objs.append(object)
            self.interact.append(1)
            self.new_map_pos.append((2230,2125))
        elif interactive == 2 and self.map == 4:
            self.interactive_objs.append(object)
            self.interact.append(2)
            self.new_map_pos.append((430, 525))
        elif interactive == 3 and self.map == 2:
            self.interactive_objs.append(object)
            self.interact.append(4)
            self.new_map_pos.append((3176, 316))
            
    def new_map(self, map, map_pos = None):
        timer = 1
        self.player_dir = "down"
        map = str(map)
        self.tmx_data = load_pygame(f"maps/map{map}.tmx")
        if map_pos == None:
            player = (300, 300)
        else:
            player = self.new_map_pos[map_pos]
        print(player)
        self.obj_group.empty()
        self.tile_group.empty()
        self.interactive_objs = []
        self.interact = []
        self.new_map_pos = []
        self.colliders = []
        self.load_map(player[0], player[1])
        self.keys = []
        self.key_rect = []
        self.chests = []
        self.chest_rect = []
        self.interactive_chest_rect = []
        for bat in self.bats:
            del bat
        self.bats = []
        self.create_keys()
        self.create_chests()
        self.load_enemies()
        time.sleep(timer)
    def font_init(self):
        pygame.font.init()
        self.font = pygame.font.Font("fonts/pixel.ttf", 20)
        self.text = self.font.render("INTERACT [E]", False, (255, 255, 255), bgcolor=(0, 0, 0))
    def display_interaction(self):
        
        self.screen.blit(self.text, (20, 680))
    def draw_keys(self):
        for key in self.keys:
            x = self.key_rect[self.keys.index(key)].x
            y = self.key_rect[self.keys.index(key)].y
            key.render(self.screen, (x, y))
    def new_key(self, x, y):
        key = gif_pygame.load("sprites/key.gif")
        self.keys.append(key)
        dist_x = -self.playerx - 300
        dist_y = -self.playery - 300
        key_rect = key.get_rect(topleft = (x-dist_x, y-dist_y))
        self.key_rect.append(key_rect)

    def check_key_collision(self):
        for key in self.key_rect:
            if self.player.player.colliderect(key):
                self.player_keys += 1
                self.destroy_key(key)

    def destroy_key(self, key):
        index = self.key_rect.index(key)
        self.keys.pop(index)
        self.key_rect.pop(index)
        if self.map == 1:
            self.map1keys.pop(index)
        elif self.map == 2:
            self.map2keys.pop(index)
        elif self.map == 3:
            self.map3keys.pop(index)

        

    def display_keys_held(self):
        text = self.font.render(f"KEYS: {self.player_keys}", False, (255, 255, 255), bgcolor=(0, 0, 0))
        self.screen.blit(text, (10, 10))

    def create_keys(self):
        if self.map == 1:
            for key in self.map1keys:
                self.new_key(key[0], key[1])   
        elif self.map == 2:
            for key in self.map2keys:
                self.new_key(key[0], key[1])
        elif self.map == 3:
            for key in self.map3keys:
                self.new_key(key[0], key[1])

    def map_keys(self):
        self.map1keys = [(160, 855), (3450, 865)]
        self.map2keys = [(1000, 850), (210, 1195)]
        self.map3keys = [(740, 690)]


    def load_chests(self):
        self.chests = []
        self.interactive_chest_rect = []
        self.chest_rect = []
        self.opened_chests = []
        self.map_chests()
        self.create_chests()

    def map_chests(self):
        self.map1chests = [[1035, 145, 0], [775, 1465, 0], [1010, 640, 0]]
        self.map3chests = [[185, 1100, 0]]
        self.map2chests = [[795, 755, 0]]

    def create_chests(self):
        if self.map == 1:
            for chest in self.map1chests:
                self.new_chest(chest[0], chest[1], chest[2])
        if self.map == 3:
            for chest in self.map3chests:
                self.new_chest(chest[0], chest[1], chest[2])
        if self.map == 2:
            for chest in self.map2chests:
                self.new_chest(chest[0], chest[1], chest[2])

    def new_chest(self, x, y, status):
        if status == 0:
            chest_image = pygame.image.load("sprites/chest.png")
        if status == 1:
            chest_image = pygame.image.load("sprites/openchest.png")
        self.chests.append(chest_image)
        dist_x = -self.playerx - 300
        dist_y = -self.playery - 300
        chest_rect = chest_image.get_rect(topleft = (x-dist_x, y-dist_y))
        interactive_rect = chest_image.get_rect(topleft = (x-dist_x, y-dist_y))
        interactive_rect.height = 100
        self.chest_rect.append(chest_rect)
        self.interactive_chest_rect.append(interactive_rect)
        self.colliders.append(chest_rect)

    def draw_chests(self):
        for chest in self.chests:
            index = self.chests.index(chest)
            x = self.chest_rect[index].x
            y = self.chest_rect[index].y
            self.screen.blit(chest, (x, y))

    def chest_collision(self):
        for chest in self.interactive_chest_rect:
            index = self.interactive_chest_rect.index(chest)
            if self.map == 1:
                if self.map1chests[index][2] == 0:
                    self.check_chest_collision(chest)
            elif self.map == 3:
                if self.map3chests[index][2] == 0:
                    self.check_chest_collision(chest)
            elif self.map == 2:
                if self.map2chests[index][2] == 0:
                    self.check_chest_collision(chest)
    
    def check_chest_collision(self, chest):
        if self.player.player.colliderect(chest):
            if self.player_keys >= 1:
                self.display_interaction()
                key = pygame.key.get_pressed()
                if key[pygame.K_e]:
                    index = self.interactive_chest_rect.index(chest)
                    self.open_chest(index)

    def open_chest(self, index):
        self.player_keys -= 1
        if self.map == 1:
            self.map1chests[index][2] = 1
        if self.map == 3:
            self.map3chests[index][2] = 1
        if self.map == 2:
            self.map2chests[index][2] = 1
        self.chests[index] = pygame.image.load("sprites/openchest.png")
        self.coins += 10
                
    def display_money(self):
        text = self.font.render(f"COINS: {self.coins}", False, (255, 255, 255), bgcolor=(0, 0, 0))
        self.screen.blit(text, (10, 30))         
        
    def check_merchant_interaction(self):
        if self.player.player.colliderect(self.merchant.interactive_collider()):
            self.display_interaction()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                self.display_merchant_screen()

    def check_merchant_collision(self):
        if self.map == 1:
            collider = self.merchant.collider()
            if self.player.player.colliderect(collider):
                self.collision()

    def display_merchant_screen(self):
        screen_up = True
        menu_screen = pygame.Surface((700, 700), pygame.SRCALPHA)
        num = 1
        self.funds_timer = 100
        while screen_up:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        screen_up = False
                    if event.key == pygame.K_UP:
                        if not num == 1:
                            num -= 1
                    if event.key == pygame.K_DOWN:
                        if not num == 3:
                            num += 1

            menu_screen.fill((0, 0, 0, 190))
            quit_text = self.font.render("CLOSE [ESC]", False, (255, 255, 255))
            menu_screen.blit(quit_text, (560, 10))
            select_text = self.font.render("SELECT [ENTER]", False, (255, 255, 255))
            menu_screen.blit(select_text, (20, 10))
            self.buy_options(num, menu_screen)
            
            
            self.check_events()
            self.draw_screen()
            self.screen.blit(menu_screen, (0, 0))

            

            pygame.time.Clock().tick(20)
            pygame.display.flip()

    def draw_screen(self):
        self.tile_group.draw(self.screen)
        self.player.animate(self.player_dir)
        self.obj_group.draw(self.screen)
        self.draw_keys()
        self.draw_chests()
        self.merchant.draw(self.playerx, self.playery)
    
    def buy_options(self, num, menu_screen):
        keys = pygame.key.get_pressed()
        if self.funds_timer < self.merchant_time_delay:
            text = self.font.render("INSUFFICIENT FUNDS", False, (255, 255, 255))
            menu_screen.blit(text, (250, 680))
            self.funds_timer += 1
        
        if self.purchased_timer < self.merchant_time_delay:
            text = self.font.render("PURCHASED SUCCESSFULLY", False, (255, 255, 255))
            menu_screen.blit(text, (200, 680))
            self.purchased_timer += 1
        
        if self.using_timer < self.merchant_time_delay:
            text = self.font.render("ALREADY  IN  USE", False, (255, 255, 255))
            menu_screen.blit(text, (250, 680))
            self.using_timer += 1


        font = pygame.font.Font("fonts/pixel.ttf", 30)
        if num == 1:
            pistol = font.render("PISTOL ------------------------ 25 COINS", False, (0, 0, 0), bgcolor=(255, 255, 255))
            shotgun = font.render("SHOTGUN --------------------- 50 COINS", False, (255, 255, 255))
            magic = font.render("MAGIC --------------------- 100 COINS", False, (255, 255, 255))
            if keys[pygame.K_RETURN]:
                if self.pistol:
                    self.using_timer = 0
                else:
                    if self.coins >= 25:

                        self.coins -= 25
                        self.pistol = True
                        self.shotgun = False
                        self.magic = False
                        time.sleep(0.5)
                        self.purchased_timer = 0
                    else:
                        self.funds_timer = 0
        elif num == 2:
            pistol = font.render("PISTOL ------------------------ 25 COINS", False, (255, 255, 255))
            shotgun = font.render("SHOTGUN --------------------- 50 COINS", False, (0, 0, 0), bgcolor=(255, 255, 255))
            magic = font.render("MAGIC --------------------- 100 COINS", False, (255, 255, 255))
            if keys[pygame.K_RETURN]:
                if self.shotgun:
                    self.using_timer = 0
                else:
                    if self.coins >= 50:
                    
                        self.coins -= 50
                        self.pistol = False
                        self.shotgun = True
                        self.magic = False
                        time.sleep(0.5)
                        self.purchased_timer = 0
                    else:
                        self.funds_timer = 0
        elif num == 3:
            pistol = font.render("PISTOL ------------------------ 25 COINS", False, (255, 255, 255))
            shotgun = font.render("SHOTGUN --------------------- 50 COINS", False, (255, 255, 255))
            magic = font.render("MAGIC --------------------- 100 COINS", False, (0, 0, 0), bgcolor = (255, 255, 255))
            if keys[pygame.K_RETURN]:
                if self.magic:
                    self.using_timer = 0
                else:
                    if self.coins >= 100:
                        self.coins -= 100
                        self.magic = True
                        self.shotgun = False
                        self.pistol = False
                        time.sleep(0.5)
                        self.purchased_timer = 0
                    else:
                        self.funds_timer = 0



        menu_screen.blit(pistol, (20, 100))
        menu_screen.blit(shotgun, (20, 200))
        menu_screen.blit(magic, (20, 300))

    def shoot_pistol(self):
        if self.pistol == True:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if self.shooting_timer > 5:
                    self.pistolobj.shoot(self.player_dir)
                    self.shooting_timer = 0
            else:
                self.shooting_timer += 1

    def shoot_shotgun(self):
        if self.shotgun == True:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if self.shooting_timer > 5:
                    self.shotgunobj.shoot(self.player_dir)
                    self.shooting_timer = 0
            else:
                self.shooting_timer += 1

    def use_magic(self):
        if self.magic:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if self.shooting_timer > 5:
                    self.magicobj.shoot(self.player_dir)
                    self.shooting_timer = 0
            else:
                self.shooting_timer += 1

    def bullet_collision(self):
        
        if self.pistol:
            for bullet in self.pistolobj.bullets:
                for collider in self.colliders:
                    if bullet.colliderect(collider):
                        self.pistolobj.destroy(bullet)
        elif self.shotgun:
            for bullet in self.shotgunobj.bullets:
                for collider in self.colliders:
                    if bullet.colliderect(collider):
                        self.shotgunobj.destroy(bullet)
        #magic bullets go through walls so no collisions

    def new_bat(self, x, y):
        dist_x = -self.playerx - 300
        dist_y = -self.playery - 300
        self.bats.append(Bat(self.player, self.screen, x - dist_x, y - dist_y))

    def update_enemies(self, dx, dy):
        for bat in self.bats:
            bat.animate()
            bat.track()
            bat.x += dx
            bat.y += dy


    def check_bat_collision(self):
        for bat in self.bats:
            if self.player.player.colliderect(bat.bat):
                self.health -= 1

            if self.pistol:
                for bullet in self.pistolobj.bullets:
                    if bullet.colliderect(bat.bat):
                        bat.health -= 1
                        index = self.pistolobj.bullets.index(bullet)
                        self.pistolobj.bullets.pop(index)
                        self.pistolobj.bulletdx.pop(index)
                        self.pistolobj.bulletdy.pop(index)
            elif self.shotgun:
                for bullet in self.shotgunobj.bullets:
                    if bullet.colliderect(bat.bat):
                        bat.health -= 1
                        index = self.shotgunobj.bullets.index(bullet)
                        self.shotgunobj.bullets.pop(index)
                        self.shotgunobj.bulletdx.pop(index)
                        self.shotgunobj.bulletdy.pop(index)
            elif self.magic:
                for bullet in self.magicobj.bullets:
                    if bullet.colliderect(bat.bat):
                        bat.health -= 1
                        index = self.magicobj.bullets.index(bullet)
                        self.magicobj.bullets.pop(index)
                        self.magicobj.bulletdx.pop(index)
                        self.magicobj.bulletdy.pop(index)
            
            if bat.health <= 0:
                index = self.bats.index(bat)
                self.bats.pop(index)
            self.check_bat_player_collision(bat)
    def check_bat_player_collision(self, bat):
        if self.player.player.colliderect(bat.bat):
            self.health -= 0.01
            self.map = 1
            self.new_map(self.map)


    def display_health(self):
        text = self.font.render(f"LIVES: {self.health}", False, (255, 255, 255), bgcolor = (0, 0, 0))
        self.screen.blit(text, (10, 50))

