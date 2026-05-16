import pygame
from settings import *

class Player:
    def __init__(self):
        # Initial size and position
        self.width = 40
        self.height = 60
        self.x = 50
        self.y = HEIGHT - self.height - 20 # 20 px above bottom
        self.color = BLUE
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Physics
        self.vel_y = 0
        self.gravity = 0.6
        self.ground_y = HEIGHT - self.height - 20

    def update(self):
        # Apply gravity
        self.vel_y += self.gravity
        self.y += self.vel_y
        
        # Ground collision
        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.vel_y = 0

        # Update rect position based on x and y
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
