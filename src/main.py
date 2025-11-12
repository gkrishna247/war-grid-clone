import pygame
from pygame import mixer
import os
import random
import csv
from settings import *
from assets import *
from sprites import Soldier, Bullet, Grenade, Explosion, ItemBox
from world import World, Decoration, Water, Exit
from ui import HealthBar, ScreenFade, draw_text, draw_controls_hud, draw_pause_menu, draw_bg, draw_cheat_notification, Button

mixer.init()
pygame.init()



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

#set frame rate
clock = pygame.time.Clock()


#define game variables
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False
screen_shake = 0

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
    particle_group.empty()

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

#create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)

#create buttons
start_button = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)


#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()



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
    # Add shotgun box
    world_data[ROWS-2][COLS-25] = 21


world = World()
player, health_bar = world.process_data(world_data, enemy_group, item_box_group, water_group, decoration_group, exit_group)


run=True
while run:

    clock.tick(FPS)


    if start_game == False:
        #draw menu
        screen.fill(BG)
        draw_bg(screen, bg_scroll)

        # Draw title
        draw_text('WAR GRIDS', title_font, WHITE, SCREEN_WIDTH // 2 - 120, 50, screen)
        draw_text('Platform Shooter Game', font, WHITE, SCREEN_WIDTH // 2 - 130, 100, screen)

        # Draw controls info
        y_start = 180
        draw_text('=== CONTROLS ===', font, YELLOW, SCREEN_WIDTH // 2 - 100, y_start, screen)
        draw_text('A / D : Move Left/Right', small_font, WHITE, SCREEN_WIDTH // 2 - 100, y_start + 35, screen)
        draw_text('W : Jump', small_font, WHITE, SCREEN_WIDTH // 2 - 40, y_start + 60, screen)
        draw_text('SPACE : Shoot', small_font, WHITE, SCREEN_WIDTH // 2 - 60, y_start + 85, screen)
        draw_text('E : Throw Grenade', small_font, WHITE, SCREEN_WIDTH // 2 - 75, y_start + 110, screen)
        draw_text('P : Pause/Resume', small_font, WHITE, SCREEN_WIDTH // 2 - 80, y_start + 135, screen)
        draw_text('ESC : Exit Game', small_font, WHITE, SCREEN_WIDTH // 2 - 70, y_start + 160, screen)

        # Draw hint about cheat
        draw_text('💡 Tip: Type secret words during gameplay...', small_font, ORANGE, SCREEN_WIDTH // 2 - 180, y_start + 200, screen)

        #add buttons
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        #update background
        draw_bg(screen, bg_scroll)
        #draw world map
        world.draw(screen, screen_scroll)
        #show health bar
        health_bar.draw(player.health, screen)

        #show ammo with number (or infinity if cheat active)
        draw_text('AMMO:', font, WHITE, 10, 35, screen)
        if cheat_active:
            draw_text('∞', font, GREEN, 100, 35, screen)
        else:
            draw_text(str(player.ammo), font, YELLOW if player.ammo > 5 else RED, 100, 35, screen)

        #show grenades with number (or infinity if cheat active)
        draw_text('GRENADES:', font, WHITE, 10, 60, screen)
        if cheat_active:
            draw_text('∞', font, GREEN, 150, 60, screen)
        else:
            draw_text(str(player.grenade), font, YELLOW if player.grenade > 0 else RED, 150, 60, screen)

        #show level number
        draw_text(f'LEVEL: {level}', font, WHITE, 10, 85, screen)

        #show enemy count
        enemy_count = len(enemy_group)
        draw_text(f'ENEMIES: {enemy_count}', font, RED if enemy_count > 0 else GREEN, 10, 110, screen)

        #show score
        draw_text(f'SCORE: {score}', font, YELLOW, 10, 135, screen)
        draw_text(f'KILLS: {enemies_killed}', font, WHITE, 10, 160, screen)

        #draw controls HUD
        draw_controls_hud(screen, small_font)

        #draw cheat notification
        draw_cheat_notification(screen, font, small_font, cheat_active)

        # Only update game if not paused
        if not game_paused:
            player.update()
            for enemy in enemy_group:
                enemy.ai(player, world, water_group, exit_group, bullet_group, screen_scroll, bg_scroll)
                enemy.update()
            bullet_group.update(world, player, enemy_group, bullet_group, screen_scroll, score, enemies_killed, particle_group)
            grenade_group.update(world, player, enemy_group, explosion_group, screen_scroll, score, enemies_killed, screen_shake)
            explosion_group.update(screen_scroll)
            item_box_group.update(player, screen_scroll, score)
            decoration_group.update(screen_scroll)
            water_group.update(screen_scroll)
            exit_group.update(screen_scroll)

        player.draw(screen)
        for enemy in enemy_group:
            enemy.draw(screen)

        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)
        particle_group.draw(screen)

        #show intro
        if start_intro == True and not game_paused:
            if intro_fade.fade(screen):
                start_intro = False
                intro_fade.fade_counter=0


        #update player actions (only if not paused)
        if player.alive and not game_paused:
            #shoot bullets
            if shoot:
                player.shoot(bullet_group, cheat_active)
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
            screen_scroll, level_complete = player.move(moving_left, moving_right, world, water_group, exit_group, bg_scroll)
            bg_scroll -= screen_scroll
            #check if player has completed the level
            if level_complete:
                # Display level complete message
                draw_text('LEVEL COMPLETE!', title_font, YELLOW, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, screen)
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
                        # Add shotgun box
                        world_data[ROWS - 2][COLS - 25] = 21
                    world = World()
                    player, health_bar = world.process_data(world_data, enemy_group, item_box_group, water_group, decoration_group, exit_group)
                else:
                    # All levels completed - Victory screen
                    draw_text('CONGRATULATIONS!', title_font, YELLOW, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 100, screen)
                    draw_text('You completed all levels!', font, WHITE, SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 40, screen)
                    draw_text('Press ESC to exit', font, WHITE, SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 20, screen)
                    pygame.display.update()
        else:
            screen_scroll = 0
            if death_fade.fade(screen):
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
                        # Add shotgun box
                        world_data[ROWS-2][COLS-25] = 21
                    world = World()
                    player, health_bar = world.process_data(world_data, enemy_group, item_box_group, water_group, decoration_group, exit_group)

        # Draw pause menu overlay if paused
        if game_paused:
            draw_pause_menu(screen, title_font, font, cheat_active)

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
        draw_bg(screen, bg_scroll)
        screen.blit(s, (random.randint(-8, 8), random.randint(-8, 8)))

    pygame.display.update()

pygame.quit()