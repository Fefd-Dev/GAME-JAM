import pygame
import random
import time
import threading
import keyboard

# I want a charecter that can turn left and right and move by jumping difrent lengths by holding down the space bar
# I also want to be able to jump on platforms to get to the end of the level
# I want the platforms to move up and down

# Global variables
## Player position can be read from anywhere because it is a array##
global runing
global looking_right
global on_ground

def on_ground_check():
    '''Check if the player is on the ground'''
    print('on_ground_check started')
    global on_ground
    global runing
    while runing:
        # TODO: make it so that the player can't go through objects
        # TODO: make collision detection
        if player_position[1] >= HEIGHT - PLAYER_SIZE:
            # on_ground = True
            time.sleep(0.01)
        
def on_bottom_check():
    '''Check if the player is on the bottom'''
    global on_ground
    if not on_ground:
        if player_position[1] < HEIGHT - PLAYER_SIZE:
            player_position_update[1] += 1
            player_position_update[1] = min(player_position_update[1], 30)
        else:
            player_position_update[0] = 0
            player_position_update[1] = 0
            player_position[1] = HEIGHT - PLAYER_SIZE
            on_ground = True

def update_position(object, object_speed):
    """Update the position of an object"""
    if on_ground:
        return
    for i in range(len(object)):
        if object[0] < 0:
            object[0] = 0
            object_speed[0] *= -1
        elif object[0] > WIDTH - PLAYER_SIZE:
            object[0] = WIDTH - PLAYER_SIZE
            object_speed[0] *= -1
            
        object[i] += object_speed[i]
        
def player_acceleration_update():
    '''
        1. Get the events\n
        2. Update the acceleration of the player\n
        3. Limit the acceleration of the player
    '''
    global on_ground
    
    if not keyboard.is_pressed('space') or not on_ground or player_position_update[1] == -30:
        on_ground = False
        return False
    player_position_update[1] += -0.15
    if looking_right:
        player_position_update[0] += 0.1
        player_position_update[0] = min(max(player_position_update[0], 2), 16)
    else:
        player_position_update[0] -= 0.1
        player_position_update[0] = max(min(player_position_update[0], -2), -16)
    player_position_update[1] = max(min(player_position_update[1], -4), -30)
    
    return True
    
def input_handler():
    '''Handle the input from the user'''
    print('input_handler started')
    global runing
    global looking_right
    while runing:
        if keyboard.is_pressed('q'):
            runing = False
        if keyboard.is_pressed('left'):
            looking_right = False
        if keyboard.is_pressed('right'):
            looking_right = True
        time.sleep(0.01)

def space_handler():
    '''Handle the space bar'''
    print('space_handler started')
    global runing
    global on_ground
    global looking_right
    while runing:
        if on_ground:
            player_acceleration_update()
        time.sleep(0.01)


# Constants
WIDTH, HEIGHT = 1920, 1080
PLAYER_SIZE = 50
Clock = pygame.time.Clock()
FPS = 60

# Initialize player position
player_position = [WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - PLAYER_SIZE]
player_position_update = [0,0]
looking_right = True
on_ground = True



# Initialize pygame
pygame.init()
runing = True

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Get out of the well")

# Starts threads
threading.Thread(target=input_handler).start()
threading.Thread(target=space_handler).start()
threading.Thread(target=on_ground_check).start()

while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
                
    # Update the position of the player
    update_position(player_position, player_position_update)
    
    # Check if the player is on the bottom of the screen
    on_bottom_check()
                
    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the player
    pygame.draw.rect(screen, (0, 0, 255), (player_position[0], player_position[1], PLAYER_SIZE, PLAYER_SIZE))

    # Update the screen
    pygame.display.update()
    
    # Limit the FPS
    Clock.tick(FPS)