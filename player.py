import pygame
from settings import *

class Player:
    def __init__(self):
        # Initial size and position (Upscaled for premium HD rendering)
        self.normal_width = 64
        self.normal_height = 96
        self.duck_height = 48
        
        self.width = self.normal_width
        self.height = self.normal_height
        
        self.x = 80  # Push slightly forward for better visibility
        self.y = HEIGHT - self.height - 20 # 20 px above bottom
        self.color = BLUE
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Physics
        self.vel_y = 0
        self.gravity = 0.65
        self.is_ducking = False
        
        # Load sprite images (Smooth 4-frame cycle)
        self.images_run = [
            load_png("assets/player_run1.png"),
            load_png("assets/player_run2.png"),
            load_png("assets/player_run3.png"),
            load_png("assets/player_run4.png")
        ]
        self.image_jump = load_png("assets/player_jump.png")
        self.images_duck = [
            load_png("assets/player_duck1.png"),
            load_png("assets/player_duck2.png")
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
            self.vel_y = -15
            
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

