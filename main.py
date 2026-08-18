import asyncio
import random
import sys
import time
import pygame
from src.cloud import Cloud
from src.dino import Dino
from src.obstacle import Obstacle

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 850, 360
GROUND_Y = 240
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrome Dino - 2D Edition")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("Courier", 20, bold=True)
GAME_OVER_FONT = pygame.font.SysFont("Courier", 28, bold=True)

THEMES = [
    {"name": "CLASSIC", "bg": (247, 247, 247), "fg": (83, 83, 83), "cloud": (210, 210, 210)},
    {"name": "NIGHT MODE", "bg": (32, 33, 36), "fg": (230, 230, 230), "cloud": (80, 80, 80)},
    {"name": "DESERT", "bg": (250, 243, 224), "fg": (120, 80, 40), "cloud": (220, 205, 180)},
    {"name": "JUNGLE", "bg": (235, 247, 235), "fg": (35, 95, 45), "cloud": (190, 220, 190)},
    {"name": "ARCTIC", "bg": (235, 245, 255), "fg": (40, 80, 130), "cloud": (190, 210, 230)}
]


async def main():
    dino = Dino(x=60, y=GROUND_Y)
    obstacles = []
    clouds = [Cloud(WIDTH), Cloud(WIDTH + 300)]

    score = 0
    high_score = 0
    
    # Real-World Speed in Pixels Per Second
    SPEED_START = 260.0  # Slow, authentic starting crawl (pixels/sec)
    SPEED_MAX = 750.0
    ACCEL = 4.0          # Pixels/sec gained per second played

    current_speed = SPEED_START
    spawn_timer = 0.0
    game_over = False
    
    last_time = time.time()

    running = True
    while running:
        # Calculate strict elapsed real time (Delta Time)
        now = time.time()
        dt = now - last_time
        last_time = now
        # Clamp dt to prevent massive jumps on tab switches
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
                        score = 0
                        current_speed = SPEED_START
                        game_over = False
                    else:
                        dino.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    dino = Dino(x=60, y=GROUND_Y)
                    obstacles = []
                    score = 0
                    current_speed = SPEED_START
                    game_over = False
                else:
                    dino.jump()

        if not game_over:
            dino.update()

            for cloud in clouds:
                cloud.x -= 80 * dt
                if cloud.x + 60 < 0:
                    clouds.remove(cloud)
                    clouds.append(Cloud(WIDTH))

            # Gradual speed increase
            if current_speed < SPEED_MAX:
                current_speed += ACCEL * dt

            # Obstacle Spawning based on distance/time
            spawn_timer += dt
            spawn_delay = 1.4 * (SPEED_START / current_speed) + random.uniform(0.1, 0.8)
            if spawn_timer >= spawn_delay:
                obstacles.append(Obstacle(WIDTH, GROUND_Y))
                spawn_timer = 0.0

            # Move obstacles with exact pixel velocity
            for obs in list(obstacles):
                obs.x -= current_speed * dt
                if obs.x + obs.width < 0:
                    obstacles.remove(obs)

                if dino.get_mask().colliderect(obs.get_mask()):
                    game_over = True
                    if int(score) > high_score:
                        high_score = int(score)

            # Score increments by real distance covered
            score += dt * (current_speed / 25.0)

        # --- Draw ---
        screen.fill(theme["bg"])

        for cloud in clouds:
            cloud.draw(screen, theme["cloud"])

        pygame.draw.line(screen, theme["fg"], (0, GROUND_Y + 48), (WIDTH, GROUND_Y + 48), 2)

        dino.draw(screen, theme["fg"], theme["bg"])
        for obs in obstacles:
            obs.draw(screen, theme["fg"])

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