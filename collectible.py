import pygame
import random
import math
from settings import *

class Collectible:
    def __init__(self, speed=5):
        # Load the newly created data core asset
        self.image = load_png("assets/data_core.png")
        self.width = 25
        self.height = 25
        
        # Spawn off-screen to the right
        self.x = WIDTH + random.randint(50, 250)
        
        # Floating positions:
        # - 'high': Player must jump to grab it
        # - 'low': Player can collect while sliding/ducking
        # - 'mid': Ground-level collection
        self.type = random.choice(['high', 'low', 'mid'])
        if self.type == 'high':
            self.y = HEIGHT - 140
        elif self.type == 'low':
            self.y = HEIGHT - 85
        else:
            self.y = HEIGHT - 45
            
        self.base_y = self.y
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collected = False
        
    def update(self):
        """Move left and bob up/down using a dynamic sine wave."""
        self.x -= self.speed
        
        # Smooth bobbing animation based on horizontal position
        self.y = self.base_y + int(math.sin(self.x * 0.05) * 5)
        
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self, screen):
        """Render the neon diamond core."""
        if not self.collected:
            screen.blit(self.image, self.rect)
            
    def is_off_screen(self):
        """Check if it has moved past the left boundary."""
        return self.x + self.width < 0
