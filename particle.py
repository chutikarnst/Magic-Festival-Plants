import pygame

class Particle:
    def __init__(self, x, y, color, size=20):
        self.x, self.y = x, y
        self.color = color
        self.life = 1.0 
        self.size = size

    def update(self, dt):
        self.life -= dt

    def draw(self, screen):
        alpha = int(self.life * 255)
        s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
        screen.blit(s, (self.x - self.size, self.y - self.size))
    