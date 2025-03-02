import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Enhanced Snake Game")

# Define colors
black = (0, 0, 0)  # Background
white = (255, 255, 255)  # Text

# Grid settings
grid_size = 20
cell_size = width // grid_size

# Font for text
font = pygame.font.Font(None, 36)

# Load and scale images
original_head = pygame.image.load('snake_head.png').convert_alpha()
original_head = pygame.transform.scale(original_head, (cell_size, cell_size))
body_img = pygame.image.load('snake_body.png').convert_alpha()
body_img = pygame.transform.scale(body_img, (cell_size, cell_size))
food_img = pygame.image.load('food.png').convert_alpha()
food_img = pygame.transform.scale(food_img, (cell_size, cell_size))

# Pre-rotate and cache head images for each direction
head_images = {
    'RIGHT': original_head,  # No rotation
    'DOWN': pygame.transform.rotate(original_head, 90),  # 90° clockwise
    'LEFT': pygame.transform.rotate(original_head, 180),  # 180°
    'UP': pygame.transform.rotate(original_head, 270)  # 270° clockwise
}


def draw_snake(snake, direction):
    """Draw the snake with a pre-rotated head and body images."""
    # Draw the head using the pre-rotated image
    head_x, head_y = snake[0]
    head_img = head_images[direction]
    screen.blit(head_img, (head_x * cell_size, head_y * cell_size))

    # Draw body segments
    for segment in snake[1:]:
        screen.blit(body_img, (segment[0] * cell_size, segment[1] * cell_size))


def draw_food(food):
    """Draw the food using an image."""
    screen.blit(food_img, (food[0] * cell_size, food[1] * cell_size))


def draw_score(score):
    """Display the current score."""
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))


def draw_pause():
    """Display a pause message when the game is paused."""
    pause_text = font.render("Paused", True, white)
    screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2,
                             height // 2 - pause_text.get_height() // 2))


def reset_game():
    """Reset the game to its initial state."""
    global snake, direction, food, score, paused
    snake = [(0, 0)]  # Start at top-left
    direction = 'RIGHT'
    food = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
    score = 0
    paused = False


def game_over_screen():
    """Show the game over screen with restart/quit options."""
    screen.fill(black)
    game_over_text = font.render("Game Over!", True, white)
    score_text = font.render(f"Final Score: {score}", True, white)
    instruction_text = font.render("Press R to Restart or Q to Quit", True, white)
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))
    screen.blit(instruction_text, (width // 2 - instruction_text.get_width() // 2, height // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()


# Initial game state
reset_game()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused  # Toggle pause state
            elif not paused:  # Only handle direction keys when not paused
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

    if not paused:
        # Move the snake
        head_x, head_y = snake[0]
        if direction == 'UP':
            new_head = (head_x, (head_y - 1) % grid_size)
        elif direction == 'DOWN':
            new_head = (head_x, (head_y + 1) % grid_size)
        elif direction == 'LEFT':
            new_head = ((head_x - 1) % grid_size, head_y)
        elif direction == 'RIGHT':
            new_head = ((head_x + 1) % grid_size, head_y)
        snake.insert(0, new_head)

        # Check if snake eats food
        if snake[0] == food:
            score += 1
            while True:
                food = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
                if food not in snake:
                    break
        else:
            snake.pop()

        # Check for collision with self
        if snake[0] in snake[1:]:
            game_over_screen()

    # Draw everything
    screen.fill(black)  # Clear screen with black background
    draw_snake(snake, direction)
    draw_food(food)
    draw_score(score)
    if paused:
        draw_pause()  # Overlay pause message when paused

    # Update display
    pygame.display.flip()

    # Control game speed (increases with score, capped at 30 FPS)
    speed = min(10 + score // 5, 30)
    clock.tick(speed)

# Clean up
pygame.quit()