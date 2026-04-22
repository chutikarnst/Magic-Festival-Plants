import pygame
import math
import random
from particle import Particle
import os

class Plant:
    def __init__(self, x, y, p_type, rare=None):
        self.x = x
        self.y = y
        self.type = p_type
        variant = random.randint(0, 2)
        self.rare = rare
        if rare=="rare":
            variant = 3
        filename = f"{p_type}{variant}.png" 
        path = os.path.join("plant", filename)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class ItemPlant:
    def __init__(self, x, y, name, effect_type):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.name = name
        self.effect_type = effect_type
        self.type = "Item"
        path = os.path.join("plant", f"{self.name}.png")
        self.image = pygame.image.load(path).convert_alpha()

    def use(self, player, room):
        if self.effect_type == "heal": #Aloe_vera
            player.hp = min(100, player.hp + 30)
            player.particles.append(Particle(player.rect.centerx + 50, player.rect.centery + 50, (0, 255, 0)))

        if self.effect_type == "blast": #Hura_Crepitans
            for e in room.enemies[:]:
                dist = math.hypot(e.x - player.x, e.y - player.y)
                if dist < 150:
                    room.enemies.remove(e)
            player.particles.append(Particle(player.rect.centerx + 50, player.rect.centery + 50, (255, 69, 0), size=150))

        if self.effect_type == "speed":
            player.state = "fast"
            player.speed = 8
            player.state_timer = 3
           
        if self.effect_type == "poison":
            player.state = "poison"
            player.sickle.damage *= 2
            player.state_timer = 3

    def draw(self, screen):
        screen.blit(self.image, self.rect)

