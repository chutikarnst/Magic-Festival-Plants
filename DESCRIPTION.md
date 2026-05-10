# Project Description

## Project Overview
- **Magic Festival Plants:**  
- **Brief Description:**  
  Magic Festival Plants is a Roguelike game in a fantasy setting, the player is the town forager gathering various plants in a changing forest to give to the player's friends for the upcoming holiday.
  
  The player has to gather as many flowers, fruits, and vegetables before the end of the day or get gravely injured by monsters with a sickle as a weapon and other magical plants as special items.

- **Target Users:**  
  Anyone who is interested in dodging games (or crazy bored) to play this game.

- **Key Features:**  
  - Left-click to hit
  - Right-click to use plant item
  - R to pause the game or go back to menu page when the game is finish
  - WASD movement

- **Proposal**
  https://docs.google.com/document/d/11cY4sNPyxlbaryzxm-XvLM_QaWBiYtfhcY_Z1co-H4g/edit?usp=sharing

- **YouTube presentaion**
  https://youtu.be/mCBUa0F3O-M?si=hE_lkn3w-Qis38O-


---

## Concept

### Background
At first, I wanted to make a game about a chef getting exotic/rare ingredients to make a *perfect dish(tm)*. Going on different areas and each of them have a uniqe task (puzzle, fighting, platforming, etc). But I looked at the given time and realised, with the knowledge I had, that work would probably let me meet my recently deceased grandpa (Note: I am NOT suicidal, just emphasizing that this work is unrealistic). So I decided to do Magic Festival Plants.

The game was inspired by games such as Cult of the Lamb for movement, Stardew Valley for the vibe, DnD for one monster, and real life plants for the plant item power (it is exaggerated for fantasy purposes). The art for the entire game is drawn by me.

### Objectives
The player must get as many plants before the end of the day, or when hp bar is zero. If the hp is zero the game will end and check if the three score count as a win or not  


---

## UML Class Diagram
[UML](UML.png)


---

## Object-Oriented Programming Implementation
- **Config:** Basic config for window and map size.

- **Menu:** Menu ui for menu page.

- **SoundManager:** Load, play, and adjust when needed.

- **Game:** The main part of the game: inro, menu, pause, handle events, save data.

- **Animation:** Animation for the entities.

- **Entity:** Base class for Enemy and Player.

- **Player(Entity):** Player can move, use item in inventory, hit/collect plants.

- **Enemy(Entity):** Overall things a typical enemy can do (chase).

- **Barghest(Enemy):** Chase the player and deal dmg.

- **Venus_Trap(Enemy):** Shoot the bullet towards the player.

- **Plant:** For the player to pick up scores, has a rare attribute to see if this plant will get higher score.

- **ItemPlant:** When used, it will check the name and play the code for the item.

- **Bullet:** get the player's position and shoot towards it.

- **Sickle:** The weapon the player has, collect plants, hit enemies, and update damage when the player uses an item that boosts damage in a time limit.

- **Particle:** when heal and blast is used the particle will show up.

- **Room:** Have the information on different rate of plants to spawn and rate for dangerous monsters, spawn plants and enemies, and updates the room.


---

## Statistical Data

### Data Recording Method
  - 1 row of data is 1 game hour (30 seconds) the game timer is 6 minutes must play it 9 times to get more than 100 rows
  - All data will be saved in [CSV](game_data.csv)


### Data Features
- **Game_ID:** number of the game played
- **Area_ID:** current area id
- **Hour:** current hour
- **Fr,V,Fl_Score:** score of each hour (Fr: Fruit, V: Vegetable, Fl: Flower)
- **Item_used:**: items that was used at that hour
- **Fruit, Vegetable, Flower:** number of each plant collectet


---

## Changed Proposed Features (Optional)
  - added and changed OOP class


---

## External Sources
**Music:**
  all music is from [Free To Use](https://freetouse.com/music)
  [License information](https://freetouse.com/license)

  - [Naturally](sounds/forest_ambient.mp3)
    by Pufino
    https://freetouse.com/music/pufino/naturally

  - [Serenity](sounds/game_over.mp3)
    by Pufino
    https://freetouse.com/music/pufino/serenity

  - [Enjoy](sounds/intro_theme.mp3)
    by Pufino
    https://freetouse.com/music/pufino/enjoy

  - [Foreign](sounds/menu_theme.mp3)
    by Moavii
    https://freetouse.com/music/moavii/foreign