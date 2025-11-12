# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# Frame rate
FPS = 60

# Game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 22
MAX_LEVELS = 3

# Game difficulty settings
PLAYER_SPEED = 5  # Default player speed
PLAYER_JUMP_VELOCITY = -13  # Jump strength (negative = upward)
ENEMY_DETECTION_RANGE = 150  # How far enemies can see
PLAYER_SHOOT_COOLDOWN = 15  # Frames between shots (lower = faster)

# Cheat code
CHEAT_CODE = "thor"

# Colors
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
