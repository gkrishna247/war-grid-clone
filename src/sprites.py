import pygame
import os
import random
from settings import *
from assets import shoot_fx, grenade_fx, item_boxes, bullet_img, grenade_img, shotgun_fx

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = pygame.Vector2(random.uniform(-2, 2), random.uniform(-4, -1))
        self.gravity = 0.1
        self.lifetime = 20

    def update(self, screen_scroll):
        self.vel.y += self.gravity
        self.rect.move_ip(self.vel)
        self.rect.x += screen_scroll
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

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
        self.shotgun = False
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


    def move(self, moving_left, moving_right, world, water_group, exit_group, bg_scroll):
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



    def shoot(self, bullet_group, cheat_active):
        # Check ammo (or if cheat is active for player)
        has_ammo = self.ammo > 0 or (cheat_active and self.char_type == 'player')

        if self.shoot_cooldown == 0 and has_ammo:
            # Use player-specific cooldown if player, else use default
            if self.char_type == 'player':
                self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
            else:
                self.shoot_cooldown = 20

            if self.shotgun:
                bullet1 = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, self.char_type, -5)
                bullet2 = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, self.char_type, 0)
                bullet3 = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction, self.char_type, 5)
                bullet_group.add(bullet1, bullet2, bullet3)
                shotgun_fx.play()
            else:
                bullet=Bullet(self.rect.centerx+(0.75*self.rect.size[0]*self.direction), self.rect.centery, self.direction, self.char_type)
                bullet_group.add(bullet)
                shoot_fx.play()

            #reduce ammo (unless cheat is active for player)
            if not (cheat_active and self.char_type == 'player'):
                self.ammo -= 1



    def ai(self, player, world, water_group, exit_group, bullet_group, screen_scroll, bg_scroll):
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
                self.shoot(bullet_group, False)
            else:
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right, world, water_group, exit_group, bg_scroll)
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
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type , x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.original_y = self.rect.y
        self.bob_counter = 0  # For bobbing animation

    def update(self, player, screen_scroll, score):
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
                score += 10
            elif self.item_type == 'Ammo':
                player.ammo += 15
                score += 5
            elif self.item_type == 'Grenade':
                player.grenade += 3
                score += 15
            elif self.item_type == 'Shotgun':
                player.shotgun = True
                score += 20
            #delete the box
            self.kill()
        return score

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, owner, spread=0):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 12
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.owner = owner
        self.lifetime = 0
        self.spread = spread

    def update(self, world, player, enemy_group, bullet_group, screen_scroll, score, enemies_killed, particle_group):
        self.rect.x += (self.direction * self.speed) + screen_scroll
        self.rect.y += self.spread
        self.lifetime += 1

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.lifetime > 100:
            self.kill()
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                for _ in range(3):
                    particle_group.add(Particle(self.rect.centerx, self.rect.centery))
                self.kill()

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
                        if was_alive and enemy.health <= 0:
                            score += 100
                            enemies_killed += 1
                        self.kill()
        return score, enemies_killed

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

    def update(self, world, player, enemy_group, explosion_group, screen_scroll, score, enemies_killed, screen_shake):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed = 0
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion=Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            screen_shake = 30
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                 player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    was_alive = enemy.alive
                    enemy.health -= 50
                    if was_alive and enemy.health <= 0:
                        score += 150
                        enemies_killed += 1
        return score, enemies_killed, screen_shake

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

    def update(self, screen_scroll):
        self.rect.x += screen_scroll
        EXPLOSION_SPEED = 4
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]
