import pygame
import sys
import random
import math
import os
from settings import *
from player import Player
from obstacle import Obstacle
from hand_tracker import HandTracker
from collectible import Collectible
import audio

class SparkParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        # Velocity vector
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, 1)
        self.color = color
        self.life = 255
        self.decay = random.randint(6, 12)
        self.size = random.randint(3, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay

    def draw(self, surface):
        if self.life > 0:
            # Draw particle as a glowing neon square using alpha surface
            p_surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            p_surf.fill((self.color[0], self.color[1], self.color[2], self.life))
            surface.blit(p_surf, (int(self.x), int(self.y)))

def load_high_score():
    if os.path.exists("highscore.txt"):
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read().strip())
        except Exception:
            return 0
    return 0

def save_high_score(score):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
    except Exception as e:
        print(f"Error saving highscore: {e}")

def draw_retro_text(surface, text, font, x, y, color):
    # Render clean minimalist 8-bit style solid text
    core_surf = font.render(text, True, color).convert_alpha()
    surface.blit(core_surf, (x, y))

def main():
    # Initialize Core modules
    pygame.init()
    pygame.font.init()
    audio.initialize_audio()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    
    clock = pygame.time.Clock()
    
    # Virtual Game surface for screen shake and glitch post-processing
    game_surface = pygame.Surface((WIDTH, HEIGHT))
    
    # Premium Font Sizes (Courier New for pure 8-bit digital typewriter feel)
    font_large = pygame.font.SysFont('Courier New', 44, bold=True)
    font_medium = pygame.font.SysFont('Courier New', 24, bold=True)
    font_small = pygame.font.SysFont('Courier New', 16, bold=True)
    
    # Game States
    STATE_MENU = 0
    STATE_PLAYING = 1
    STATE_GAMEOVER = 2
    game_state = STATE_MENU
    
    # Objects & Persistence
    player = Player()
    obstacles = []
    collectibles = []
    particles = []
    
    high_score = load_high_score()
    score = 0
    
    spawn_timer = 0.0
    import random
    next_spawn_distance = random.randint(850, 1300)
    
    collectible_timer = 0
    COLLECTIBLE_SPAWN_INTERVAL = 140
    
    game_speed = 5.6
    screen_shake = 0
    
    # Initialize Hand Tracker
    hand_tracker = HandTracker()
    
    # Load background images
    bg_stars = load_png("assets/bg_stars.png", has_alpha=False)
    bg_mountains = load_png("assets/bg_mountains.png", has_alpha=True)
    bg_floor = load_png("assets/bg_floor.png", has_alpha=True)
    
    # Parallax coordinates
    stars_x = 0.0
    mountains_x = 0.0
    floor_x = 0.0
    
    # Classic Dino Colors
    DINO_DARK = (83, 83, 83)
    DINO_LIGHT = (247, 247, 247)
    DINO_GOLD = (245, 166, 35)
    DINO_WHITE = (255, 255, 255)
    
    running = True
    
    while running:
        # 1. Process webcam gestures
        is_jumping, is_ducking, cam_surface = hand_tracker.process_frame()
        is_webcam_active = (cam_surface is not None)
        
        # 2. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if game_state == STATE_MENU:
                    if event.key == pygame.K_SPACE:
                        # Transition to playing state
                        game_state = STATE_PLAYING
                        obstacles.clear()
                        collectibles.clear()
                        particles.clear()
                        score = 0
                        game_speed = 5.6
                        player.y = player.ground_y
                        player.vel_y = 0
                        player.unduck()
                        audio.play_sound("pickup")
                        
                elif game_state == STATE_PLAYING:
                    if event.key == pygame.K_SPACE:
                        if player.y >= player.ground_y and not player.is_ducking:
                            player.jump()
                            audio.play_sound("jump")
                            # Emit jump sparks (Grey dust puffs)
                            for _ in range(10):
                                particles.append(SparkParticle(player.x + 20, player.ground_y + 55, DINO_DARK))
                    if event.key == pygame.K_DOWN:
                        player.duck()
                        audio.play_sound("slide")
                    if event.key == pygame.K_UP:
                        player.unduck()
                        
                elif game_state == STATE_GAMEOVER:
                    if event.key == pygame.K_r or event.key == pygame.K_SPACE:
                        # Reboot system / restart
                        game_state = STATE_PLAYING
                        obstacles.clear()
                        collectibles.clear()
                        particles.clear()
                        score = 0
                        game_speed = 5.6
                        player.y = player.ground_y
                        player.vel_y = 0
                        player.unduck()
                        audio.play_sound("pickup")
                        
        # 3. Apply Gestures in Playing State
        if game_state == STATE_PLAYING:
            # Gesture Overrides
            if is_webcam_active:
                if is_jumping:
                    # Automatically release slide/duck state to leap instantly!
                    if player.is_ducking:
                        player.unduck()
                    if player.y >= player.ground_y:
                        player.jump()
                        audio.play_sound("jump")
                        for _ in range(10):
                            particles.append(SparkParticle(player.x + 20, player.ground_y + 55, DINO_DARK))
                elif is_ducking:
                    if not player.is_ducking:
                        audio.play_sound("slide")
                    player.duck()
                else:
                    player.unduck()
                    
            # 4. Update Game State
            player.update()
            score += 1
            
            # Ramps speed smoothly based on score; starts at 5.6, capped at 11.5!
            game_speed = 5.6 + (score // 180) * 0.4
            if game_speed > 11.5:
                game_speed = 11.5
                
            # Parallax Scrolling scaled to speed
            stars_x -= 0.05 * game_speed
            if stars_x <= -WIDTH:
                stars_x = 0.0
                
            mountains_x -= 0.2 * game_speed
            if mountains_x <= -WIDTH:
                mountains_x = 0.0
                
            floor_x -= 1.0 * game_speed
            if floor_x <= -WIDTH:
                floor_x = 0.0
                
            # Emit player running or sliding sparks (Grey dust trail)
            if player.y >= player.ground_y:
                if player.is_ducking:
                    # Slide particles (Grey dust)
                    if random.random() < 0.6:
                        particles.append(SparkParticle(player.x + 5, player.ground_y + 28, DINO_DARK))
                else:
                    # Run particles (Grey dust sparks)
                    if random.random() < 0.3:
                        particles.append(SparkParticle(player.x + 10, player.ground_y + 55, DINO_DARK))
                        
            # Spawning Obstacles based on physical distance (guarantees safe landing space)
            spawn_timer += game_speed
            if spawn_timer >= next_spawn_distance:
                obstacles.append(Obstacle(speed=game_speed))
                spawn_timer = 0.0
                next_spawn_distance = random.randint(850, 1300)
                
                
            # Spawning Collectibles (Floating Data Cores)
            collectible_timer += 1
            if collectible_timer >= COLLECTIBLE_SPAWN_INTERVAL:
                # Do not spawn directly on top of an obstacle
                collectibles.append(Collectible(speed=game_speed))
                collectible_timer = 0
                COLLECTIBLE_SPAWN_INTERVAL = random.randint(120, 200)
                
            # Update all collectibles and check collection
            for col in collectibles[:]:
                col.update()
                
                # Player collects data core!
                if player.rect.colliderect(col.rect) and not col.collected:
                    col.collected = True
                    score += 500  # Grant huge score bonus (+50 points converted)
                    audio.play_sound("pickup")
                    # Emit glowing gold particles
                    for _ in range(12):
                        particles.append(SparkParticle(col.rect.centerx, col.rect.centery, DINO_GOLD))
                    collectibles.remove(col)
                    
                elif col.is_off_screen():
                    collectibles.remove(col)
                
            # Update all obstacles
            for obs in obstacles[:]:
                obs.update()
                
                # Check collision with custom explosion particles
                if player.rect.colliderect(obs.rect):
                    game_state = STATE_GAMEOVER
                    screen_shake = 15  # Trigger visual camera impact shake
                    audio.play_sound("crash")
                    
                    # Save high score
                    final_score_val = score // 10
                    if final_score_val > high_score:
                        high_score = final_score_val
                        save_high_score(high_score)
                        
                    # Trigger minimalist grey particle explosion
                    for _ in range(30):
                        particles.append(SparkParticle(player.rect.centerx, player.rect.centery, DINO_DARK))
                    break
                    
                if obs.is_off_screen():
                    obstacles.remove(obs)
                    
        else:
            # In Menu or Game Over state, scroll backgrounds at very slow ambient speeds
            stars_x -= 0.1
            if stars_x <= -WIDTH: stars_x = 0.0
            mountains_x -= 0.3
            if mountains_x <= -WIDTH: mountains_x = 0.0
            floor_x -= 1.0
            if floor_x <= -WIDTH: floor_x = 0.0
            
        # Update particles
        for p in particles[:]:
            p.update()
            if p.life <= 0:
                particles.remove(p)
                
        # 5. RENDER SCENE TO FRAMEBUFFER (game_surface)
        # Background layers (Parallax)
        game_surface.blit(bg_stars, (stars_x, 0))
        game_surface.blit(bg_stars, (stars_x + WIDTH, 0))
        
        game_surface.blit(bg_mountains, (mountains_x, 0))
        game_surface.blit(bg_mountains, (mountains_x + WIDTH, 0))
        
        game_surface.blit(bg_floor, (floor_x, HEIGHT - 100))
        game_surface.blit(bg_floor, (floor_x + WIDTH, HEIGHT - 100))
        
        # Render active items
        for col in collectibles:
            col.draw(game_surface)
            
        for obs in obstacles:
            obs.draw(game_surface)
            
        player.draw(game_surface)
        
        for p in particles:
            p.draw(game_surface)
            
        # Render Game State HUDs directly to framebuffer
        if game_state == STATE_MENU:
            # Bobbing logo animation using sine wave
            bob_offset = int(math.sin(pygame.time.get_ticks() * 0.006) * 6)
            logo_text = "MIND-WAVE DINO RUNNER"
            logo_width, logo_height = font_large.size(logo_text)
            draw_retro_text(game_surface, logo_text, font_large, WIDTH // 2 - logo_width // 2, 70 + bob_offset, DINO_DARK)
            
            # Clean Instructions Box
            inst_w, inst_h = 520, 140
            inst_x, inst_y = WIDTH // 2 - inst_w // 2, 150
            
            overlay = pygame.Surface((inst_w, inst_h), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 230))
            pygame.draw.rect(overlay, DINO_DARK, (0, 0, inst_w, inst_h), 2, border_radius=10)
            pygame.draw.rect(overlay, DINO_DARK, (0, 0, 10, inst_h), border_radius=10) # Left accent stripe
            game_surface.blit(overlay, (inst_x, inst_y))
            
            title_inst = font_medium.render("DINO GESTURE SYSTEM PROTOCOL", True, DINO_DARK).convert_alpha()
            game_surface.blit(title_inst, (inst_x + 20, inst_y + 12))
            
            guide_gest = font_small.render("1. WEBCAM INTERFACE: Open Hand to JUMP | Fist to DUCK/SLIDE", True, DINO_DARK).convert_alpha()
            guide_keys = font_small.render("2. KEYBOARD INTERFACE: SPACE to JUMP | DOWN ARROW to SLIDE", True, DINO_DARK).convert_alpha()
            guide_tip = font_small.render("Keep hand steady and clearly visible in center of camera feed.", True, (120, 120, 120)).convert_alpha()
            
            game_surface.blit(guide_gest, (inst_x + 20, inst_y + 45))
            game_surface.blit(guide_keys, (inst_x + 20, inst_y + 70))
            game_surface.blit(guide_tip, (inst_x + 20, inst_y + 105))
            
            # Blinking Start Prompt
            if (pygame.time.get_ticks() // 350) % 2 == 0:
                prompt_text = "PRESS SPACEBAR TO INITIALIZE CORE RUNNER"
                p_w, p_h = font_medium.size(prompt_text)
                draw_retro_text(game_surface, prompt_text, font_medium, WIDTH // 2 - p_w // 2, 310, DINO_DARK)
                
        elif game_state == STATE_PLAYING:
            # Draw Score panel in clean grey
            curr_score_val = score // 10
            score_text = f"SCORE: {curr_score_val}"
            draw_retro_text(game_surface, score_text, font_medium, 20, 20, DINO_DARK)
            
            # Speed/Progression indicator
            system_stat = f"SPEED: {int(game_speed * 10)}%"
            draw_retro_text(game_surface, system_stat, font_small, 20, 52, DINO_DARK)
            
        elif game_state == STATE_GAMEOVER:
            # Big Clean T-Rex GameOver banner
            crash_text = "G A M E   O V E R"
            c_w, c_h = font_large.size(crash_text)
            draw_retro_text(game_surface, crash_text, font_large, WIDTH // 2 - c_w // 2, 80, DINO_DARK)
            
            # Score panel box
            box_w, box_h = 360, 100
            box_x, box_y = WIDTH // 2 - box_w // 2, 150
            
            overlay = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 230))
            pygame.draw.rect(overlay, DINO_DARK, (0, 0, box_w, box_h), 2, border_radius=8)
            game_surface.blit(overlay, (box_x, box_y))
            
            final_score_txt = font_medium.render(f"FINAL SCORE: {score // 10}", True, DINO_DARK).convert_alpha()
            high_score_txt = font_medium.render(f"HIGH SCORE: {high_score}", True, DINO_DARK).convert_alpha()
            
            game_surface.blit(final_score_txt, (box_x + 25, box_y + 20))
            game_surface.blit(high_score_txt, (box_x + 25, box_y + 50))
            
            # Reboot blinking prompt
            if (pygame.time.get_ticks() // 350) % 2 == 0:
                reboot_text = "PRESS R TO REBOOT RUNNER MODULE"
                r_w, r_h = font_medium.size(reboot_text)
                draw_retro_text(game_surface, reboot_text, font_medium, WIDTH // 2 - r_w // 2, 280, DINO_DARK)
                
        # 6. POST-PROCESSING (Screen Shake blitted to Screen)
        shake_dx = 0
        shake_dy = 0
        if screen_shake > 0:
            shake_dx = random.randint(-4, 4)
            shake_dy = random.randint(-4, 4)
            screen_shake -= 1
            
        # Draw frame buffer to screen
        screen.blit(game_surface, (shake_dx, shake_dy))
            
        # 7. FOREGROUND UI RENDERING (webcam feed remains stable across all states!)
        if cam_surface:
            # Render PIP on top of screen with clean grey border
            pygame.draw.rect(screen, DINO_DARK, (WIDTH - 182, 18, 164, 124), 2, border_radius=4)
            screen.blit(cam_surface, (WIDTH - 180, 20))
            
            # Dynamic recognition status pill overlay
            if is_jumping:
                pygame.draw.rect(screen, (0, 150, 60), (WIDTH - 182, 146, 164, 20), border_radius=3)
                status_lbl = font_small.render("GESTURE: JUMP", True, DINO_WHITE).convert_alpha()
                screen.blit(status_lbl, (WIDTH - 172, 148))
            elif is_ducking:
                pygame.draw.rect(screen, (180, 80, 0), (WIDTH - 182, 146, 164, 20), border_radius=3)
                status_lbl = font_small.render("GESTURE: DUCK", True, DINO_WHITE).convert_alpha()
                screen.blit(status_lbl, (WIDTH - 172, 148))
            else:
                pygame.draw.rect(screen, DINO_DARK, (WIDTH - 182, 146, 164, 20), border_radius=3)
                status_lbl = font_small.render("GESTURE: RUNNING", True, (200, 200, 200)).convert_alpha()
                screen.blit(status_lbl, (WIDTH - 172, 148))
            
        # Global WebCam/Keyboard Connection HUD alert at the bottom
        hud_bar_y = HEIGHT - 20
        hud_bg = pygame.Surface((WIDTH, 20), pygame.SRCALPHA)
        hud_bg.fill((240, 240, 240, 220))
        screen.blit(hud_bg, (0, hud_bar_y))
        
        if is_webcam_active:
            status_text = "HYBRID INTERFACE CONNECTED // WEBCAM HUD STABLE [GESTURES ENABLED]"
            status_surf = font_small.render(status_text, True, (0, 120, 60)).convert_alpha()
        else:
            # Blinking offline alert
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                status_text = "WEBCAM HUD DETECTING FAILURE // KEYBOARD OVERRIDE ENGAGED [MANUAL CONTROL ONLY]"
                status_surf = font_small.render(status_text, True, (180, 80, 0)).convert_alpha()
            else:
                status_text = "WEBCAM HUD OFFLINE // SYSTEM STABLE"
                status_surf = font_small.render(status_text, True, DINO_DARK).convert_alpha()
                
        screen.blit(status_surf, (20, hud_bar_y + 1))
        
        pygame.display.flip()
        clock.tick(FPS)
        
    hand_tracker.release()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
