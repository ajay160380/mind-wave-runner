import pygame
from settings import *

class Player:
    def __init__(self):
        # Initial size and position
        self.normal_width = 40
        self.normal_height = 60
        self.duck_height = 30
        
        self.width = self.normal_width
        self.height = self.normal_height
        
        self.x = 50
        self.y = HEIGHT - self.height - 20 # 20 px above bottom
        self.color = BLUE
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Physics
        self.vel_y = 0
        self.gravity = 0.6
        self.is_ducking = False
        
        # Load sprite images
        self.images_run = [
            pygame.image.load("assets/player_run1.png").convert_alpha(),
            pygame.image.load("assets/player_run2.png").convert_alpha()
        ]
        self.image_jump = pygame.image.load("assets/player_jump.png").convert_alpha()
        self.images_duck = [
            pygame.image.load("assets/player_duck1.png").convert_alpha(),
            pygame.image.load("assets/player_duck2.png").convert_alpha()
        ]
        
        self.animation_index = 0.0
        self.image = self.images_run[0]

    @property
    def ground_y(self):
        return HEIGHT - self.height - 20

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
        self.rect.width = self.width
        self.rect.height = self.height
        
        # Increment animation index
        self.animation_index += 0.15
        
        # Determine which image to show based on state
        if self.y < self.ground_y:
            self.image = self.image_jump
        elif self.is_ducking:
            self.image = self.images_duck[int(self.animation_index) % len(self.images_duck)]
        else:
            self.image = self.images_run[int(self.animation_index) % len(self.images_run)]

    def jump(self):
        # Only jump if on the ground and not ducking
        if self.y >= self.ground_y and not self.is_ducking:
            self.vel_y = -12
            
    def duck(self):
        if not self.is_ducking:
            self.is_ducking = True
            self.height = self.duck_height
            # Immediately snap y to new ground so we don't float
            if self.y >= HEIGHT - self.normal_height - 20:
                self.y = self.ground_y
            
    def unduck(self):
        if self.is_ducking:
            self.is_ducking = False
            self.height = self.normal_height
            # Move player up so they don't get stuck in the ground
            self.y -= (self.normal_height - self.duck_height)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

