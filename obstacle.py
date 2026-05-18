import pygame
import random
from settings import *

class Obstacle:
    """A single obstacle that moves from right to left across the screen."""
    
    def __init__(self):
        # Choose a random type of obstacle
        self.type = random.choice(['small', 'tall', 'wide'])
        
        if self.type == 'small':
            self.image = pygame.image.load("assets/obstacle_small.png").convert_alpha()
            self.width = 25
            self.height = 40
            self.y = HEIGHT - self.height - 20  # Grounded
        elif self.type == 'tall':
            self.image = pygame.image.load("assets/obstacle_tall.png").convert_alpha()
            self.width = 30
            self.height = 70
            self.y = HEIGHT - self.height - 20  # Grounded
        elif self.type == 'wide':
            self.image = pygame.image.load("assets/obstacle_wide.png").convert_alpha()
            self.width = 45
            self.height = 45
            # Floating drone: duck under it!
            # Standing player y = HEIGHT - 60 - 20 = HEIGHT - 80 (top at HEIGHT - 80)
            # Ducking player y = HEIGHT - 30 - 20 = HEIGHT - 50 (top at HEIGHT - 50)
            # Drone y = HEIGHT - 100, height = 45, so bottom is HEIGHT - 55.
            # Standing player (top HEIGHT-80) collides; ducking player (top HEIGHT-50) passes under.
            self.y = HEIGHT - 100
        
        # Start off-screen to the right
        self.x = WIDTH + random.randint(0, 100)
        
        self.speed = 5  # Horizontal speed (pixels per frame)
        
        # Collision rect
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        """Move the obstacle to the left each frame."""
        self.x -= self.speed
        self.rect.x = self.x
    
    def is_off_screen(self):
        """Check if obstacle has moved past the left edge."""
        return self.x + self.width < 0
    
    def draw(self, screen):
        """Render the obstacle using its sprite."""
        screen.blit(self.image, self.rect)
