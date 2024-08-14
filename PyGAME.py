import pygame
import sys
import random
import time


pygame.init()

#preferred reso
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#handyman
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
gold = (255,215,0)

#sprites
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
character_img = pygame.image.load("E:\Run.png").convert_alpha()
jumping_character_img = pygame.image.load("E:\Jump.png").convert_alpha()  
pipe_img = pygame.image.load("D:\slot.png").convert_alpha()
title_img = pygame.image.load("E:\logo.png").convert_alpha()
gameover_screen = pygame.image.load("E:\Gameover.png").convert_alpha()
background_img = pygame.image.load("E:\poster.jpg").convert()
coin = pygame.image.load("E:\coin.png").convert_alpha()


character_img = pygame.transform.scale(character_img, (50, 50))  
jumping_character_img = pygame.transform.scale(jumping_character_img, (50, 50))  # Resize jumping sprite
pipe_img = pygame.transform.scale(pipe_img, (60, random.randint(150, 400)))
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

#sound effects
point_sound = pygame.mixer.Sound("E:\half.mp3")
hit_sound = pygame.mixer.Sound("E:\HIT1.mp3")
highscore_sound = pygame.mixer.Sound("E:\point.mp3")
initial_sound = pygame.mixer.Sound("E:\start.mp3")
jump_sound = pygame.mixer.Sound("E:\jump.mp3")
kaching = pygame.mixer.Sound("E:\kaching.mp3")
bg_music_path = "E:\music.mp3"

#seting up the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Let's GO Gambling!")


clock = pygame.time.Clock()

#character prop
BIRD_X = 100
BIRD_Y = 100
bird_velocity = 0
gravity = 0.5

#pipe
PIPE_GAP = 140
pipe_x = SCREEN_WIDTH
pipe_velocity = -4

# Score
score = 0
highscore = 0

# Highscore sound flag
new_highscore_set = False

# Speed increment flag
speed_increment_counter = 0

#highscore check
try:
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())
except FileNotFoundError:
    highscore = 0

# Timer for jump animation
jump_timer = None

def reset_game():
    global BIRD_Y, bird_velocity, pipe_x, score, new_highscore_set, pipe_velocity, speed_increment_counter
    BIRD_Y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipe_x = SCREEN_WIDTH
    score = 0
    new_highscore_set = False
    pipe_velocity = -4
    speed_increment_counter = 0

def screen_shake(shake_duration=300, shake_magnitude=10):
    shake_start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - shake_start_time < shake_duration:
        shake_x = random.randint(-shake_magnitude, shake_magnitude)
        shake_y = random.randint(-shake_magnitude, shake_magnitude)
        
        screen.blit(background_img, (0, 0))
        screen.blit(character_img, (BIRD_X + shake_x, BIRD_Y + shake_y))
        screen.blit(pipe_img, (pipe_x + shake_x, 0 + shake_y))
        screen.blit(pipe_img, (pipe_x + shake_x, pipe_img.get_height() + PIPE_GAP + shake_y))
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))
        text = font.render(f"Highscore: {highscore}", True, WHITE)
        screen.blit(text, (10, 30))
        
        pygame.display.update()
        clock.tick(60)

def game_over():
    pygame.mixer.music.stop()
   
    kaching.play()
    screen_shake()
    time.sleep(kaching.get_length())

    
    screen.blit(background_img, (0, 0))  
    go_x = (SCREEN_WIDTH - gameover_screen.get_width()) // 2
    go_y = (SCREEN_HEIGHT - gameover_screen.get_height()) // 2 - 50
    screen.blit(gameover_screen, (go_x, go_y))  

    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, gold)
    screen.blit(text, (10, 450))
    text = font.render(f"Highscore: {highscore}", True, gold)
    screen.blit(text, (220, 450))
    pygame.display.update()

    hit_sound.play() 
    time.sleep(hit_sound.get_length())

    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return

