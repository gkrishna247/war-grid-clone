import pygame
from settings import *
from assets import small_font

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health, screen):
        self.health=health
        ratio = self.health / self.max_health
        if ratio > 0.6:
            bar_color = GREEN
        elif ratio > 0.3:
            bar_color = ORANGE
        else:
            bar_color = RED
        pygame.draw.rect(screen, BLACK, (self.x-2, self.y-2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, bar_color, (self.x, self.y, 150 * ratio, 20))
        draw_text(f'{int(self.health)}/{int(self.max_health)}', small_font, WHITE, self.x + 165, self.y - 2, screen)

def draw_text(text, font, text_col, x, y, screen):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self, screen):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, SCREEN_WIDTH //2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.color, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2:
            pygame.draw.rect(screen, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True
        return fade_complete

def draw_text(text, font, text_col, x, y, screen):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_controls_hud(screen, small_font):
    """Display game controls on screen"""
    hud_alpha = 180
    hud_surface = pygame.Surface((220, 160))
    hud_surface.set_alpha(hud_alpha)
    hud_surface.fill((0, 0, 0))
    screen.blit(hud_surface, (SCREEN_WIDTH - 230, 10))

    y_offset = 20
    draw_text('CONTROLS:', small_font, WHITE, SCREEN_WIDTH - 220, y_offset, screen)
    y_offset += 25
    draw_text('A/D: Move', small_font, WHITE, SCREEN_WIDTH - 220, y_offset, screen)
    y_offset += 22
    draw_text('W: Jump', small_font, WHITE, SCREEN_WIDTH - 220, y_offset, screen)
    y_offset += 22
    draw_text('SPACE: Shoot', small_font, WHITE, SCREEN_WIDTH - 220, y_offset, screen)
    y_offset += 22
    draw_text('E: Grenade', small_font, WHITE, SCREEN_WIDTH - 220, y_offset, screen)
    y_offset += 22
    draw_text('P: Pause', small_font, WHITE, SCREEN_WIDTH - 220, y_offset, screen)
    y_offset += 22
    draw_text('ESC: Quit', small_font, WHITE, SCREEN_WIDTH - 220, y_offset, screen)

def draw_pause_menu(screen, title_font, font, cheat_active):
    """Draw the pause menu overlay"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    draw_text('GAME PAUSED', title_font, YELLOW, SCREEN_WIDTH // 2 - 140, 100, screen)

    if cheat_active:
        draw_text('⚡ GOD MODE ACTIVE ⚡', font, GREEN, SCREEN_WIDTH // 2 - 120, 180, screen)

    draw_text('Press P to Resume', font, WHITE, SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 - 50, screen)
    draw_text('Press ESC to Exit', font, WHITE, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, screen)

def draw_bg(screen, bg_scroll, sky_img, mountain_img, pine1_img, pine2_img):
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

def draw_cheat_notification(screen, font, small_font, cheat_active):
    """Show notification when cheat is active"""
    if cheat_active:
        if pygame.time.get_ticks() % 1000 < 500:
            draw_text('⚡ GOD MODE ⚡', font, YELLOW, SCREEN_WIDTH // 2 - 80, 10, screen)
            draw_text('Infinite Health & Ammo', small_font, GREEN, SCREEN_WIDTH // 2 - 90, 40, screen)

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
