import pygame
import math
from animation import Animation
from weapon import Sickle, Bullet
from config import Config

class Entity:
    def __init__(self, x, y, hp, speed, name):
        self.name = name
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.state = "normal"
        self.state_timer = 0
        self.animation = Animation(name)
        sample_img = self.animation.frames['move']['right'][0]
        self.rect = sample_img.get_rect(topleft=(x, y))

    def take_dmg(self, amount):
        self.hp -= amount
        if self.hp <= 0: self.state = "dead"


class Player(Entity):
    def __init__(self, x, y, game):
        super().__init__(x, y, 100, 4, "player")
        self.game = game
        self.sickle = Sickle(self)
        self.inventory = []
        self.item_used_this_hour = []
        self.particles = []
        self.is_attacking = False
        self.attack_timer = 0
        self.invincibility_timer = 0

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        moving = False
        
        if keys[pygame.K_a]: dx -= 1; self.animation.direction = 'left'
        if keys[pygame.K_d]: dx += 1; self.animation.direction = 'right'
        if keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_s]: dy += 1

        if dx != 0 or dy != 0:
            moving = True
            length = math.hypot(dx, dy)
            self.x += (dx / length) * self.speed
            self.y += (dy / length) * self.speed

        self.rect.topleft  = (self.x, self.y)

        if self.is_attacking:
            self.attack_timer -= dt
            if self.attack_timer <= 0:
                self.is_attacking = False

        if keys[pygame.K_a]: 
            self.animation.direction = 'left'
        elif keys[pygame.K_d]: 
            self.animation.direction = 'right'

        self.animation.update(dt, moving, self.is_attacking)
        if self.state != "normal":
            self.state_timer -= dt
            if self.state_timer <= 0:
                if self.state == "fast":
                    self.speed = 4
                elif self.state == "poison":
                    self.sickle.damage = 25
                
                self.state = "normal"
                self.state_timer = 0
            
        if self.invincibility_timer > 0:
            self.invincibility_timer -= dt

        self.x = max(20, min(self.x, Config.WINDOW_WIDTH - 20))
        self.y = max(20, min(self.y, Config.WINDOW_HEIGHT - 20))

    def collect(self, plant):
        if plant.type in self.game.plants_collected:
            self.game.plants_collected[plant.type] += 1
            self.game.hour_plants_collected[plant.type] += 1
            idx = ["Fruit", "Vegetable", "Flower"].index(plant.type)
            if plant.rare == "rare":
                self.game.hour_scores[idx] += 50
                self.game.scores[idx] += 50
            else:
                self.game.hour_scores[idx] += 10
                self.game.scores[idx] += 10
        else:
            self.inventory.append(plant)

    def use_item(self, room):
        if self.inventory:
            item = self.inventory.pop(0)
            item.use(self, room)
            self.item_used_this_hour.append(item.name)

    def draw(self, screen):
        if self.invincibility_timer > 0:
            if int(pygame.time.get_ticks() / 50) % 2 == 0:
                return

        tint = None
        if self.state == "fast": tint = (100, 255, 100, 255)
        elif self.state == "harm": tint = (255, 100, 100, 255)
        elif self.state == "poison": tint = (150, 0, 255, 255)
        self.animation.draw(screen, self.x, self.y, tint)

    def take_dmg(self, amount):
        if self.invincibility_timer <= 0:
            super().take_dmg(amount)
            self.invincibility_timer = 0.5
            if self.state == "normal":
                self.state = "harm"
                self.state_timer = 0.5


class Enemy(Entity):
    def __init__(self, x, y, hp, speed, name):
        super().__init__(x, y, hp, speed, name)
        self.danger = "normal"
        self.rect = pygame.Rect(x, y, 30, 30)
        
    def chase(self, player):
        dx, dy = player.x - self.x, player.y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx/dist) * 1.3
            self.y += (dy/dist) * 1.3
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        tint = (255, 100, 100, 255) if self.danger == "danger" else None
        self.animation.draw(screen, self.x, self.y, tint)


class Barghest(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 2, "barghest")

    def chase(self, player, dt):
        dx, dy = player.x - self.x, player.y - self.y
        dist = math.hypot(dx, dy)
        
        if dist > 0:
            self.animation.direction = 'left' if dx < 0 else 'right'
            self.x += (dx/dist) * self.speed
            self.y += (dy/dist) * self.speed
            
            self.rect.topleft = (self.x, self.y)

            if self.rect.colliderect(player.rect):
                player.take_dmg(5)


class Venus_Trap(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 75, 0, "venus")
        self.shoot_cooldown = 0

    def chase(self, player, room, dt):
        self.shoot_cooldown += dt
        
        dx = player.rect.centerx - self.rect.centerx
        self.animation.direction = 'right' if dx > 0 else 'left'
        SHOOT_DELAY = 4.0 
        
        is_winding_up = self.shoot_cooldown > (SHOOT_DELAY - 0.5)
        self.animation.update(dt, False, is_winding_up)

        if self.shoot_cooldown >= SHOOT_DELAY:
            dy = player.rect.centery - self.rect.centery
            angle = math.atan2(dy, dx)
            
            room.projectiles.append(Bullet(self.rect.centerx, self.rect.centery, angle))
            self.shoot_cooldown = 0
