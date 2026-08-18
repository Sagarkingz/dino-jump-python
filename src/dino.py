import pygame

class Dino:
    def __init__(self, x=60, y=260):
        self.x = x
        self.ground_y = y
        self.y = self.ground_y
        self.width = 48
        self.height = 50
        self.vy = 0
        self.jump_force = -12.2
        self.gravity = 0.60
        self.is_grounded = True
        self.leg_step = 0.0

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
            self.leg_step = (self.leg_step + 0.22) % 2.0

    def draw(self, screen, color=(75, 75, 75), bg_color=(247, 247, 247)):
        x, y = int(self.x), int(self.y)

        # 1. Back Dorsal Spikes (Dino 2.0 Feature)
        pygame.draw.polygon(screen, color, [(x + 8, y + 10), (x + 4, y + 4), (x + 12, y + 10)])
        pygame.draw.polygon(screen, color, [(x + 16, y + 8), (x + 14, y + 1), (x + 20, y + 8)])
        pygame.draw.polygon(screen, color, [(x + 24, y + 6), (x + 23, y - 1), (x + 28, y + 6)])

        # 2. Tail with Fin
        pygame.draw.rect(screen, color, (x, y + 22, 8, 8))
        pygame.draw.rect(screen, color, (x + 4, y + 16, 8, 16))

        # 3. Main Torso
        pygame.draw.rect(screen, color, (x + 10, y + 12, 24, 26))

        # 4. Sculpted Head & Snout
        pygame.draw.rect(screen, color, (x + 22, y, 22, 14))
        pygame.draw.rect(screen, color, (x + 40, y + 2, 10, 12))

        # 5. Cyber Visor / Glowing Eye & Sharp Mouth Cutout
        pygame.draw.rect(screen, bg_color, (x + 28, y + 3, 7, 4))   # Eye visor slit
        pygame.draw.rect(screen, bg_color, (x + 36, y + 9, 14, 4))   # Open jaw line

        # 6. Forearm with Claws
        pygame.draw.rect(screen, color, (x + 32, y + 20, 8, 3))
        pygame.draw.rect(screen, color, (x + 38, y + 23, 2, 4))

        # 7. Articulated Running Legs
        if self.is_grounded:
            if self.leg_step < 1.0:
                # Left Leg forward, Right Leg trailing
                pygame.draw.rect(screen, color, (x + 16, y + 38, 5, 12))
                pygame.draw.rect(screen, color, (x + 16, y + 48, 8, 3))
                pygame.draw.rect(screen, color, (x + 27, y + 38, 5, 6))
                pygame.draw.rect(screen, color, (x + 29, y + 44, 5, 4))
            else:
                # Right Leg forward, Left Leg trailing
                pygame.draw.rect(screen, color, (x + 16, y + 38, 5, 6))
                pygame.draw.rect(screen, color, (x + 13, y + 44, 5, 4))
                pygame.draw.rect(screen, color, (x + 27, y + 38, 5, 12))
                pygame.draw.rect(screen, color, (x + 27, y + 48, 8, 3))
        else:
            # Jumping stance
            pygame.draw.rect(screen, color, (x + 16, y + 38, 5, 8))
            pygame.draw.rect(screen, color, (x + 25, y + 38, 5, 8))

    def get_mask(self):
        return pygame.Rect(self.x + 6, self.y + 2, self.width - 8, self.height - 2)