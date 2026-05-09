import pygame
import threading
import os
import csv
import sys
from os.path import join

from sound import SoundManager
from config import Config
from entities import Player
from room import Room
from menu import Menu
from data_dashboard import open_data_dashboard

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT))
        pygame.display.set_caption("Magic Festival Plants")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)

        self.background_img = pygame.image.load(join("map", "background.PNG")).convert()
        self.foreground_img = pygame.image.load(join("map", "foreground.PNG")).convert_alpha()
        self.intro_bg = pygame.image.load(join("menu", "intro_background.png")).convert()
        self.menu_bg = pygame.image.load(join("menu", "menu_background.png")).convert()
        self.sound_manager = SoundManager()

        self.state = "INTRO" 
        self.menu_manager = Menu()
        
        self.reset_game_logic()

    def reset_game_logic(self):
        self.game_session_id = self.get_next_session_id()
        self.player = Player(400, 400, self)
        self.current_area = 1
        self.rooms = {i: Room(i) for i in range(1, 5)}
        
        self.plants_collected = {"Fruit": 0, "Vegetable": 0, "Flower": 0}
        self.hour_plants_collected = {"Fruit": 0, "Vegetable": 0, "Flower": 0} 
        self.scores = [0, 0, 0] # [Fruit, Veg, Flower]
        self.hour_scores = [0, 0, 0]
        
        self.current_hour = 1
        self.hour_timer = 0
        self.total_game_time = 0

    def get_next_session_id(self):
        filename = 'game_data.csv'
        if not os.path.exists(filename): return 1
        try:
            with open(filename, mode='r') as f:
                reader = csv.DictReader(f)
                ids = [int(row['Game_ID']) for row in reader]
                return max(ids) + 1 if ids else 1
        except: return 1

    def save_hour_data(self):
        """Saves a row of data every 30 seconds"""
        file_exists = os.path.isfile('game_data.csv')
        with open('game_data.csv', mode='a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Game_ID", "Area_ID", "Hour", "Fr_Score", "V_Score", "Fl_Score", "Item_used", "Fruit", "Vegetable", "Flower"])
            
            writer.writerow([
                self.game_session_id, self.current_area, self.current_hour,
                self.hour_scores[0], self.hour_scores[1], self.hour_scores[2],
                "|".join(self.player.item_used_this_hour),
                self.hour_plants_collected["Fruit"], self.hour_plants_collected["Vegetable"], self.hour_plants_collected["Flower"]
            ])
        self.hour_scores = [0,0,0]
        self.player.item_used_this_hour = []
        self.hour_plants_collected = {"Fruit": 0, "Vegetable": 0, "Flower": 0} 

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = event.pos
                if self.state == "INTRO":
                    self.state = "MENU"
                elif self.state == "MENU":
                    if self.menu_manager.start_btn.collidepoint(m_pos):
                        self.reset_game_logic()
                        self.state = "PLAYING"
                    elif self.menu_manager.sound_btn.collidepoint(m_pos):
                        new_vol = self.sound_manager.volume + 0.1
                        if new_vol > 1.0:
                            new_vol = 0.0
                        self.sound_manager.set_volume(new_vol)
                        print(f"Volume set to: {int(self.sound_manager.volume * 100)}%")
                    elif self.menu_manager.data_btn.collidepoint(m_pos):
                        threading.Thread(target=open_data_dashboard, daemon=True).start()
                    elif self.menu_manager.exit_btn.collidepoint(m_pos):
                        pygame.quit()
                        sys.exit()
                elif self.state == "PLAYING":
                    if event.button == 1: # Left Click
                        self.player.sickle.harvest(self.rooms[self.current_area])
                    if event.button == 3: # Right Click
                        self.player.use_item(self.rooms[self.current_area])

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if self.state == "END":
                        self.state = "MENU"
                    elif self.state == "PLAYING":
                        self.state = "PAUSED"
                    elif self.state == "PAUSED":
                        self.state = "PLAYING"

    def update(self):
        dt = self.clock.tick(60) / 1000 
        self.sound_manager.play_state_music(self.state)
        if self.state == "PLAYING":
            self.player.update(dt)
            self.rooms[self.current_area].update(self.player, dt)
            
            for p in self.player.particles[:]:
                p.update(dt)
                if p.life <= 0:
                    self.player.particles.remove(p)

            self.hour_timer += dt
            if self.hour_timer >= 30:
                self.save_hour_data()
                self.current_hour += 1
                self.hour_timer = 0
            
            if self.player.x > Config.WINDOW_WIDTH - 50:
                if self.current_area in [1, 3]:
                    self.current_area += 1
                    self.player.x = 60 
            
            elif self.player.x < 50:
                if self.current_area in [2, 4]: 
                    self.current_area -= 1
                    self.player.x = Config.WINDOW_WIDTH - 60

            if self.player.y > Config.WINDOW_HEIGHT - 50:
                if self.current_area in [1, 2]: 
                    self.current_area += 2
                    self.player.y = 60
            
            elif self.player.y < 50:
                if self.current_area in [3, 4]: 
                    self.current_area -= 2
                    self.player.y = Config.WINDOW_HEIGHT - 60

            if self.current_hour > 12 or self.player.hp <= 0:
                self.state = "END"

    def draw_ui(self):
        # 1. Stats Bar
        stats_rect = pygame.Rect(Config.WINDOW_WIDTH//2 - 300, 20, 600, 50)
        pygame.draw.rect(self.screen, (150, 100, 200), stats_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), stats_rect, 2)
        
        stats_str = f"Fruits: {self.scores[0]:04}  |  Veggies: {self.scores[1]:04}  |  Flowers: {self.scores[2]:04}  |  Room Area: {self.current_area}"
        stats_surf = self.font.render(stats_str, True, (0, 0, 0))
        self.screen.blit(stats_surf, (stats_rect.x + 20, stats_rect.y + 12))

        # 2. Health Box
        hp_rect = pygame.Rect(10, 10, 180, 80)
        pygame.draw.rect(self.screen, (50, 80, 200), hp_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), hp_rect, 2)
        hp_text = self.font.render(f"Health", True, (255, 255, 255))
        hp_val = self.font.render(f"{int(self.player.hp)}/100", True, (255, 255, 255))
        self.screen.blit(hp_text, (70, 20))
        self.screen.blit(hp_val, (70, 45))

        # 3. Hour Box
        hour_rect = pygame.Rect(Config.WINDOW_WIDTH - 200, 10, 180, 60)
        pygame.draw.rect(self.screen, (255, 255, 255), hour_rect)
        pygame.draw.rect(self.screen, (200, 0, 0), hour_rect, 3)
        hour_text = self.font.render(f"Hour: {self.current_hour}/12", True, (0, 0, 0))
        self.screen.blit(hour_text, (hour_rect.x + 40, hour_rect.y + 15))

        inv_rect = pygame.Rect(10, 120, 80, 500)
        pygame.draw.rect(self.screen, (230, 220, 200), inv_rect) # Beige box
        pygame.draw.rect(self.screen, (180, 150, 100), inv_rect, 2)
        
        inv_label = self.font.render("Item", True, (0, 0, 0))
        self.screen.blit(inv_label, (25, 95))
        
        # inventory items 
        for i, item in enumerate(self.player.inventory[:8]):
            slot_x = 20
            slot_y = 140 + (i * 60)
            if hasattr(item, 'image'):
                self.screen.blit(item.image, (slot_x, slot_y))

    def draw(self):
        if self.state == "INTRO":
            self.screen.blit(self.intro_bg, (0, 0))
            txt = self.title_font.render("CLICK TO START", True, (255, 255, 255))
            self.screen.blit(txt, (Config.WINDOW_WIDTH//2 - 130, 500))
            
        elif self.state == "MENU":
            self.screen.blit(self.menu_bg, (0, 0))
            self.menu_manager.draw(self.screen)
            
        elif self.state == "PLAYING":
            # 1. Background
            self.screen.blit(self.background_img, (0, 0))
            
            # 2. Room Content
            self.rooms[self.current_area].draw(self.screen, self.player)
            
            # 3. Particles 
            for p in self.player.particles:
                p.draw(self.screen)
            
            # 4. Player
            self.player.draw(self.screen)
            
            # 5. Foreground and UI
            self.screen.blit(self.foreground_img, (0, 0))
            self.draw_ui()

        elif self.state == "PAUSED":
            self.screen.blit(self.background_img, (0, 0))
            self.rooms[self.current_area].draw(self.screen, self.player)
            self.player.draw(self.screen)
            
            overlay = pygame.Surface((Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            
            pause_txt = self.title_font.render("PAUSED - Press R to Resume", True, (255, 255, 255))
            self.screen.blit(pause_txt, (Config.WINDOW_WIDTH//2 - 180, Config.WINDOW_HEIGHT//2))

        elif self.state == "END":
            self.screen.fill((20, 20, 30))
            msg = "WINNER!" if self.player.hp > 0 else "GAME OVER"
            msg = "WINNER!" if self.scores[0] > 300 and self.scores[1] > 300 and self.scores[2] > 300 else "GAME OVER"
            if msg == "WINNER!":
                self.screen.blit(pygame.image.load(join("menu", "win_background.png")).convert(), (0, 0))
            else:
                self.screen.blit(pygame.image.load(join("menu", "lose_background.png")).convert(), (0, 0))
            color = (0, 255, 0) if self.player.hp > 0 else (255, 0, 0)
            img = self.title_font.render(msg, True, color)
            self.screen.blit(img, (320, 100))
            self.screen.blit(self.font.render("Press R to return to Menu", True, (150, 150, 150)), (250, 450))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()

if __name__ == "__main__":
    game = Game()
    game.run()
