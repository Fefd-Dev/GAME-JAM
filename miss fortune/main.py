import pygame
import random
import time

# I want a charecter that can turn left and right and move by jumping difrent lengths by holding down the space bar
# I also want to be able to jump on platforms to get to the end of the level
# I want the platforms to move up and down

def update_position(object, object_speed):
    """Update the position of an object"""
    for i in range(len(object)):
        if object[0] < 0:
            object[0] = 0
            object_speed[0] *= -1
        elif object[0] > WIDTH - PLAYER_SIZE:
            object[0] = WIDTH - PLAYER_SIZE
            object_speed[0] *= -1
            
        object[i] += object_speed[i]
    


# Constants
WIDTH, HEIGHT = 1920, 1080
PLAYER_SIZE = 50

# Initialize player position
player_position = [WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE]
# player_y = HEIGHT - PLAYER_SIZE
player_position_update = [0,0]
# player_y_change = 0
right = True


# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Get out of the well")

runing = True
while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                runing = False
            if event.key == pygame.K_LEFT:
                right = False
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_SPACE:
                escape = True
                player_position_update[1] = -6
                while escape:
                    for event in pygame.event.get():
                        if right:
                            player_position_update[0] += 2
                            player_position_update[1] += -3
                        else:
                            player_position_update[0] -= 2
                            player_position_update[1] += -3
                        if event.type == pygame.KEYUP:
                            escape = False
                            break
                    time.sleep(0.05)
                if player_position_update[0] > 0:
                    player_position_update[0] = min(player_position_update[0], 16)
                else:
                    player_position_update[0] = max(player_position_update[0], -16)
                player_position_update[1] = max(player_position_update[1], -30)
                
    update_position(player_position, player_position_update)
    if player_position[1] < HEIGHT - PLAYER_SIZE:
        player_position_update[1] += 1
    else:
        player_position_update[0] = 0
        player_position_update[1] = 0
        player_position[1] = HEIGHT - PLAYER_SIZE
        
                
    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the player
    # print(player_position)
    pygame.draw.rect(screen, (0, 0, 255), (player_position[0], player_position[1], PLAYER_SIZE, PLAYER_SIZE))

    # Update the screen
    pygame.display.update()