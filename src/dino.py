import pygame

class Dino:
    def __init__(self, x=60, y=260):
        self.x = x
        self.ground_y = y
        self.y = self.ground_y
        self.width = 44
        self.height = 48
        self.vy = 0
        # Chrome Dino standard gravity & jump balance
        self.jump_force = -11.8
        self.gravity = 0.58
        self.is_grounded = True
        self.leg_step = 0

    def jump(self):
        if self.is_grounded:
            self.vy = self.jump_force
            self.is_grounded = False

    def update(self):
        self.y += self.vy
        self.vy += self.gravity

        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.vy = 0
            self.is_grounded = True

        if self.is_grounded:
            self.leg_step = (self.leg_step + 0.15) % 2

    def draw(self, screen, color=(83, 83, 83), bg_color=(247, 247, 247)):
        x, y = int(self.x), int(self.y)

        # 1. Tail
        pygame.draw.rect(screen, color, (x, y + 20, 6, 8))
        pygame.draw.rect(screen, color, (x + 4, y + 16, 6, 16))

        # 2. Body
        pygame.draw.rect(screen, color, (x + 8, y + 12, 22, 24))

        # 3. Head & Snout
        pygame.draw.rect(screen, color, (x + 18, y, 22, 14))
        pygame.draw.rect(screen, color, (x + 36, y + 2, 8, 12))

        # 4. Eye & Open Mouth Cutout
        pygame.draw.rect(screen, bg_color, (x + 24, y + 3, 4, 4))
        pygame.draw.rect(screen, bg_color, (x + 32, y + 8, 12, 4))

        # 5. Front Arm
        pygame.draw.rect(screen, color, (x + 28, y + 20, 6, 3))
        pygame.draw.rect(screen, color, (x + 32, y + 23, 2, 4))

        # 6. Legs
        if self.is_grounded:
            if self.leg_step < 1:
                pygame.draw.rect(screen, color, (x + 14, y + 36, 4, 12))
                pygame.draw.rect(screen, color, (x + 14, y + 45, 7, 3))
                pygame.draw.rect(screen, color, (x + 24, y + 36, 4, 6))
            else:
                pygame.draw.rect(screen, color, (x + 14, y + 36, 4, 6))
                pygame.draw.rect(screen, color, (x + 24, y + 36, 4, 12))
                pygame.draw.rect(screen, color, (x + 24, y + 45, 7, 3))
        else:
            pygame.draw.rect(screen, color, (x + 14, y + 36, 4, 8))
            pygame.draw.rect(screen, color, (x + 22, y + 36, 4, 8))

    def get_mask(self):
        return pygame.Rect(self.x + 4, self.y, self.width - 4, self.height)