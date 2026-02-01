import pygame
import random

# -------------------- INIT --------------------
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 50)
big_font = pygame.font.SysFont("Arial", 200)
smaller = pygame.font.SysFont("Arial", 100)

# -------------------- ASSETS --------------------
logo = pygame.image.load("Python.svg.png").convert_alpha()
player_image = pygame.transform.scale(
    pygame.image.load("flappybird.png").convert_alpha(), (304, 198)
)

# -------------------- PLAYER --------------------
player_rect = player_image.get_rect()
player_rect.x = 150
player_rect.y = HEIGHT // 2

# Smaller hitbox
player_hitbox = player_rect.inflate(-75, -75)

gravity = 1
jump_strength = -15
velocity = 0

# -------------------- WALLS --------------------
WALL_WIDTH = 80
WALL_GAP = player_hitbox.height + 300
WALL_SPEED = 6
WALL_SPAWN_TIME = 180

walls = []
wall_timer = 0
previous_gap = HEIGHT // 2


# ---------------- SOUND -----------------------
SOUND_GAME_OVER = pygame.mixer.Sound("mixkit-dramatic-metal-explosion-impact-1687.wav")
SOUND_SCORE = pygame.mixer.Sound("retro-game-coin-pickup-jam-fx-1-00-03.wav")

def create_wall():
    global previous_gap

    # Smooth gap movement
    gap_y = previous_gap + random.randint(-150, 150)
    gap_y = max(200, min(HEIGHT - 200, gap_y))
    previous_gap = gap_y

    HITBOX_MARGIN = 10

    top_height = max(50, gap_y - WALL_GAP // 2 - HITBOX_MARGIN)
    bottom_y = gap_y + WALL_GAP // 2 + HITBOX_MARGIN

    top = pygame.Rect(
        WIDTH + HITBOX_MARGIN,
        0,
        WALL_WIDTH - HITBOX_MARGIN * 2,
        top_height
    )

    bottom = pygame.Rect(
        WIDTH + HITBOX_MARGIN,
        bottom_y,
        WALL_WIDTH - HITBOX_MARGIN * 2,
        HEIGHT - bottom_y
    )

    return {"top": top, "bottom": bottom, "passed": False}

# -------------------- GAME STATE --------------------
score = 0
running = True
game_over = False
show_logo = True
frame = 0

# -------------------- MAIN LOOP --------------------
while running:
    clock.tick(60)
    frame += 1

    # ---------- EVENTS ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE and not game_over and not show_logo:
                velocity = jump_strength

            if event.key == pygame.K_r and game_over:
                walls.clear()
                wall_timer = 0
                previous_gap = HEIGHT // 2
                player_rect.y = HEIGHT // 2
                velocity = 0
                score = 0
                game_over = False
                frame = 0
                show_logo = True

    screen.fill((0, 0, 0))

    # ---------- INTRO ----------
    if show_logo:
        screen.blit(
            logo,
            (WIDTH // 2 - logo.get_width() // 2,
             HEIGHT // 2 - logo.get_height() // 2)
        )
        if frame > 180:
            show_logo = False
        pygame.display.flip()
        continue

    # ---------- GAME ----------
    if not game_over:
        velocity += gravity
        player_rect.y += velocity
        player_hitbox.center = player_rect.center

        wall_timer += 1
        if wall_timer >= WALL_SPAWN_TIME:
            walls.append(create_wall())
            wall_timer = 0

        for wall in walls:
            wall["top"].x -= WALL_SPEED
            wall["bottom"].x -= WALL_SPEED

            if player_hitbox.colliderect(wall["top"]) or player_hitbox.colliderect(wall["bottom"]):
                game_over = True
                SOUND_GAME_OVER.play()

            if not wall["passed"] and wall["top"].right < player_hitbox.left:
                score += 1
                SOUND_SCORE.play()
                wall["passed"] = True

        walls = [w for w in walls if w["top"].right > 0]

        if player_rect.top <= 0 or player_rect.bottom >= HEIGHT:
            game_over = True
            SOUND_GAME_OVER.play()

        for wall in walls:
            pygame.draw.rect(screen, (0, 255, 0), wall["top"])
            pygame.draw.rect(screen, (0, 255, 0), wall["bottom"])

        screen.blit(player_image, player_rect)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

    # ---------- GAME OVER ----------
    else:
        text = big_font.render("GAME OVER", True, (255, 255, 255))
        restart = font.render("Press R to Restart", True, (200, 200, 200))
        score_text = smaller.render(f"Score: {score}", True, (255, 255, 255))

        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 200))
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 50))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 150))

    pygame.display.flip()

pygame.quit()
