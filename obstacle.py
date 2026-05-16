import pygame
import random
from settings import *

class Obstacle:
    """A single obstacle that moves from right to left across the screen."""
    
    def __init__(self):
        # Random size for variety
        self.width = random.randint(20, 40)
        self.height = random.randint(30, 70)
        
        # Start off-screen to the right
        self.x = WIDTH + random.randint(0, 100)
        self.y = HEIGHT - self.height - 20  # Same ground level as player
        
        self.speed = 5  # Horizontal speed (pixels per frame)
        self.color = RED
        
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
        """Render the obstacle as a red rectangle."""
        pygame.draw.rect(screen, self.color, self.rect)
