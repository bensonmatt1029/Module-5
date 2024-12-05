import pygame
import sys

# Initialize PyGame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600  # Width and height of the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
pygame.display.set_caption("Pong Game")  # Set the title of the window

# Colors
WHITE = (255, 255, 255)  # White color for paddles, ball, and text
BLACK = (0, 0, 0)        # Black color for the background

# Game variables
paddle_width, paddle_height = 10, 100  # Dimensions of the paddles
ball_size = 15                         # Diameter of the ball
ball_speed_x, ball_speed_y = 5, 5      # Initial speed of the ball (x and y directions)
paddle_speed = 7                       # Speed at which paddles move

# Ball and paddles positions
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
# Ball starts at the center of the screen
paddle1 = pygame.Rect(10, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
# Left paddle starts near the left edge
paddle2 = pygame.Rect(WIDTH - 10 - paddle_width, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
# Right paddle starts near the right edge

# Scores
score1, score2 = 0, 0  # Initialize scores for both players

# Fonts
font = pygame.font.Font(None, 74)       # Font for the scores
small_font = pygame.font.Font(None, 36)  # Optional smaller font (not currently used)

# Clock
clock = pygame.time.Clock()  # Clock to control the game's frame rate

# Sounds
pong_sound = pygame.mixer.Sound("pong_hit.wav")  # Sound for ball hitting the paddle
score_sound = pygame.mixer.Sound("score.wav")    # Sound for scoring a point

# Function to draw all game elements
def draw():
    screen.fill(BLACK)  # Fill the background with black
    pygame.draw.rect(screen, WHITE, paddle1)  # Draw the left paddle
    pygame.draw.rect(screen, WHITE, paddle2)  # Draw the right paddle
    pygame.draw.ellipse(screen, WHITE, ball)  # Draw the ball
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    # Draw a center line for reference
    
    # Draw scores
    score_text1 = font.render(str(score1), True, WHITE)  # Render player 1's score
    score_text2 = font.render(str(score2), True, WHITE)  # Render player 2's score
    screen.blit(score_text1, (WIDTH // 4 - score_text1.get_width() // 2, 20))  # Display player 1's score
    screen.blit(score_text2, (3 * WIDTH // 4 - score_text2.get_width() // 2, 20))  # Display player 2's score

# Function to handle ball movement and collisions
def handle_ball_movement():
    global ball_speed_x, ball_speed_y, score1, score2

    ball.x += ball_speed_x  # Move ball horizontally
    ball.y += ball_speed_y  # Move ball vertically

    # Ball collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1  # Reverse vertical direction
    
    # Ball collision with paddles
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed_x *= -1  # Reverse horizontal direction
        pong_sound.play()  # Play paddle hit sound
    
    # Ball goes out of bounds (left or right side)
    if ball.left <= 0:
        score2 += 1  # Player 2 scores a point
        score_sound.play()  # Play scoring sound
        reset_ball()  # Reset ball to the center
    elif ball.right >= WIDTH:
        score1 += 1  # Player 1 scores a point
        score_sound.play()  # Play scoring sound
        reset_ball()  # Reset ball to the center

# Function to handle paddle movement
def handle_paddle_movement():
    keys = pygame.key.get_pressed()  # Get the state of all keys

    # Paddle 1 movement (W/S keys)
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.y -= paddle_speed  # Move paddle 1 up
    if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
        paddle1.y += paddle_speed  # Move paddle 1 down

    # Paddle 2 movement (Up/Down arrow keys)
    if keys[pygame.K_UP] and paddle2.top > 0:
        paddle2.y -= paddle_speed  # Move paddle 2 up
    if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
        paddle2.y += paddle_speed  # Move paddle 2 down

# Function to reset ball to the center of the screen
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)  # Place the ball at the center
    ball_speed_x *= -1  # Reverse ball's horizontal direction to alternate serve

# Main game loop
def main():
    global running
    running = True  # Game is running
    while running:
        # Handle events (e.g., quit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the game loop
        
        # Update game mechanics
        handle_paddle_movement()  # Update paddle positions
        handle_ball_movement()  # Update ball position and check collisions
        
        # Draw everything on the screen
        draw()

        # Update the display
        pygame.display.flip()
        
        # Limit the frame rate to 60 FPS
        clock.tick(60)

    pygame.quit()  # Quit PyGame
    sys.exit()  # Exit the program

# Run the game
if __name__ == "__main__":
    main()