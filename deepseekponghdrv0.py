import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 600
HEIGHT = 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60

# Ball dimensions
BALL_SIZE = 8

# Player positions
player_pos = HEIGHT // 2 - PADDLE_HEIGHT // 2
opponent_pos = HEIGHT // 2 - PADDLE_HEIGHT // 2

# Ball position and speed
ball_x = WIDTH // 2 - BALL_SIZE // 2
ball_y = HEIGHT // 2 - BALL_SIZE // 2
ball_speed_x = random.choice([5, -5])
ball_speed_y = random.choice([5, -5])

# Scores
player_score = 0
opponent_score = 0

# Clock for frame rate control
clock = pygame.time.Clock()

# Game loop
running = True
game_over = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddles (player controls the left paddle with arrow keys)
    keys = pygame.key.get_pressed()
    
    # Player movement
    if keys[pygame.K_UP] and player_pos > 0:
        player_pos -= 5
    if keys[pygame.K_DOWN] and player_pos < HEIGHT - PADDLE_HEIGHT:
        player_pos += 5

    # Opponent AI (simple movement to follow the ball)
    opponent_speed = 3
    if opponent_pos + PADDLE_HEIGHT // 2 < ball_y and ball_x > WIDTH // 2:
        opponent_pos += opponent_speed
    if opponent_pos + PADDLE_HEIGHT // 2 > ball_y and ball_x > WIDTH // 2:
        opponent_pos -= opponent_speed

    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with top/bottom walls
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_speed_y *= -1

    # Ball collision with paddles
    if (
        (ball_x <= PADDLE_WIDTH and player_pos <= ball_y <= player_pos + PADDLE_HEIGHT)
        or (
            ball_x >= WIDTH - PADDLE_WIDTH - BALL_SIZE
            and opponent_pos <= ball_y <= opponent_pos + PADDLE_HEIGHT
        )
    ):
        ball_speed_x *= -1

    # Score points
    if ball_x <= 0:
        opponent_score += 1
        ball_x = WIDTH // 2 - BALL_SIZE // 2
        ball_y = HEIGHT // 2 - BALL_SIZE // 2
        ball_speed_x = random.choice([5, -5])
        ball_speed_y = random.choice([5, -5])
    if ball_x >= WIDTH - BALL_SIZE:
        player_score += 1
        ball_x = WIDTH // 2 - BALL_SIZE // 2
        ball_y = HEIGHT // 2 - BALL_SIZE // 2
        ball_speed_x = random.choice([5, -5])
        ball_speed_y = random.choice([5, -5])

    # Clear the screen
    win.fill(BLACK)

    # Draw paddles and ball
    pygame.draw.rect(win, WHITE, (0, player_pos, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(
        win, WHITE, (WIDTH - PADDLE_WIDTH, opponent_pos, PADDLE_WIDTH, PADDLE_HEIGHT)
    )
    pygame.draw.ellipse(win, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    # Draw scores
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"{player_score} - {opponent_score}", True, WHITE)
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    clock.tick(60)

pygame.quit()
