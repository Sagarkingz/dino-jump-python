import asyncio
import random
import sys
import time
import pygame
from src.cloud import Cloud, GroundDetail
from src.dino import Dino
from src.obstacle import Obstacle

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 850, 360
GROUND_Y = 240
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrome Dino 2.0 - Next-Gen Runner")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("Courier", 20, bold=True)
GAME_OVER_FONT = pygame.font.SysFont("Courier", 28, bold=True)

# Dino 2.0 Color Palettes (Switches every 1000 points)
THEMES = [
    {"name": "CLASSIC 2.0", "bg": (247, 247, 247), "fg": (60, 60, 60), "cloud": (210, 210, 210)},
    {"name": "CYBER NIGHT", "bg": (24, 26, 32), "fg": (0, 255, 180), "cloud": (60, 75, 90)},
    {"name": "DESERT DUNE", "bg": (252, 246, 229), "fg": (140, 75, 30), "cloud": (225, 205, 175)},
    {"name": "JUNGLE ACID", "bg": (230, 248, 235), "fg": (20, 110, 45), "cloud": (180, 220, 190)},
    {"name": "ARCTIC FROST", "bg": (235, 245, 255), "fg": (30, 90, 160), "cloud": (195, 215, 235)}
]


async def main():
    dino = Dino(x=60, y=GROUND_Y)
    obstacles = []
    clouds = [Cloud(WIDTH), Cloud(WIDTH + 280), Cloud(WIDTH + 540)]
    ground_specks = [GroundDetail(random.randint(0, WIDTH), GROUND_Y) for _ in range(15)]

    score = 0.0
    high_score = 0

    # Authentic smooth acceleration curve
    SPEED_START = 270.0
    SPEED_MAX = 720.0
    ACCELERATION = 3.5

    current_speed = SPEED_START
    spawn_timer = 0.0
    game_over = False
    last_time = time.time()

    running = True
    while running:
        now = time.time()
        dt = now - last_time
        last_time = now
        if dt > 0.05:
            dt = 0.016

        theme = THEMES[(int(score) // 1000) % len(THEMES)]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if game_over:
                        dino = Dino(x=60, y=GROUND_Y)
                        obstacles = []
                        score = 0.0
                        current_speed = SPEED_START
                        game_over = False
                    else:
                        dino.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    dino = Dino(x=60, y=GROUND_Y)
                    obstacles = []
                    score = 0.0
                    current_speed = SPEED_START
                    game_over = False
                else:
                    dino.jump()

        if not game_over:
            dino.update()

            # Clouds & Ground details
            for cloud in clouds:
                cloud.update(dt)
                if cloud.x + 60 < 0:
                    clouds.remove(cloud)
                    clouds.append(Cloud(WIDTH))

            for speck in ground_specks:
                speck.update(current_speed, dt)
                if speck.x < -15:
                    ground_specks.remove(speck)
                    ground_specks.append(GroundDetail(WIDTH, GROUND_Y))

            # Gradual speed progression
            if current_speed < SPEED_MAX:
                current_speed += ACCELERATION * dt

            # Obstacle spawner
            spawn_timer += dt
            spawn_interval = 1.35 * (SPEED_START / current_speed) + random.uniform(0.1, 0.75)
            if spawn_timer >= spawn_interval:
                obstacles.append(Obstacle(WIDTH, GROUND_Y))
                spawn_timer = 0.0

            # Obstacles update & collision
            for obs in list(obstacles):
                obs.update(current_speed * dt)
                if obs.x + obs.width < -10:
                    obstacles.remove(obs)

                if dino.get_mask().colliderect(obs.get_mask()):
                    game_over = True
                    if int(score) > high_score:
                        high_score = int(score)

            score += dt * (current_speed / 28.0)

        # --- Render ---
        screen.fill(theme["bg"])

        # Clouds
        for cloud in clouds:
            cloud.draw(screen, theme["cloud"])

        # Ground line and terrain specks
        pygame.draw.line(screen, theme["fg"], (0, GROUND_Y + 48), (WIDTH, GROUND_Y + 48), 2)
        for speck in ground_specks:
            speck.draw(screen, theme["cloud"])

        # Entities
        dino.draw(screen, theme["fg"], theme["bg"])
        for obs in obstacles:
            obs.draw(screen, theme["fg"])

        # HUD Score
        score_str = f"HI {high_score:05d}  {int(score):05d}"
        score_surf = FONT.render(score_str, True, theme["fg"])
        screen.blit(score_surf, (WIDTH - 240, 25))

        if game_over:
            go_msg = GAME_OVER_FONT.render("G A M E   O V E R", True, theme["fg"])
            sub_msg = FONT.render("Press SPACE or Tap to Restart", True, theme["fg"])
            screen.blit(go_msg, (WIDTH // 2 - go_msg.get_width() // 2, HEIGHT // 2 - 35))
            screen.blit(sub_msg, (WIDTH // 2 - sub_msg.get_width() // 2, HEIGHT // 2 + 10))

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())