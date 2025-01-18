import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game settings
FPS = 60
GRAVITY = 0.25
FLAP_STRENGTH = -6
PIPE_SPEED = 4
PIPE_GAP = 150

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Bird class
class Bird:
    def _init_(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.width = 30
        self.height = 30

    def draw(self):
        pygame.draw.ellipse(screen, RED, (self.x, self.y, self.width, self.height))

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def flap(self):
        self.velocity = FLAP_STRENGTH

# Pipe class
class Pipe:
    def _init_(self, x):
        self.x = x
        self.top_height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.bottom_height = SCREEN_HEIGHT - self.top_height - PIPE_GAP
        self.width = 50

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, GREEN, (self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height))

    def update(self):
        self.x -= PIPE_SPEED

# Check collision
def check_collision(bird, pipes):
    for pipe in pipes:
        if (bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe.width):
            if bird.y < pipe.top_height or bird.y + bird.height > SCREEN_HEIGHT - pipe.bottom_height:
                return True
    if bird.y < 0 or bird.y + bird.height > SCREEN_HEIGHT:
        return True
    return False

# Main game function
def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * 200) for i in range(3)]
    score = 0
    running = True
    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Update bird
        bird.update()

        # Update pipes
        for pipe in pipes:
            pipe.update()
            if pipe.x + pipe.width < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(SCREEN_WIDTH))
                score += 1

        # Check for collision
        if check_collision(bird, pipes):
            running = False

        # Draw everything
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

# Run the game
if __name__ == "_main_":
    main()
#End