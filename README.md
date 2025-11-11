# War Grids - Platform Shooter Game

A Python-based 2D platform shooter game built with Pygame featuring multiple levels, enemies, collectibles, and an engaging combat system.

## 🎮 How to Run

```bash
python shooter_tut.py
```

Make sure you have Pygame installed:
```bash
pip install pygame
```

## 🕹️ Game Controls

| Action | Key |
|--------|-----|
| Move Left | ← (Left Arrow) |
| Move Right | → (Right Arrow) |
| Jump | SPACE |
| Shoot | Q |
| Throw Grenade | E |
| Exit Game | ESC |

## 📊 Features

### Gameplay
- **3 Challenging Levels** with increasing difficulty
- **Smart Enemy AI** that detects and attacks the player
- **Combat System** with guns and grenades
- **Collectible Items**: Health boxes, ammo crates, and grenades
- **Environmental Hazards**: Water tiles (instant death)
- **Score System** tracking kills and pickups
- **Level Progression** with fade effects

### Visual Elements
- **Dynamic Parallax Background** with mountains and trees
- **Smooth Animations** for idle, run, jump, and death
- **Health Bar** with color-coded warning system
- **Real-time HUD** showing:
  - Health (with percentage colors)
  - Ammo count
  - Grenade count
  - Current level
  - Enemy count
  - Score and kills
  - Controls reference panel

### Game Mechanics
- **Physics-based Movement** with gravity
- **Scrolling Levels** that follow the player
- **Collision Detection** for terrain, bullets, and grenades
- **Explosion Effects** from grenades
- **Item Animations** with bobbing effect
- **Victory/Death Screens** with restart option

## 🎯 Scoring

- **Enemy Kill** (bullet): 100 points
- **Enemy Kill** (grenade): 150 points  
- **Health Pickup**: +10 points
- **Ammo Pickup**: +5 points
- **Grenade Pickup**: +15 points

## 🎨 Game Assets

The game uses the following asset directories:
- `img/player/` - Player character animations
- `img/enemy/` - Enemy character animations
- `img/background/` - Background layers
- `img/tile/` - Level tiles (21 types)
- `img/icons/` - UI elements and items
- `img/explosion/` - Explosion animation frames
- `audio/` - Sound effects and music

## 🛠️ Level Editor

Use `level_editor_tut.py` to create custom levels:
- Place tiles by clicking
- Save/Load level data
- 21 different tile types including:
  - Terrain blocks
  - Water hazards
  - Decorations
  - Player spawn
  - Enemy spawn
  - Item boxes
  - Level exit

## 📝 Files

- `shooter_tut.py` - Main game file (IMPROVED VERSION)
- `level_editor_tut.py` - Level editor tool
- `button.py` - Button UI class
- `menu.py` - Menu system example
- `level0_data.csv` through `level3_data.csv` - Level data
- `GAME_IMPROVEMENTS.md` - Detailed list of improvements
- `CONTROLS_REFERENCE.txt` - Quick controls reference

## 🎮 Gameplay Tips

1. **Conserve Ammo**: You start with limited ammo - pick up ammo boxes!
2. **Use Grenades Wisely**: They deal massive damage and give bonus points
3. **Watch Your Health**: The health bar changes color as a warning
4. **Explore Levels**: Find all item boxes for maximum score
5. **Strategic Shooting**: Enemies can shoot back - take cover behind blocks
6. **Jump Carefully**: Falling in water means instant death
7. **Kill All Enemies**: Clear each area before proceeding

## 🔧 Customization

Easy-to-modify difficulty settings in `shooter_tut.py`:

```python
PLAYER_SPEED = 5              # Movement speed (1-10)
PLAYER_JUMP_VELOCITY = -13    # Jump height (higher negative = higher jump)
ENEMY_DETECTION_RANGE = 150   # Enemy vision (in pixels)
PLAYER_SHOOT_COOLDOWN = 15    # Shooting speed (lower = faster)
```

## 🚀 What's New (Latest Update)

### ✅ Changed Controls
- Movement now uses **Arrow Keys** instead of A/D
- Jump changed from W to **SPACE**
- Shoot changed from SPACE to **Q**
- Grenade changed from Q to **E**

### ✅ Gameplay Improvements
- Added comprehensive **score system**
- **Health bar** now shows numeric values with color coding
- **Better bullet speed** and lifetime tracking
- **Item boxes animate** with bobbing effect
- **Improved jumping** mechanics
- **Faster shooting** cooldown

### ✅ Visual Improvements
- **Enhanced main menu** with full controls display
- **In-game controls panel** (semi-transparent, top-right)
- **Level complete screen** with pause
- **Victory screen** after beating all levels
- **Color-coded warnings** for low resources
- **Real-time enemy counter**

### ✅ Code Quality
- Better organized with clear comments
- Reusable UI functions
- Configurable difficulty constants
- Improved game state management
- Clean reset functionality

## 🐛 Known Issues

None at this time! The game has been tested and all systems are working correctly.

## 📄 License

This is an educational project. Feel free to modify and learn from it!

## 🤝 Contributing

This is a learning project. Feel free to:
- Add new levels
- Create new enemy types
- Add power-ups
- Improve graphics
- Add sound effects

---

**Have fun playing War Grids! Try to beat all 3 levels with the highest score possible! 🎮**
