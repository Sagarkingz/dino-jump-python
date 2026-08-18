import random
import pygame

class Obstacle:
    def __init__(self, screen_width, ground_y):
        self.screen_width = screen_width
        self.ground_y = ground_y
        
        # 4 Diverse Obstacle Types
        self.type = random.choices(
            ["cactus_cluster", "cactus_saguaro", "crawler_bug", "pterodactyl"],
            weights=[35, 30, 20, 15]
        )[0]

        if self.type == "cactus_saguaro":
            self.width = 24
            self.height = 46
            self.x = screen_width
            self.y = ground_y + 48 - self.height

        elif self.type == "cactus_cluster":
            self.width = 46
            self.height = 48
            self.x = screen_width
            self.y = ground_y + 48 - self.height

        elif self.type == "crawler_bug":
            # Low ground crawling creature
            self.width = 34
            self.height = 20
            self.x = screen_width
            self.y = ground_y + 50 - self.height
            self.anim_tick = 0.0

        elif self.type == "pterodactyl":
            # Variable flight altitudes (High, Medium, Low)
            self.width = 44
            self.height = 30
            self.x = screen_width
            self.y = ground_y - random.choice([10, 48, 85])
            self.wing_frame = 0.0

    def update(self, speed):
        self.x -= speed
        if self.type == "pterodactyl":
            self.wing_frame = (self.wing_frame + 0.18) % 2.0
        elif self.type == "crawler_bug":
            self.anim_tick = (self.anim_tick + 0.25) % 2.0

    def draw(self, screen, color=(75, 75, 75)):
        x, y = int(self.x), int(self.y)

        if self.type == "cactus_saguaro":
            # Central thick trunk
            pygame.draw.rect(screen, color, (x + 8, y, 9, self.height))
            # Left branch
            pygame.draw.rect(screen, color, (x, y + 12, 8, 14))
            pygame.draw.rect(screen, color, (x, y + 12, 12, 5))
            # Right branch
            pygame.draw.rect(screen, color, (x + 16, y + 18, 8, 14))
            pygame.draw.rect(screen, color, (x + 12, y + 18, 12, 5))

        elif self.type == "cactus_cluster":
            # Three varied cacti bunched together
            pygame.draw.rect(screen, color, (x + 4, y + 8, 7, self.height - 8))
            pygame.draw.rect(screen, color, (x, y + 16, 5, 8))
            pygame.draw.rect(screen, color, (x + 18, y, 9, self.height))
            pygame.draw.rect(screen, color, (x + 27, y + 10, 6, 12))
            pygame.draw.rect(screen, color, (x + 36, y + 14, 7, self.height - 14))

        elif self.type == "crawler_bug":
            # Ground scorpion/bug with pincer and tail
            pygame.draw.ellipse(screen, color, (x + 8, y + 6, 20, 12))
            # Stinger Tail
            pygame.draw.rect(screen, color, (x, y + 2, 8, 4))
            pygame.draw.rect(screen, color, (x + 2, y, 4, 6))
            # Pincers
            pygame.draw.rect(screen, color, (x + 26, y + 4, 8, 4))
            pygame.draw.rect(screen, color, (x + 26, y + 12, 8, 4))
            # Legs animation
            leg_off = 3 if self.anim_tick < 1.0 else -3
            pygame.draw.line(screen, color, (x + 12, y + 16), (x + 10 + leg_off, y + 20), 2)
            pygame.draw.line(screen, color, (x + 20, y + 16), (x + 22 - leg_off, y + 20), 2)

        elif self.type == "pterodactyl":
            # Head, Beak, and Eye
            pygame.draw.polygon(screen, color, [(x + 26, y + 14), (x + 44, y + 10), (x + 30, y + 18)])
            pygame.draw.rect(screen, color, (x + 10, y + 10, 20, 9))

            # 2-Frame Flapping Wings
            if self.wing_frame < 1.0:
                # Wings Raised
                pygame.draw.polygon(screen, color, [(x + 14, y + 10), (x + 22, y - 10), (x + 26, y + 10)])
            else:
                # Wings Lowered
                pygame.draw.polygon(screen, color, [(x + 14, y + 14), (x + 22, y + 28), (x + 26, y + 14)])

    def get_mask(self):
        return pygame.Rect(self.x + 2, self.y + 2, self.width - 4, self.height - 2)