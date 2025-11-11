import pygame
from pygame import mixer
import os
import random
import csv
import button
 
mixer.init()
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
MAX_LEVELS = 3
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False
screen_shake = 0

# Game difficulty settings
PLAYER_SPEED = 5  # Default player speed
PLAYER_JUMP_VELOCITY = -13  # Jump strength (negative = upward)
ENEMY_DETECTION_RANGE = 150  # How far enemies can see
PLAYER_SHOOT_COOLDOWN = 15  # Frames between shots (lower = faster)

# Score system
score = 0
enemies_killed = 0

# define player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# Pause system
game_paused = False

# Cheat code system
cheat_input = ""  # Store typed characters
cheat_active = False  # God mode status
CHEAT_CODE = "thor"  # The secret code

#load music and sounds
# pygame.mixer.music.load('audio/music2.mp3')
# pygame.mixer.music.set_volume(0.3)
# pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.05)
shoot_fx = pygame.mixer.Sound('audio/shot.wav')
shoot_fx.set_volume(0.05)
grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
grenade_fx.set_volume(0.05)

#load images
#button images
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()

# define colors
BG = (144, 201, 120)  # background color
RED=(255,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
BLACK=(0,0,0)
PINK = (235, 65, 54)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Create pause/resume button images programmatically if they don't exist
def create_button_image(text, width, height, color):
    """Create a simple button image with text"""
    surface = pygame.Surface((width, height))
    surface.fill(color)
    pygame.draw.rect(surface, WHITE, (0, 0, width, height), 3)
    button_font = pygame.font.SysFont('Futura', 30)
    text_surf = button_font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(width//2, height//2))
    surface.blit(text_surf, text_rect)
    return surface

resume_img = create_button_image('RESUME', 200, 60, (50, 150, 50))
menu_exit_img = create_button_image('EXIT', 200, 60, (150, 50, 50))

#background
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
#bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()
#grenade
grenade_img = pygame.image.load('img/icons/grenade.png').convert_alpha()
#pick up boxes
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img
}


#define font
font=pygame.font.SysFont('Futura', 24)
small_font=pygame.font.SysFont('Futura', 18)
title_font=pygame.font.SysFont('Futura', 36)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_controls_hud():
    """Display game controls on screen"""
    hud_alpha = 180  # semi-transparent background
    hud_surface = pygame.Surface((220, 160))
    hud_surface.set_alpha(hud_alpha)
    hud_surface.fill((0, 0, 0))
    screen.blit(hud_surface, (SCREEN_WIDTH - 230, 10))
    
    # Draw control instructions
    y_offset = 20
    draw_text('CONTROLS:', small_font, WHITE, SCREEN_WIDTH - 220, y_offset)
    y_offset += 25
    draw_text('A/D: Move', small_font, WHITE, SCREEN_WIDTH - 220, y_offset)
    y_offset += 22
    draw_text('W: Jump', small_font, WHITE, SCREEN_WIDTH - 220, y_offset)
    y_offset += 22
    draw_text('SPACE: Shoot', small_font, WHITE, SCREEN_WIDTH - 220, y_offset)
    y_offset += 22
    draw_text('E: Grenade', small_font, WHITE, SCREEN_WIDTH - 220, y_offset)
    y_offset += 22
    draw_text('P: Pause', small_font, WHITE, SCREEN_WIDTH - 220, y_offset)
    y_offset += 22
    draw_text('ESC: Quit', small_font, WHITE, SCREEN_WIDTH - 220, y_offset)

def draw_pause_menu():
    """Draw the pause menu overlay"""
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Draw pause text
    draw_text('GAME PAUSED', title_font, YELLOW, SCREEN_WIDTH // 2 - 140, 100)
    
    # Draw cheat status if active
    if cheat_active:
        draw_text('⚡ GOD MODE ACTIVE ⚡', font, GREEN, SCREEN_WIDTH // 2 - 120, 180)
    
    # Draw instructions
    draw_text('Press P to Resume', font, WHITE, SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 - 50)
    draw_text('Press ESC to Exit', font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50)

def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5): 
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

#function to reset level
def reset_level():
    """Clear all sprite groups and return empty world data"""
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    
    #create empty tile list
    data=[]
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data

def reset_game_state():
    """Reset game state variables for new game"""
    global score, enemies_killed, level, bg_scroll, start_intro, cheat_active, cheat_input
    score = 0
    enemies_killed = 0
    level = 1
    bg_scroll = 0
    start_intro = True
    cheat_active = False
    cheat_input = ""

def check_cheat_code(new_char):
    """Check if cheat code has been entered"""
    global cheat_input, cheat_active
    cheat_input += new_char.lower()
    
    # Keep only the last characters needed
    if len(cheat_input) > len(CHEAT_CODE):
        cheat_input = cheat_input[-len(CHEAT_CODE):]
    
    # Check if cheat code matches
    if cheat_input == CHEAT_CODE:
        cheat_active = True
        cheat_input = ""  # Reset after activation
        return True
    return False

def draw_cheat_notification():
    """Show notification when cheat is active"""
    if cheat_active:
        # Draw flashing notification
        if pygame.time.get_ticks() % 1000 < 500:  # Flash every 500ms
            draw_text('⚡ GOD MODE ⚡', font, YELLOW, SCREEN_WIDTH // 2 - 80, 10)
            draw_text('Infinite Health & Ammo', small_font, GREEN, SCREEN_WIDTH // 2 - 90, 40)

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenade):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.ammo=ammo
        self.start_ammo=ammo
        self.shoot_cooldown = 0
        self.grenade=grenade
        self.health = 100
        self.max_health = self.health
        self.direction = 1  
        self.vel_y=0
        self.jump= False
        self.in_air= True
        self.flip = False  
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #create ai speciffic variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, ENEMY_DETECTION_RANGE, 20)
        self.idling = False
        self.idling_counter = 0
    

        #load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img=pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img=pygame.transform.scale(img, (int(img.get_width() * scale), (int(img.get_height() * scale))))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()


    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1


    def move(self, moving_left, moving_right):
        #reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        #assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = PLAYER_JUMP_VELOCITY
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check for collision
        for tile in world.obstacle_list:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                #if the ai has hit a wall then make it turn around
                if self.char_type == 'enemy':
                    self.direction *= -1
                    self.move_counter = 0
            #check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom


        #check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0

        #check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        #check if fallen off the map
        if self.rect.bottom > SCREEN_HEIGHT:
            self.health = 0

        #check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on the player position
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
                 or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete



    def shoot(self):
        # Check ammo (or if cheat is active for player)
        has_ammo = self.ammo > 0 or (cheat_active and self.char_type == 'player')
        
        if self.shoot_cooldown == 0 and has_ammo:
            # Use player-specific cooldown if player, else use default
            if self.char_type == 'player':
                self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
            else:
                self.shoot_cooldown = 20
            bullet=Bullet(self.rect.centerx+(0.75*self.rect.size[0]*self.direction), self.rect.centery, self.direction, self.char_type)
            bullet_group.add(bullet)
            #reduce ammo (unless cheat is active for player)
            if not (cheat_active and self.char_type == 'player'):
                self.ammo -= 1
            shoot_fx.play()



    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)#0: idle
                self.idling = True
                self.idling_counter = 50
            #check if the ai in near the player
            if self.vision.colliderect(player.rect):
                #stop running and face the player
                self.update_action(0)#0: idle
                
                # Make enemy face the player
                if player.rect.centerx > self.rect.centerx:
                    self.direction = 1
                    self.flip = False
                else:
                    self.direction = -1
                    self.flip = True
                
                #shoot
                self.shoot()
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else: 
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)#1: run
                    self.move_counter += 1
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + (ENEMY_DETECTION_RANGE // 2) * self.direction, self.rect.centery)
                    #check if the ai has hit a wall or water tile
                    if pygame.sprite.spritecollide(self, water_group, False):
                        self.direction *= -1
                        self.move_counter = 0
                    for tile in world.obstacle_list:
                        if tile[1].colliderect(self.rect.x + self.direction * self.speed, self.rect.y, self.width, self.height):
                            self.direction *= -1
                            self.move_counter = 0
                            
                    #update ai vision as the enemy moves
                    self.vision.center = (self.rect.centerx + (ENEMY_DETECTION_RANGE // 2) * self.direction, self.rect.centery)

                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        #scroll 
        self.rect.x += screen_scroll


    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks() 
            self.frame_index += 1
        #if the animation has run out, reset to the first frame
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0



    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        # God mode for player when cheat is active
        if cheat_active and self.char_type == 'player':
            if self.health < self.max_health:
                self.health = self.max_health
        
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
class World():
    def __init__(self, data):
        self.obstacle_list = []
        # Add these two lines to store the player and health_bar
        self.player = None
        self.health_bar = None
        self.process_data(data)

    def process_data(self, data):
        self.level_length = len(data[0])
        # We don't need these local variables anymore
        # player_created = False
        # player = None
        # health_bar = None
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >=0 and tile <= 8:
                        self.obstacle_list.append(tile_data)   
                    elif tile >= 9 and tile <=10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >=11 and tile <=14:
                        decoration= Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15 : #create player
                        # Use self.player and self.health_bar instead of local variables
                        self.player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, PLAYER_SPEED, 20, 5)
                        self.health_bar = HealthBar(10, 10, self.player.health, self.player.health )
                    elif tile == 16:#create enemies
                        enemy = Soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2, 20, 0)
                        enemy_group.add(enemy)
                    elif tile == 17:#create ammo box 
                        item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 18:#create grenade
                        item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:#create health box
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:#create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
        # If no player was created from level data, create a default one
        if not self.player:
            self.player = Soldier('player', 100, 100, 1.65, PLAYER_SPEED, 20, 5)
            self.health_bar = HealthBar(10, 10, self.player.health, self.player.health)
        # REMOVE the return statement
        # return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

class Decoration(pygame.sprite.Sprite):
    def __init__(self,img , x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self,img , x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self,img , x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type , x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.original_y = self.rect.y
        self.bob_counter = 0  # For bobbing animation

    def update(self):
        global score
        #scroll
        self.rect.x += screen_scroll
        
        # Add subtle bobbing animation
        self.bob_counter += 0.1
        self.rect.y = self.original_y + int(5 * abs(pygame.math.Vector2(0, 1).rotate(self.bob_counter * 10).y))
        
        #check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            #check what kind of box it was
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
                score += 10  # Bonus points for health pickup
            elif self.item_type == 'Ammo':
                player.ammo += 15
                score += 5  # Bonus points for ammo pickup
            elif self.item_type == 'Grenade':
                player.grenade += 3
                score += 15  # Bonus points for grenade pickup
            #delete the box
            self.kill()

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
    def draw(self, health):
        #update width of health bar
        self.health=health
        #calculate health ratio
        ratio = self.health / self.max_health
        # Determine color based on health percentage
        if ratio > 0.6:
            bar_color = GREEN
        elif ratio > 0.3:
            bar_color = ORANGE
        else:
            bar_color = RED
        pygame.draw.rect(screen, BLACK, (self.x-2, self.y-2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, bar_color, (self.x, self.y, 150 * ratio, 20))
        # Draw health text
        draw_text(f'{int(self.health)}/{int(self.max_health)}', small_font, WHITE, self.x + 165, self.y - 2)
        


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, owner):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 12  # Increased bullet speed
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.owner = owner
        self.lifetime = 0  # Track how long bullet has existed

    def update(self):
        #move bullet
        self.rect.x += (self.direction * self.speed) + screen_scroll
        self.lifetime += 1
        
        #check if bullet has gone off screen or existed too long
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.lifetime > 100:
            self.kill()
        #check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #check collision with characters
        if self.owner == 'enemy':
            if pygame.sprite.spritecollide(player, bullet_group, False):
                if player.alive:
                    player.health -= 5
                    self.kill()
        elif self.owner == 'player':
            for enemy in enemy_group:
                if pygame.sprite.spritecollide(enemy, bullet_group, False):
                    if enemy.alive:
                        was_alive = enemy.alive
                        enemy.health -= 25
                        # Award points if enemy was killed
                        if was_alive and enemy.health <= 0:
                            global score, enemies_killed
                            score += 100
                            enemies_killed += 1
                        self.kill()
        
class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer=100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        #check for collision with level
        for tile in world.obstacle_list:
            #check collision with walls
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            #check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                #check if below the ground i.e. thrown up
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        
        #update grenade position
        self.rect.x += dx + screen_scroll
        self.rect.y += dy



        #count down timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion=Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            #add screen shake
            global screen_shake
            screen_shake = 30
            #do damage to anyone that is nearby
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                 player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    was_alive = enemy.alive
                    enemy.health -= 50
                    # Award points for grenade kill
                    if was_alive and enemy.health <= 0:
                        global score, enemies_killed
                        score += 150  # More points for grenade kills
                        enemies_killed += 1



class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        for num in range(1,6):
            img= pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img=pygame.transform.scale(img, (int(img.get_width() * scale),int( img.get_height() * scale)))
            self.images.append(img)
        self.frame_index=0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter=0


    def update(self):
        #scroll
        self.rect.x += screen_scroll

        EXPLOSION_SPEED = 4
        #update explosion animation
        self.counter += 1


        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            #if the animation is complete then delete the explosion
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]

class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1: #whole screen fade
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, SCREEN_WIDTH //2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.color, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2: #vertical screen fade down
            pygame.draw.rect(screen, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True
        return fade_complete


#create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)

#create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)


#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()



world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

#load in level data and create world
try:
    with open(f'level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)
except FileNotFoundError:
    print(f"Error: level{level}_data.csv file not found.")
    print("Initializing with a blank level.")
    #create default floor
    for tile in range(0, COLS):
        world_data[ROWS-1][tile] = 0
    # Add an exit tile so the level can be completed.
    world_data[ROWS-1][COLS-1] = 20
    # Add an enemy
    world_data[ROWS-2][COLS-20] = 16


world = World(world_data)
player = world.player
health_bar = world.health_bar


run=True
while run:

    clock.tick(FPS)


    if start_game == False:
        #draw menu
        screen.fill(BG)
        draw_bg()
        
        # Draw title
        draw_text('WAR GRIDS', title_font, WHITE, SCREEN_WIDTH // 2 - 120, 50)
        draw_text('Platform Shooter Game', font, WHITE, SCREEN_WIDTH // 2 - 130, 100)
        
        # Draw controls info
        y_start = 180
        draw_text('=== CONTROLS ===', font, YELLOW, SCREEN_WIDTH // 2 - 100, y_start)
        draw_text('A / D : Move Left/Right', small_font, WHITE, SCREEN_WIDTH // 2 - 100, y_start + 35)
        draw_text('W : Jump', small_font, WHITE, SCREEN_WIDTH // 2 - 40, y_start + 60)
        draw_text('SPACE : Shoot', small_font, WHITE, SCREEN_WIDTH // 2 - 60, y_start + 85)
        draw_text('E : Throw Grenade', small_font, WHITE, SCREEN_WIDTH // 2 - 75, y_start + 110)
        draw_text('P : Pause/Resume', small_font, WHITE, SCREEN_WIDTH // 2 - 80, y_start + 135)
        draw_text('ESC : Exit Game', small_font, WHITE, SCREEN_WIDTH // 2 - 70, y_start + 160)
        
        # Draw hint about cheat
        draw_text('💡 Tip: Type secret words during gameplay...', small_font, ORANGE, SCREEN_WIDTH // 2 - 180, y_start + 200)
        
        #add buttons
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        #update background
        draw_bg()
        #draw world map
        world.draw()
        #show health bar
        health_bar.draw(player.health)

        #show ammo with number (or infinity if cheat active)
        draw_text('AMMO:', font, WHITE, 10, 35)
        if cheat_active:
            draw_text('∞', font, GREEN, 100, 35)
        else:
            draw_text(str(player.ammo), font, YELLOW if player.ammo > 5 else RED, 100, 35)
        
        #show grenades with number (or infinity if cheat active)
        draw_text('GRENADES:', font, WHITE, 10, 60)
        if cheat_active:
            draw_text('∞', font, GREEN, 150, 60)
        else:
            draw_text(str(player.grenade), font, YELLOW if player.grenade > 0 else RED, 150, 60)
        
        #show level number
        draw_text(f'LEVEL: {level}', font, WHITE, 10, 85)
        
        #show enemy count
        enemy_count = len(enemy_group)
        draw_text(f'ENEMIES: {enemy_count}', font, RED if enemy_count > 0 else GREEN, 10, 110)
        
        #show score
        draw_text(f'SCORE: {score}', font, YELLOW, 10, 135)
        draw_text(f'KILLS: {enemies_killed}', font, WHITE, 10, 160)
        
        #draw controls HUD
        draw_controls_hud()
        
        #draw cheat notification
        draw_cheat_notification()

        # Only update game if not paused
        if not game_paused:
            player.update()
        player.draw()
        
        if not game_paused:
            for enemy in enemy_group:
                enemy.ai()
                enemy.update()
                enemy.draw()

            #update and draw groups
            bullet_group.update()
            grenade_group.update()
            explosion_group.update()
            item_box_group.update()
            decoration_group.update()
            water_group.update()
            exit_group.update()
        else:
            # Still draw enemies and groups when paused
            for enemy in enemy_group:
                enemy.draw()
        
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        #show intro
        if start_intro == True and not game_paused:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter=0
            

        #update player actions (only if not paused)
        if player.alive and not game_paused:
            #shoot bullets
            if shoot:
                player.shoot()
            #throw grenades
            has_grenades = player.grenade > 0 or cheat_active
            if grenade and grenade_thrown == False and has_grenades:
                grenade=Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                                player.rect.top, player.direction)
                grenade_group.add(grenade)
                #reduce grenade (unless cheat is active)
                if not cheat_active:
                    player.grenade -= 1
                grenade_thrown = True

            if player.in_air:
                player.update_action(2) # 2: jump
            elif moving_left or moving_right:
                player.update_action(1) # 1: run
            else:
                player.update_action(0) # 0: idle
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            #check if player has completed the level
            if level_complete:
                # Display level complete message
                draw_text('LEVEL COMPLETE!', title_font, YELLOW, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
                pygame.display.update()
                pygame.time.delay(1500)  # Show message for 1.5 seconds
                
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <=MAX_LEVELS:
                    #load in level data and create world
                    try:
                        with open(f'level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter = ',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                    except FileNotFoundError:
                        print(f"Error: level{level}_data.csv file not found.")
                        print("Initializing with a blank level.")
                        #create default floor
                        for tile in range(0, COLS):
                            world_data[ROWS - 1][tile] = 0
                        # Add an exit tile so the level can be completed.
                        world_data[ROWS - 1][COLS - 1] = 20
                        # Add an enemy
                        world_data[ROWS - 2][COLS - 20] = 16
                    world = World(world_data)
                    player = world.player
                    health_bar = world.health_bar
                else:
                    # All levels completed - Victory screen
                    draw_text('CONGRATULATIONS!', title_font, YELLOW, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 100)
                    draw_text('You completed all levels!', font, WHITE, SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 40)
                    draw_text('Press ESC to exit', font, WHITE, SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 20)
                    pygame.display.update()
        else:
            screen_scroll = 0
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter=0
                    reset_game_state()
                    world_data = reset_level()
                    #load in level data and create world
                    try:
                        with open(f'level{level}_data.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile, delimiter = ',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                    except FileNotFoundError:
                        print(f"Error: level{level}_data.csv file not found.")
                        print("Initializing with a blank level.")
                        #create default floor
                        for tile in range(0, COLS):
                            world_data[ROWS-1][tile] = 0
                        # Add an exit tile so the level can be completed.
                        world_data[ROWS - 1][COLS - 1] = 20
                        # Add an enemy
                        world_data[ROWS-2][COLS-20] = 16
                    world = World(world_data)
                    player = world.player
                    health_bar = world.health_bar

        # Draw pause menu overlay if paused
        if game_paused:
            draw_pause_menu()

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            # Pause toggle (only when game is running)
            if event.key == pygame.K_p and start_game:
                game_paused = not game_paused
            
            # Handle input when NOT paused
            if not game_paused:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_SPACE:
                    shoot = True
                if event.key == pygame.K_e:
                    grenade = True
                if event.key == pygame.K_w and player.alive:
                    player.jump = True
                    jump_fx.play()
                
                # Cheat code detection - check for letter keys
                if event.unicode.isalpha() and start_game:
                    if check_cheat_code(event.unicode):
                        # Show activation message
                        print("🔥 CHEAT ACTIVATED: God Mode Enabled! 🔥")
            
            if event.key == pygame.K_ESCAPE:
                run = False


        #keyboard button released
        if event.type == pygame.KEYUP:
            if not game_paused:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_SPACE:
                    shoot = False
                if event.key == pygame.K_e:
                    grenade = False
                    grenade_thrown = False


    # screen shake
    if screen_shake > 0:
        screen_shake -= 1
        s = screen.copy()
        draw_bg()
        screen.blit(s, (random.randint(-8, 8), random.randint(-8, 8)))

    pygame.display.update()

pygame.quit()