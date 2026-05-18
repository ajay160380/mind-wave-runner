import pygame
import random
from settings import *

class Obstacle:
    """A single obstacle that moves from right to left across the screen."""
    
    def __init__(self, speed=5):
        # Choose a random type of obstacle
        self.type = random.choice(['small', 'tall', 'wide'])
        
        if self.type == 'small':
            self.image = load_png("assets/obstacle_small.png")
            self.width = 40
            self.height = 60
            self.y = HEIGHT - self.height - 20  # Grounded
        elif self.type == 'tall':
            self.image = load_png("assets/obstacle_tall.png")
            self.width = 45
            self.height = 100
            self.y = HEIGHT - self.height - 20  # Grounded
        elif self.type == 'wide':
            self.image = load_png("assets/obstacle_wide.png")
            self.width = 60
            self.height = 60
            # Floating drone: duck under it!
            # Standing player y = HEIGHT - 96 - 20 = HEIGHT - 116 (top at HEIGHT - 116)
            # Ducking player y = HEIGHT - 48 - 20 = HEIGHT - 68 (top at HEIGHT - 68)
            # Drone y = HEIGHT - 130, height = 60, so bottom is HEIGHT - 70.
            # Standing player (top HEIGHT-116) collides; ducking player (top HEIGHT-68) passes under.
            self.y = HEIGHT - 130
        
        # Start off-screen to the right
        self.x = WIDTH + random.randint(0, 100)
        
        self.speed = speed  # Horizontal speed (pixels per frame)
        
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
