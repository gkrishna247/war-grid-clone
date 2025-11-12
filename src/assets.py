import pygame
from pygame import mixer
import os
from settings import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
def get_asset_path(relative_path):
    return os.path.join(project_root, relative_path)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class DummySound:
    def play(self):
        pass

#load music and sounds
try:
    mixer.init()
    # pygame.mixer.music.load(get_asset_path('audio/music2.mp3'))
    # pygame.mixer.music.set_volume(0.3)
    # pygame.mixer.music.play(-1, 0.0, 5000)
    jump_fx = pygame.mixer.Sound(get_asset_path('audio/jump.wav'))
    jump_fx.set_volume(0.05)
    shoot_fx = pygame.mixer.Sound(get_asset_path('audio/shot.wav'))
    shoot_fx.set_volume(0.05)
    grenade_fx = pygame.mixer.Sound(get_asset_path('audio/grenade.wav'))
    grenade_fx.set_volume(0.05)
    item_pickup_fx = pygame.mixer.Sound(get_asset_path('audio/item_pickup.wav'))
    item_pickup_fx.set_volume(0.05)
    shotgun_fx = pygame.mixer.Sound(get_asset_path('audio/shotgun.wav'))
    shotgun_fx.set_volume(0.05)
    enemy_death_fx = pygame.mixer.Sound(get_asset_path('audio/enemy_death.wav'))
    enemy_death_fx.set_volume(0.05)
except pygame.error:
    print("Mixer could not be initialized. Sound will be disabled.")
    jump_fx = DummySound()
    shoot_fx = DummySound()
    grenade_fx = DummySound()
    item_pickup_fx = DummySound()
    shotgun_fx = DummySound()
    enemy_death_fx = DummySound()

#load images
#button images
start_img = pygame.image.load(get_asset_path('img/start_btn.png')).convert_alpha()
exit_img = pygame.image.load(get_asset_path('img/exit_btn.png')).convert_alpha()
restart_img = pygame.image.load(get_asset_path('img/restart_btn.png')).convert_alpha()

#background
pine1_img = pygame.image.load(get_asset_path('img/background/pine1.png')).convert_alpha()
pine2_img = pygame.image.load(get_asset_path('img/background/pine2.png')).convert_alpha()
mountain_img = pygame.image.load(get_asset_path('img/background/mountain.png')).convert_alpha()
sky_img = pygame.image.load(get_asset_path('img/background/sky_cloud.png')).convert_alpha()

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(get_asset_path(f'img/tile/{x}.png'))
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
#bullet
bullet_img = pygame.image.load(get_asset_path('img/icons/bullet.png')).convert_alpha()
#grenade
grenade_img = pygame.image.load(get_asset_path('img/icons/grenade.png')).convert_alpha()
#pick up boxes
health_box_img = pygame.image.load(get_asset_path('img/icons/health_box.png')).convert_alpha()
ammo_box_img = pygame.image.load(get_asset_path('img/icons/ammo_box.png')).convert_alpha()
grenade_box_img = pygame.image.load(get_asset_path('img/icons/grenade_box.png')).convert_alpha()
item_boxes = {
    'Health': health_box_img,
    'Ammo': ammo_box_img,
    'Grenade': grenade_box_img
}


#define font
font=pygame.font.SysFont('Futura', 24)
small_font=pygame.font.SysFont('Futura', 18)
title_font=pygame.font.SysFont('Futura', 36)

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
