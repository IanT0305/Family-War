# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1800
HEIGHT = 1000
SIZE = (WIDTH, HEIGHT)
TITLE = "Family War"
screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)
BLUE = (66, 134, 244)


# Fonts
FONT_SM = pygame.font.Font("assets/fonts/Famig___.ttf", 24)
FONT_MD = pygame.font.Font("assets/fonts/Famig___.ttf", 32)
FONT_LG = pygame.font.Font("assets/fonts/Famig___.ttf", 64)
FONT_XL = pygame.font.Font("assets/fonts/Famig___.ttf", 96)
FONT_NUM = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 96)
FONT_NUM_SM = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 64)


# Images
ship_img = pygame.image.load('assets/images/stewy.png').convert_alpha()
laser_img = pygame.image.load('assets/images/laserRed.png').convert_alpha()
enemy1_img = pygame.image.load('assets/images/brian.png').convert_alpha()
enemy2_img = pygame.image.load('assets/images/Lois.png').convert_alpha()
bomb1_img = pygame.image.load('assets/images/poop.jpg').convert_alpha()
bomb2_img = pygame.image.load('assets/images/teddybear.png').convert_alpha()
back_img = pygame.image.load('assets/images/back.jpg').convert_alpha()
powerup1_img = pygame.image.load('assets/images/Giant_chicken_powerup.png').convert_alpha()
powerup2_img = pygame.image.load('assets/images/Peter.png').convert_alpha()
start_screen_img = pygame.image.load('assets/images/Family_Guy.jpg').convert_alpha()

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
LASER = pygame.mixer.Sound('assets/sounds/Laser_sound.ogg')


# Stages
START = 0
PLAYING = 1
END = 2


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()

        self.speed = 4
        self.health = 3
        self.double_shots = False

    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed
    
    def move_down(self):
        self.rect.y += self.speed

    def shoot(self):
        print("Pew!")
        LASER.play()

        if self.double_shots == False:
            laser = Laser(laser_img)
            laser.rect.centerx = self.rect.centerx
            laser.rect.centery = self.rect.top
            lasers.add(laser)
        elif self.double_shots == True:
            laser1 = Laser(laser_img)
            laser1.rect.centerx = self.rect.centerx + 30
            laser1.rect.centery = self.rect.top
            laser2 = Laser(laser_img)
            laser2.rect.centerx = self.rect.centerx - 30
            laser2.rect.centery = self.rect.top
            lasers.add(laser1, laser2)
            

    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

        ''' Check Powerups '''
        hit_list = pygame.sprite.spritecollide(self, powerups, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            print("Woot Beep")
            hit.apply(self)

        ''' check bombs '''
        hit_list = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            print("Oof!")
            self.health -= 1
            self.double_shots = False
        if self.health <= 0:
            stage = END
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect = image.get_rect()

        self.speed = 6

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image, bomb_image, mob_health):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bomb_image = bomb_image

        self.health = mob_health

    def drop_bomb(self):
        print("Bwampp!")
        
        bomb = Bomb(self.bomb_image)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
        
    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            self.health -= 1
            player.num_hits += 1
            EXPLOSION.play()
        if self.health <= 0:
            self.kill()
            fleet1.speed += 2
            fleet2.speed += 2
            player.score += 1

class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect = image.get_rect()

        self.speed = 6

    def update(self):
        self.rect.y += self.speed

        if self.rect.bottom > HEIGHT:
            self.kill()

class HealthPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7

    def apply(self, ship):
        ship.health = 3
        player.score += 5

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class ShootPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 7

    def apply(self, ship):
        ship.double_shots = True
        player.score += 5

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()


class Fleet1():
    def __init__(self, mobs1):
        self.mobs1 = mobs1
        self.speed = 5
        self.drop = 20
        self.moving_right = True
        self.bomb_rate = 60 #lower is faster

    def move(self):
        hits_edge = False

        for m in mobs1:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True

            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            # self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs1:
            m.rect.y += self.drop

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs1.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def update(self):
        self.move()
        self.choose_bomber()

class Fleet2():
    def __init__(self, mobs):
        self.mobs2 = mobs2
        self.speed = 5
        self.drop = 20
        self.moving_right = False
        self.bomb_rate = 60 #lower is faster

    def move(self):
        hits_edge = False

        for m in mobs2:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True

            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            #self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs2:
            m.rect.y += self.drop

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs2.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def update(self):
        self.move()
        self.choose_bomber()
            
# Game helper functions
def accuracy_booster():
    if player.num_shots > 0:
        accuracy = round(100*(player.num_hits/player.num_shots), 2)
    else:
        accuracy = 0
    
    if ((len(mobs1) > 0 and len(mobs1) < 4) and (len(mobs2) > 0 and len(mobs2) < 4)):
        ship.speed = 4
    elif ((len(mobs1) == 0)  or (len(mobs2) == 0)):
        if accuracy >= 60:
            ship.speed = 10
            player.bonus = "Yes"
        else:
            ship.speed = 4
            
def show_title_screen():
    title_text1 = FONT_XL.render("Family War!", 1, BLACK)
    title_text2 = FONT_XL.render("Press Space to Play", 1, BLACK)
    w = title_text1.get_width()
    r = title_text2.get_width()
    screen.blit(start_screen_img, (0, 0))
    screen.blit(title_text1, [WIDTH/2 - w/2, 300])
    screen.blit(title_text2, [WIDTH/2 - r/2, 400])

