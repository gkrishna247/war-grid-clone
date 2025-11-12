# War Grids - A 2D Platform Shooter

War Grids is a fast-paced 2D platform shooter built with Pygame. It features multiple levels, a variety of enemies, and a classic arcade feel. This project has been refactored for better performance, readability, and modularity, making it an excellent starting point for anyone looking to build their own 2D shooter.

## 🚀 Getting Started

Follow these instructions to get the game up and running on your local machine.

### Prerequisites

You'll need to have Python and `pip` installed. You can download them from the official Python website.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```
2.  **Install Pygame:**
    ```bash
    pip install pygame
    ```

### Running the Game

To start the game, run the `main.py` script from the `src` directory:

```bash
python3 src/main.py
```

## 🎮 Gameplay

### Controls

| Action          | Key              |
| --------------- | ---------------- |
| **Move Left**   | `A` or `←` (Left Arrow) |
| **Move Right**  | `D` or `→` (Right Arrow) |
| **Jump**        | `W` or `↑` (Up Arrow) |
| **Shoot**       | `Spacebar`       |
| **Throw Grenade** | `E`              |
| **Pause/Resume**| `P`              |
| **Exit Game**   | `ESC`            |

### Objective

The goal of each level is to eliminate all the enemies and reach the exit. As you progress, the levels will become more challenging, with more enemies and trickier platforming.

### Scoring

You'll earn points for various actions in the game:

| Action             | Points |
| ------------------ | ------ |
| **Enemy Kill**     | `100`  |
| **Grenade Kill**   | `150`  |
| **Health Pickup**  | `10`   |
| **Ammo Pickup**    | `5`    |
| **Grenade Pickup** | `15`   |

## ✨ Features

*   **Modular Codebase:** The project has been refactored into a clean, easy-to-understand structure, making it perfect for learning and extending.
*   **Performance Optimized:** Assets are pre-loaded to ensure smooth, lag-free gameplay.
*   **Dynamic Gameplay:** Features include a variety of enemies, collectible items (health, ammo, grenades), and environmental hazards.
*   **Particle Effects:** Visual flair is added with particle effects for bullet impacts.
*   **Cheat Codes:** For a little extra fun, a "God Mode" cheat code is included (`thor`).

## 📂 Project Structure

The project has been refactored to follow a modular structure, making it easy to navigate and maintain. All the game's source code is located in the `src` directory.

| File / Directory   | Description                                                                                                                              |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **`src/`**         | The main directory for all the game's source code.                                                                                        |
| `├── main.py`      | The entry point of the game. It manages the main game loop, handles top-level events, and orchestrates the different game modules.         |
| `├── settings.py`  | A centralized configuration file that contains all the game's constants, such as screen dimensions, colors, gravity, and player speed.     |
| `├── assets.py`    | Responsible for loading all the game's assets (images, sounds) at the start of the game. This pre-loading strategy improves performance. |
| `├── sprites.py`   | Contains all the game's sprite classes, including `Soldier`, `Bullet`, `Grenade`, `Explosion`, `ItemBox`, and `Particle`.                    |
| `├── world.py`     | Manages the game world, including the `World` class and other environment-related classes like `Decoration`, `Water`, and `Exit`.         |
| `├── ui.py`        | Contains all the UI elements, such as the `HealthBar`, `Button` class, and text-drawing functions.                                        |
| **`img/`**         | A directory containing all the game's images, organized into subdirectories for background, enemies, icons, player, and tiles.            |
| **`audio/`**       | Contains all the game's sound effects and music.                                                                                        |
| **`level_data/`**  | CSV files that define the layout of each level.                                                                                          |

## 🛠️ Level Editor

This project includes a simple, easy-to-use level editor that allows you to create your own custom levels for the game.

### How to Use

1.  **Run the Level Editor:**
    ```bash
    python3 level_editor.py
    ```
2.  **Create Your Level:**
    *   Click on the tiles in the right-hand panel to select them.
    *   Click on the main grid to place the selected tile.
    *   To erase, select the "Eraser" tile (the empty one).
3.  **Save/Load:**
    *   Use the "Save" and "Load" buttons to save your creations and load them back in for further editing.
    *   Levels are saved as `.csv` files, which the game can read directly.
