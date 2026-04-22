import random
from plant import ItemPlant, Plant
from entities import Barghest, Venus_Trap

class Room:
    PLAY_X_MIN, PLAY_X_MAX = 140, 1140
    PLAY_Y_MIN, PLAY_Y_MAX = 160, 580
    def __init__(self, area_id):
        self.area_id = area_id
        self.plants = []
        self.enemies = []
        self.projectiles = []
        self.spawn_timer = 0
        level = {1: (0.4, 0.4, 0.2, 0.05, 0.0), 2: (0.3, 0.3, 0.4, 0.15, 0.25),
                   3: (0.2, 0.2, 0.6, 0.20, 0.25), 4: (0.3, 0.3, 0.4, 0.50, 0.50)}
        self.level = level[area_id]

    def spawn(self):
        GRASS_X = (200, 1080)
        GRASS_Y = (220, 500)
        x = random.randint(*GRASS_X)
        y = random.randint(*GRASS_Y)

        if len(self.plants) < 12:
            if random.random() < 0.2: # 10% chance for an Item Plant
                item = random.choice([("Aloe", "heal"), ("Hura", "blast"), ("Guarana", "speed"), ("Hemlock", "poison")])
                self.plants.append(ItemPlant(x,y, item[0], item[1]))
            else:
                rare = None
                if random.random() < self.level[4]:
                    rare = "rare"
                p_type = random.choices(["Fruit", "Vegetable", "Flower"], weights=self.level[:3])[0]
                self.plants.append(Plant(x,y, p_type, rare))
        
        if len(self.enemies) < 5:
            if random.random() < self.level[3]:
                x = random.randint(*GRASS_X)
                y = random.randint(*GRASS_Y)
                new_enemy = random.choice([Barghest(x,y), Venus_Trap(x,y)])
                if random.random() < self.level[4]: 
                    new_enemy.hp *= 1.5
                    new_enemy.danger = "danger"
                self.enemies.append(new_enemy)

    def update(self, player, dt):
        self.spawn_timer += dt
        if self.spawn_timer > 1.5:
            self.spawn()
            self.spawn_timer = 0

        for e in self.enemies[:]:
            if e.state == "dead": self.enemies.remove(e); continue
        
            if isinstance(e, Barghest):
                e.chase(player,dt)
                # Use the global dt from the update function
                e.animation.update(dt, True, False) 
            elif isinstance(e, Venus_Trap):
                e.chase(player, self, dt)

        for b in self.projectiles[:]:
            b.update()
            if b.rect.colliderect(player.rect):
                player.hp -= 15
                self.projectiles.remove(b)
            # Add bounds check for bullets
            elif not (0 < b.x < 1280 and 0 < b.y < 720):
                self.projectiles.remove(b)

    def draw(self, screen, player):
        render_list = self.plants + self.enemies + [player] + self.projectiles
    
        # Sort them so whoever is "lower" on the screen is drawn last (on top)
        render_list.sort(key=lambda obj: obj.rect.bottom)
        
        for obj in render_list:
            obj.draw(screen)