def start_screen():
    angle = 0  
    rotation_speed = 0.5 
    
    while True:
        screen.blit(background_img, (0, 0))
        
        title_x = (SCREEN_WIDTH - title_img.get_width()) // 2
        title_y = (SCREEN_HEIGHT - title_img.get_height()) // 2 - 50  

        screen.blit(title_img, (title_x, title_y))  

        #drawing the coins
        rotated_sprite = pygame.transform.rotate(coin, angle)
        rotated_rect = rotated_sprite.get_rect(center=(350,57))
        screen.blit(rotated_sprite, rotated_rect.topleft)
        rotated_sprite = pygame.transform.rotate(coin, angle)
        rotated_rect = rotated_sprite.get_rect(center=(50,57))
        screen.blit(rotated_sprite, rotated_rect.topleft)
        rotated_sprite = pygame.transform.rotate(coin, angle)
        rotated_rect = rotated_sprite.get_rect(center=(350,550))
        screen.blit(rotated_sprite, rotated_rect.topleft)
        rotated_sprite = pygame.transform.rotate(coin, angle)
        rotated_rect = rotated_sprite.get_rect(center=(50,550))
        screen.blit(rotated_sprite, rotated_rect.topleft)
        
        #front text
        font = pygame.font.Font(None, 48)
        text = font.render("Press SPACE to Start", True, WHITE)
        text_x = (SCREEN_WIDTH - text.get_width()) // 2
        screen.blit(text, (text_x, 390))

        pygame.display.update()

        angle = (angle + rotation_speed) % 360  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  

initial_sound.play()
start_screen()  
pygame.mixer.music.load(bg_music_path)


scale_factor = 2  

# Game loop
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump_sound.play()
                bird_velocity = -8

                if not pygame.mixer.music.get_busy(): 
                    pygame.mixer.music.play(-1)  

               
                jump_timer = current_time

    bird_velocity += gravity
    BIRD_Y += bird_velocity

    pipe_x += pipe_velocity
    if pipe_x < -pipe_img.get_width():
        pipe_x = SCREEN_WIDTH
        pipe_img = pygame.transform.scale(pipe_img, (60, random.randint(200, 400)))
        score += 1
        speed_increment_counter += 1

        if speed_increment_counter == 10:
            pipe_velocity -= 3
            speed_increment_counter = 0

        if score > highscore:
            highscore = score
            if not new_highscore_set:
                highscore_sound.play()
                new_highscore_set = True
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
        if score % 25 == 0:
            point_sound.play()

   
    if BIRD_Y < 0 or BIRD_Y > SCREEN_HEIGHT - character_img.get_height():
        game_over()  
        continue  

    if (pipe_x < BIRD_X + character_img.get_width() < pipe_x + pipe_img.get_width()) and \
       (BIRD_Y < pipe_img.get_height() or BIRD_Y + character_img.get_height() > pipe_img.get_height() + PIPE_GAP):
        game_over()  
        continue  

    
    screen.blit(background_img, (0, 0))

    if jump_timer and current_time - jump_timer < 1000:
        scaled_jump_sprite = pygame.transform.scale(jumping_character_img, (int(character_img.get_width() * scale_factor), int(character_img.get_height() * scale_factor)))
        screen.blit(scaled_jump_sprite, (BIRD_X - int((scaled_jump_sprite.get_width() - character_img.get_width()) / 2), BIRD_Y - int((scaled_jump_sprite.get_height() - character_img.get_height()) / 2)))
    else:
        scaled_sprite = pygame.transform.scale(character_img, (int(character_img.get_width() * scale_factor), int(character_img.get_height() * scale_factor)))
        screen.blit(scaled_sprite, (BIRD_X - int((scaled_sprite.get_width() - character_img.get_width()) / 2), BIRD_Y - int((scaled_sprite.get_height() - character_img.get_height()) / 2)))

    screen.blit(pipe_img, (pipe_x, 0))
    screen.blit(pipe_img, (pipe_x, pipe_img.get_height() + PIPE_GAP))

    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, gold)
    screen.blit(text, (10, 10))
    text = font.render(f"Highscore: {highscore}", True, gold)
    screen.blit(text, (10, 35))

    pygame.display.update()
    clock.tick(30)

