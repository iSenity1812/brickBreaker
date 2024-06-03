import sys
import os
try:
    import pygame
    from pygame.locals import *
except ModuleNotFoundError:
    os.system('pip install pygame')

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Paddle
paddle_width = 100
paddle_height = 10
paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - 50, paddle_width, paddle_height)
paddle_speed = 10

# Ball
ball_radius = 10
ball_speed = [5, -5]
ball = pygame.Rect(screen_width // 2, screen_height // 2, ball_radius * 2, ball_radius * 2)

# Bricks
brick_rows = 5
brick_cols = 10
brick_width = 75
brick_height = 20
brick_padding = 10
bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        brick = pygame.Rect(col * (brick_width + brick_padding) + 35,
                            row * (brick_height + brick_padding) + 50,
                            brick_width, brick_height)
        bricks.append(brick)

# Main game loop
clock = pygame.time.Clock()
running = True
game_over = False
you_win = False

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    if not game_over and not you_win:
        # Move paddle
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if keys[K_RIGHT] and paddle.right < screen_width:
            paddle.right += paddle_speed

        # Move ball
        ball.left += ball_speed[0]
        ball.top += ball_speed[1]

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= screen_width:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]

        # Ball collision with paddle
        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]

        # Ball collision with bricks
        for brick in bricks[:]:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1]
                bricks.remove(brick)

        # Check if ball falls off the screen
        if ball.bottom >= screen_height:
            game_over = True

        # Check if all bricks are destroyed
        if len(bricks) == 0:
            you_win = True

        # Clear screen
        screen.fill(BLACK)

        # Draw paddle
        pygame.draw.rect(screen, BLUE, paddle)

        # Draw ball
        pygame.draw.ellipse(screen, WHITE, ball)

        # Draw bricks
        for brick in bricks:
            pygame.draw.rect(screen, GREEN, brick)

        # Update display
        pygame.display.flip()

        # Frame rate
        clock.tick(60)

    else:
        # Game over or You win screen
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 48)
        if game_over:
            text = font.render("Game Over", True, WHITE)
        elif you_win:
            text = font.render("You Win!", True, WHITE)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

        pygame.display.flip()

        # Wait for player input
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_RETURN:
                    # Restart the game
                    game_over = False
                    you_win = False
                    ball.left = screen_width // 2
                    ball.top = screen_height // 2
                    paddle.left = screen_width // 2 - paddle_width // 2
                    bricks = [pygame.Rect(col * (brick_width + brick_padding) + 35,
                                          row * (brick_height + brick_padding) + 50,
                                        brick_width, brick_height)
        for row in range(brick_rows) for col in range(brick_cols)]

pygame.quit()
