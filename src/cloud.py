import random
import pygame

class Cloud:
    def __init__(self, screen_width):
        self.x = screen_width + random.randint(20, 160)
        self.y = random.randint(35, 120)
        self.speed = random.uniform(35.0, 55.0)

    def update(self, dt):
        self.x -= self.speed * dt

    def draw(self, screen, color=(200, 200, 200)):
        x, y = int(self.x), int(self.y)
        pygame.draw.rect(screen, color, (x, y + 6, 52, 10))
        pygame.draw.rect(screen, color, (x + 10, y, 26, 6))
        pygame.draw.rect(screen, color, (x + 20, y - 4, 16, 4))


class GroundDetail:
    def __init__(self, screen_width, ground_y):
        self.x = screen_width + random.randint(0, 100)
        self.y = ground_y + 48 + random.randint(4, 18)
        self.length = random.choice([2, 4, 8, 12])

    def update(self, speed, dt):
        self.x -= speed * dt

    def draw(self, screen, color=(160, 160, 160)):
        pygame.draw.rect(screen, color, (int(self.x), int(self.y), self.length, 2))