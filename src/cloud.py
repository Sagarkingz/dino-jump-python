import random
import pygame

class Cloud:
    def __init__(self, screen_width):
        self.x = screen_width + random.randint(20, 150)
        self.y = random.randint(40, 130)
        self.speed = 1.8

    def update(self):
        self.x -= self.speed

    def draw(self, screen, color=(180, 180, 180)):
        x, y = int(self.x), int(self.y)
        # Classic 2D segmented cloud block
        pygame.draw.rect(screen, color, (x, y + 6, 50, 10))
        pygame.draw.rect(screen, color, (x + 10, y, 25, 6))
        pygame.draw.rect(screen, color, (x + 20, y - 4, 15, 4))