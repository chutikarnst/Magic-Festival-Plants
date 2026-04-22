import math
import pygame

class Sickle:
    def __init__(self, owner):
        self.owner = owner
        self.damage = 25  
        self.reach = 110  # Horizontal reach
        self.swing_height = 160 # Vertical coverage

    def harvest(self, room):
        self.owner.is_attacking = True
        self.owner.attack_timer = 0.35 

        hit_rect = pygame.Rect(
            self.owner.rect.centerx - (self.reach//2) + 15, 
            self.owner.rect.centery, 
            self.reach*2, 
            self.swing_height
        )

        for e in room.enemies[:]:
            if hit_rect.colliderect(e.rect):
                e.take_dmg(self.damage)
                
        # Process Plants
        for p in room.plants[:]:
            if hit_rect.colliderect(p.rect):
                if p.type == "Item": 
                    self.owner.inventory.append(p)
                else:
                    self.owner.collect(p)
                room.plants.remove(p)

class Bullet:
    def __init__(self, x, y, angle):
        self.x, self.y = x, y
        self.angle = angle
        self.speed = 5
        self.rect = pygame.Rect(x, y, 10, 10)

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 10)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 6)
