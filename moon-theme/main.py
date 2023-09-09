import math
import pygame
import random
import time


def remove_object_off_screen(obj_x, obj_y, obj_speed):
    for i in range(len(obj_x)):
        if obj_y[i] > HEIGHT:
            obj_y.pop(i)
            obj_x.pop(i)
            obj_speed.pop(i)
            return

def remove_object(obj_x, obj_y, obj_speed, index):
    obj_y.pop(i)
    obj_x.pop(i)
    obj_speed.pop(i)
        
def update_position(obj, obj_speed):
    for i in range(len(obj)):
        obj[i] += obj_speed[i]
        
def create_object(obj_x, obj_y, obj_speed):
    obj_x.append(random.randint(0, WIDTH - OBJECT_SIZE))
    obj_y.append(0 - OBJECT_SIZE)
    obj_speed.append(random.randint(2,7))
    

    

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
PLAYER_SIZE = 246
OBJECT_SIZE = 160
PLAYER_SPEED = 5
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DELAY = time.time_ns

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Game")

# Load images
player_img = pygame.image.load("resources/cohete_on_wf.png")
enemy_img = pygame.image.load("resources/Rock Pile.png")
fuel_img = pygame.image.load("resources/fuel.png")
moon_img = pygame.image.load("resources/moon.png")
background_img = pygame.image.load("resources/back.png")

# Initialize Pygame fonts
pygame.font.init()
font = pygame.font.Font(None, 36)

# Initialize moon position
moon_x = WIDTH // 2 - 256
moon_y = -256

# Initialize player position
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT - PLAYER_SIZE
player_x_change = 0

# Initialize enemy position
enemy_x = []
enemy_y = []
enemy_y_speed = []

# Initialize fuel position
fuel_x = []
fuel_y = []
fuel_y_speed = []

# Initialize fuel level
fuel_level = 100

# Initialize variables for score
score = 1

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if fuel_level > 0:
                if event.key == pygame.K_LEFT:
                    player_x_change = -PLAYER_SPEED
                if event.key == pygame.K_RIGHT:
                    player_x_change = PLAYER_SPEED
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    PLAYER_SPEED *= 3  # Double the player speed
            elif event.key == pygame.K_r:
                # Reset the game
                fuel_level = 100
                player_x = WIDTH // 2 - PLAYER_SIZE // 2
                player_y = HEIGHT - PLAYER_SIZE
                score = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                PLAYER_SPEED /= 3  # Reset player speed to normal when Shift key is released
            if player_x_change > 0:
                if event.key == pygame.K_RIGHT:
                    player_x_change = 0
            else:
                if event.key == pygame.K_LEFT:
                    player_x_change = 0


    player_x += player_x_change

    # Boundaries for the player
    if player_x < 0 - PLAYER_SIZE/4:
        player_x = 0 - PLAYER_SIZE/4
    elif player_x > WIDTH - PLAYER_SIZE * 0.75:
        player_x = WIDTH - PLAYER_SIZE * 0.75

    # Delete enemy and fuel
    remove_object_off_screen(enemy_x, enemy_y, enemy_y_speed)
    remove_object_off_screen(fuel_x, fuel_y, fuel_y_speed)
    
    # Move enemy and fuel
    update_position(enemy_y, enemy_y_speed)
    update_position(fuel_y, fuel_y_speed)

    # Respawn enemy and fuel
    if fuel_level > 0:
        if random.randint(1,40) == 1:
            create_object(enemy_x, enemy_y, enemy_y_speed)
        if random.randint(1,150) == 1:
            create_object(fuel_x, fuel_y, fuel_y_speed)

    # Check for collision with enemy
    for i in range(len(enemy_x)):
        if (
            player_x < enemy_x[i] + OBJECT_SIZE
            and player_x + PLAYER_SIZE > enemy_x[i]
            and player_y < enemy_y[i] + OBJECT_SIZE
            and player_y + PLAYER_SIZE > enemy_y[i]
        ):
            fuel_level -= 20
            remove_object(enemy_x, enemy_y, enemy_y_speed, i)
            break
            

    # Check for collision with fuel
    for i in range(len(fuel_x)):
        if (
            player_x < fuel_x[i] + OBJECT_SIZE
            and player_x + PLAYER_SIZE > fuel_x[i]
            and player_y < fuel_y[i] + OBJECT_SIZE
            and player_y + PLAYER_SIZE > fuel_y[i]
        ):
            fuel_level += 15
            remove_object(fuel_x, fuel_y, fuel_y_speed, i)
            break
        
    # Reduce fuel based on time
    if score % 100 == 0:
        fuel_level -= 1

    # Keep fuel level within bounds
    if fuel_level < 0:
        fuel_level = 0
    elif fuel_level > 100:
        fuel_level = 100

    # Clear the screen
    screen.blit(background_img, (0,0))

    # Draw player, enemy, and fuel
    screen.blit(player_img, (player_x, player_y))
    screen.blit(moon_img, (moon_x, moon_y))
    for i in range(len(enemy_x)):
        screen.blit(enemy_img, (enemy_x[i], enemy_y[i]))
    for i in range(len(fuel_x)):
        screen.blit(fuel_img, (fuel_x[i], fuel_y[i]))

    # Draw fuel level
    pygame.draw.rect(screen, GREEN, (10, 10, fuel_level * 2, 20))
    pygame.draw.rect(screen, RED, (10, 10, 200, 20), 2)
    
    # Drawing score
    if fuel_level > 0:
        score += 1
        score_text = font.render(f"Score: {math.floor(score / 150)}", True, BLUE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, 50)
    screen.blit(score_text, score_rect)
    
    pygame.display.update()
    if fuel_level <= 0:
        for i in range(len(enemy_x)):
            remove_object(enemy_x,enemy_y, enemy_y_speed, i)
            break
        for i in range(len(fuel_x)):
            remove_object(fuel_x,fuel_y, fuel_y_speed, i)
            break
        game_over_text = font.render("Game Over", True, RED)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WIDTH // 2, HEIGHT // 2)
        screen.blit(game_over_text, game_over_rect)

        retry_text = font.render("Press R to retry or Q to quit", True, BLUE)
        retry_rect = retry_text.get_rect()
        retry_rect.center = (WIDTH // 2, HEIGHT // 2 + 40)
        screen.blit(retry_text, retry_rect)

        pygame.display.update()

# Quit the game
pygame.quit()


