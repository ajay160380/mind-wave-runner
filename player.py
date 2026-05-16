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

    def update(self):
        # Update rect position based on x and y
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
