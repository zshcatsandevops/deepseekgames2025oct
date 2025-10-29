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

# Game states
game_over = False

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Middle mouse click (mouse wheel)
                # Restart game
                player_score = 0
                opponent_score = 0
                ball_x = WIDTH // 2 - BALL_SIZE // 2
                ball_y = HEIGHT // 2 - BALL_SIZE // 2
                ball_speed_x = random.choice([5, -5])
                ball_speed_y = random.choice([5, -5])
                game_over = False
            elif event.button == 1:  # Left mouse click
                running = False

    if not game_over:
        # Move paddles (player controls the left paddle with mouse)
        mouse_pos = pygame.mouse.get_pos()[1]
        player_pos = mouse_pos - PADDLE_HEIGHT // 2
        
        # Keep player paddle within screen bounds
        if player_pos < 0:
            player_pos = 0
        elif player_pos > HEIGHT - PADDLE_HEIGHT:
            player_pos = HEIGHT - PADDLE_HEIGHT

        # Opponent AI (simple movement to follow the ball)
        opponent_speed = 3
        if ball_x > WIDTH // 2:
            if opponent_pos + PADDLE_HEIGHT // 2 < ball_y:
                opponent_pos += opponent_speed
            elif opponent_pos + PADDLE_HEIGHT // 2 > ball_y:
                opponent_pos -= opponent_speed

        # Keep opponent paddle within screen bounds
        if opponent_pos < 0:
            opponent_pos = 0
        elif opponent_pos > HEIGHT - PADDLE_HEIGHT:
            opponent_pos = HEIGHT - PADDLE_HEIGHT

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

        # Check if game over conditions are met
        if player_score == 5 or opponent_score == 5:
            game_over = True

    # Clear the screen
    win.fill(BLACK)

    if not game_over:
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

    if game_over:
        # Draw game over message
        game_over_font = pygame.font.Font(None, 74)
        game_over_text = game_over_font.render("GAME OVER", True, WHITE)
        win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        
        # Draw restart/quit instructions
        instructions_font = pygame.font.Font(None, 36)
        instructions_text_left = instructions_font.render("LEFT CLICK to QUIT", True, WHITE)
        win.blit(instructions_text_left, (WIDTH // 4 - instructions_text_left.get_width() // 2, HEIGHT // 2))
        
        instructions_text_right = instructions_font.render("Middle Click to RESTART", True, WHITE)
        win.blit(instructions_text_right, (3 * WIDTH // 4 - instructions_text_right.get_width() // 2, HEIGHT // 2))

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    clock.tick(60)

pygame.quit()