def show_end_screen():
    if (len(mobs1) == 0 and len(mobs2) == 0):
        end_text1 = FONT_XL.render("You Win!", 1, WHITE)
        end_text2 = FONT_XL.render("Press Space to Play Again", 1, WHITE)
        w = end_text1.get_width()
        r = end_text2.get_width()
        screen.blit(end_text1, [WIDTH/2 - w/2, 300])
        screen.blit(end_text2, [WIDTH/2 - r/2, 400])
    if len(player) == 0:
        end_text1 = FONT_XL.render("You Lose!", 1, WHITE)
        end_text2 = FONT_XL.render("Press Space to Play Again", 1, WHITE)
        w = end_text1.get_width()
        r = end_text2.get_width()
        screen.blit(end_text1, [WIDTH/2 - w/2, 300])
        screen.blit(end_text2, [WIDTH/2 - r/2, 400])

def show_stats():
    score_con_txt = FONT_NUM_SM.render("Points", 1, BLACK)
    score_txt = FONT_NUM.render(str(player.score), 1, BLACK)
    screen.blit(score_con_txt, [20, 10])
    screen.blit(score_txt, [20, 40])

    shield_con_txt = FONT_NUM_SM.render("Lives", 1, BLACK)
    shield_txt = FONT_NUM.render(str(ship.health), 1, BLACK)
    screen.blit(shield_con_txt, [1600, 10])
    screen.blit(shield_txt, [1700, 40])
    pygame.draw.rect(screen, BLACK, [1400, 20, 175, 30])
    if ship.health == 3:
        pygame.draw.rect(screen, BLUE, [1403, 22, 169, 26])
    elif ship.health == 2:
        pygame.draw.rect(screen, BLUE, [1403, 22, 112, 26])
    elif ship.health == 1:
        pygame.draw.rect(screen, RED, [1403, 22, 56, 26])
    elif ship.health == 0:
        pass
    
    bonus_txt = FONT_NUM_SM.render("Accuracy Bonus: " + player.bonus, 1, WHITE)
    w = bonus_txt.get_width()
    screen.blit(bonus_txt, [WIDTH/2 - w/2, 40])

def end_stats():
    if player.num_shots > 0:
        accuracy = round(100*(player.num_hits/player.num_shots), 2)
        accuracy_txt = FONT_NUM.render("Accuracy = " + str(accuracy) + "%", 1, BLACK)
        w = accuracy_txt.get_width()
        screen.blit(accuracy_txt, [WIDTH/2 - w/2, 500])
    else:
        accuracy = 0
        accuracy_txt = FONT_NUM.render("Accuracy = " + str(accuracy) + "%", 1, BLACK)
        w = accuracy_txt.get_width()
        screen.blit(accuracy_txt, [WIDTH/2 - w/2, 500])

def setup():
    global stage, done
    global player, ship, lasers, mobs1, mobs2, fleet1, fleet2, bombs, powerups
    
    ''' Make game objects '''
    ship = Ship(ship_img)
    ship.rect.centerx = WIDTH / 2
    ship.rect.bottom = HEIGHT - 30

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0
    player.num_shots = 0
    player.num_hits = 0
    player.bonus = "No"

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    mob1 = Mob(450, 100, enemy1_img, bomb1_img, 2)
    mob2 = Mob(900, 100, enemy1_img, bomb1_img, 1)
    mob3 = Mob(1350, 100, enemy1_img, bomb1_img, 2)
    mob4 = Mob(450, 250, enemy2_img, bomb2_img, 3)
    mob5 = Mob(900, 250, enemy2_img, bomb2_img, 2)
    mob6 = Mob(1350, 250, enemy2_img, bomb2_img, 3)

    mobs1 = pygame.sprite.Group()
    mobs1.add(mob1, mob2, mob3)

    mobs2 = pygame.sprite.Group()
    mobs2.add(mob4, mob5, mob6)

    powerup1 = HealthPowerUp(200, -2000, powerup1_img)
    powerup2 = ShootPowerUp(650, -5000, powerup2_img)
    powerups = pygame.sprite.Group()
    powerups.add(powerup1, powerup2)

    fleet1 = Fleet1(mobs1)
    fleet2 = Fleet2(mobs2)

    ''' set stage '''
    stage = START
    done = False

    
# Game loop
setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                    if event.key == pygame.K_SPACE:
                        ship.shoot()
                        player.num_shots += 1
                        
    pressed = pygame.key.get_pressed()
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        if pressed[pygame.K_UP]:
            ship.move_up()
        elif pressed[pygame.K_DOWN]:
            ship.move_down()

        player.update()
        lasers.update()
        bombs.update()
        fleet1.update()
        fleet2.update()
        mobs1.update()
        mobs2.update()
        powerups.update()
        accuracy_booster()

        if len(player) == 0 or (len(mobs1) == 0 and len(mobs2) == 0):
            stage = END

    if stage == END:
        if pressed[pygame.K_SPACE]:
            setup()
    
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    screen.blit(back_img, (0,0))
    lasers.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    mobs1.draw(screen)
    mobs2.draw(screen)
    powerups.draw(screen)
    show_stats()
    
    if stage == START:
        show_title_screen()

    if stage == END:
        show_end_screen()
        end_stats()
        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
