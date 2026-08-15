import random
import pygame

class ParallaxBackground:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.distant_offset = 0
        self.midground_offset = 0
        self.particles = []

    def update(self, speed, particle_type):
        self.distant_offset = (self.distant_offset + speed * 0.12) % self.width
        self.midground_offset = (self.midground_offset + speed * 0.45) % self.width

        if len(self.particles) < 35:
            self.particles.append({
                "x": self.width + random.randint(0, 100),
                "y": random.randint(20, self.height - 120),
                "size": random.uniform(1.5, 4.5),
                "speed": random.uniform(1.2, 3.2),
                "alpha": random.randint(80, 200)
            })

        for p in list(self.particles):
            p["x"] -= p["speed"]
            if p["x"] < -10:
                self.particles.remove(p)

    def draw(self, screen, theme):
        w, h = self.width, self.height

        # 1. Base Sky Atmosphere Gradient
        for y in range(0, h, 8):
            ratio = y / h
            r = int(theme["sky_top"][0] * (1 - ratio) + theme["sky_bot"][0] * ratio)
            g = int(theme["sky_top"][1] * (1 - ratio) + theme["sky_bot"][1] * ratio)
            b = int(theme["sky_top"][2] * (1 - ratio) + theme["sky_bot"][2] * ratio)
            pygame.draw.rect(screen, (r, g, b), (0, y, w, 8))

        # 2. Celestial Body / Sun (Volumetric Glow)
        sun_surf = pygame.Surface((180, 180), pygame.SRCALPHA)
        pygame.draw.circle(sun_surf, (*theme["sun_glow"], 35), (90, 90), 85)
        pygame.draw.circle(sun_surf, (*theme["sun_glow"], 90), (90, 90), 55)
        pygame.draw.circle(sun_surf, theme["sun_core"], (90, 90), 32)
        screen.blit(sun_surf, (w - 240, 30))

        # 3. Distant Parallax Mountains / Structures (Slow Plane)
        d_pts = [
            (0 - self.distant_offset, h - 140),
            (w * 0.25 - self.distant_offset, h - 260),
            (w * 0.55 - self.distant_offset, h - 180),
            (w * 0.85 - self.distant_offset, h - 300),
            (w * 1.25 - self.distant_offset, h - 140),
            (w * 1.55 - self.distant_offset, h - 280),
            (w * 2.0 - self.distant_offset, h - 140),
            (w * 2.0, h), (0, h)
        ]
        pygame.draw.polygon(screen, theme["distant_mountains"], d_pts)

        # 4. Midground Rolling Ridges (Medium Plane)
        m_pts = [
            (0 - self.midground_offset, h - 90),
            (w * 0.3 - self.midground_offset, h - 170),
            (w * 0.7 - self.midground_offset, h - 120),
            (w * 1.1 - self.midground_offset, h - 180),
            (w * 1.6 - self.midground_offset, h - 100),
            (w * 2.0 - self.midground_offset, h - 170),
            (w * 2.0, h), (0, h)
        ]
        pygame.draw.polygon(screen, theme["mid_ridge"], m_pts)

        # 5. 3D Environmental Particles (Dust/Ash/Snow/Stars)
        for p in self.particles:
            part_surf = pygame.Surface((int(p["size"] * 2), int(p["size"] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(part_surf, (*theme["particle_color"], p["alpha"]), (int(p["size"]), int(p["size"])), int(p["size"]))
            screen.blit(part_surf, (int(p["x"]), int(p["y"])))