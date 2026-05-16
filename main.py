import pygame
import sys
import random
from settings import *
from player import Player
from obstacle import Obstacle

def main():
    # Initialize Pygame
    pygame.init()
    pygame.font.init()
    
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Set up the clock
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 32, bold=True)
    
    # Initialize game objects
    player = Player()
    obstacles = []
    spawn_timer = 0
    SPAWN_INTERVAL = random.randint(60, 120)  # Frames between spawns
    score = 0
    
    # Main game loop
    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
        
        # 2. Update Game State
        player.update()
        score += 1
        
        # Spawn obstacles at random intervals
        spawn_timer += 1
        if spawn_timer >= SPAWN_INTERVAL:
            obstacles.append(Obstacle())
            spawn_timer = 0
            SPAWN_INTERVAL = random.randint(60, 120)
        
        # Update all obstacles, check collision, and remove off-screen ones
        for obs in obstacles[:]:
            obs.update()
            
            # AABB Collision Detection
            if player.rect.colliderect(obs.rect):
                print(f"COLLISION! Final Score: {score // 10}")
                running = False
                break
            
            if obs.is_off_screen():
                obstacles.remove(obs)
        
        # 3. Render
        screen.fill(WHITE)
        
        # Draw ground line
        pygame.draw.line(screen, GRAY, (0, HEIGHT - 20), (WIDTH, HEIGHT - 20), 2)
        
        # Draw obstacles
        for obs in obstacles:
            obs.draw(screen)
        
        # Draw player
        player.draw(screen)
        
        # Draw Score
        score_text = font.render(f"Score: {score // 10}", True, BLACK)
        screen.blit(score_text, (20, 20))
        
        pygame.display.flip()
        
        # 4. Cap the frame rate
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
