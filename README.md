# Magic Festival Plants

## Project Description

- Project by: Chutikarn Stenger
- Game Genre: Fantacy Roguelike game

Magic Festival Plants is a Roguelike game in a fantasy setting, the player is the town forager gathering various plants in a changing forest to give to their best friend and his husband to prepare the upcoming festival.

The player has to gather as many flowers, fruits, and vegetables before the end of the day or get gravely injured by monsters with a sickle as a weapon and other magical plants as special items.

---

## Installation
To Clone this project:
```sh
git clone https://github.com/chutikarnst/Magic-Festival-Plants.git
```

To create and run Python Environment for This project:

Window:
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Mac:
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Running Guide
After activate Python Environment of this project, you can process to run the game by:

Window:
```bat
python main.py
```

Mac:
```sh
python3 main.py
```

---

## Tutorial / Usage
1. run the main.py code
2. read the pages(optional), then click to menu
3. start game
  - Left-click to hit
  - Right-click to use plant item
  - R to pause the game or go back to menu page when the game is finish
  - WASD movement

---

## Game Features
- 1 game hour is 30 second real-time and the game timer is 12 hours (6 minutes)

- Killing monsters does NOT add the score. The main focus is to survive and get plants

- 4 Special plants that the player can use (damage, heal, speed, poison)

- 4 big areas to move around. Each area has a different rate of plants to spawn and rate for dangerous monsters. Table for the map layout
  1. Starting area: very low chance of rare plants, low chance for more dangerous monsters to spawn
  2. low chance of rare flowers medium chance of rare fruits and vegetables, medium chance for more dangerous monsters to spawn
  3. low chance of rare fruits and vegetables medium chance of rare flowers, medium chance for more dangerous monsters to spawn
  4. High chance of rare fruits, vegetables, flowers, but also high chance for more dangerous monsters to spawn

---

## Known Bugs
The scores for the plants and rare plants are the same (the rare plants should have get more score). I found the reason but it is too late to fix it.
the data window won't update hourly, only when the game is done and open a new data window. If exit the game while the data window is open, it will get an error.

---

## Unfinished Works
My task are satisfactory (despite some minor error) 

---

## External sources
Acknowledge to:
1. Free To Use, https://freetouse.com/music [game background music]
