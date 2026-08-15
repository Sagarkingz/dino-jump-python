import random
import pygame

class Obstacle:
    def __init__(self, screen_width, ground_y):
        self.screen_width = screen_width
        self.ground_y = ground_y
        self.type = random.choice(["cactus_single", "cactus_double", "bird"])

        if self.type == "cactus_single":
            self.width = 20
            self.height = 42
            self.x = screen_width
            self.y = ground_y + 48 - self.height
        elif self.type == "cactus_double":
            self.width = 38
            self.height = 46
            self.x = screen_width
            self.y = ground_y + 48 - self.height
        else:
            # 2D Flying Bird (Pterodactyl)
            self.width = 42
            self.height = 28
            self.x = screen_width
            self.y = ground_y - random.choice([15, 55])
            self.wing_frame = 0

    def update(self, speed):
        self.x -= speed
        if self.type == "bird":
            self.wing_frame = (self.wing_frame + 0.18) % 2

    def draw(self, screen, color=(83, 83, 83)):
        x, y = int(self.x), int(self.y)

        if self.type == "cactus_single":
            # Main stem
            pygame.draw.rect(screen, color, (x + 6, y, 8, self.height))
            # Left arm
            pygame.draw.rect(screen, color, (x, y + 10, 6, 12))
            pygame.draw.rect(screen, color, (x, y + 10, 10, 4))
            # Right arm
            pygame.draw.rect(screen, color, (x + 14, y + 16, 6, 10))
            pygame.draw.rect(screen, color, (x + 10, y + 16, 10, 4))

        elif self.type == "cactus_double":
            # First cactus
            pygame.draw.rect(screen, color, (x + 4, y + 6, 8, self.height - 6))
            pygame.draw.rect(screen, color, (x, y + 14, 5, 8))
            # Second cactus
            pygame.draw.rect(screen, color, (x + 22, y, 8, self.height))
            pygame.draw.rect(screen, color, (x + 28, y + 12, 6, 10))

        elif self.type == "bird":
            # Body & Beak
            pygame.draw.rect(screen, color, (x + 8, y + 10, 24, 8))
            pygame.draw.rect(screen, color, (x + 30, y + 12, 8, 4))
            pygame.draw.rect(screen, color, (x + 4, y + 8, 6, 6))

            # Flapping 2D Wings
            if self.wing_frame < 1:
                # Wings Up
                pygame.draw.rect(screen, color, (x + 14, y, 6, 10))
            else:
                # Wings Down
                pygame.draw.rect(screen, color, (x + 14, y + 16, 6, 10))

    def get_mask(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)