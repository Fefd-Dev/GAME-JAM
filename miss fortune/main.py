import pygame
import random
import time
import threading
import keyboard

# Global variables
## Player position can be read from anywhere because it is a array##
global runing
global looking_right
global on_ground

def create_platforms():
    '''Create the platforms'''
    print('create_platforms started')
    global runing
    
    # Posisions of the platforms x and y
    new_platform = [random.randint(0, WIDTH - PLAYER_SIZE), int(player_position[1]) - HEIGHT // 4, random.randint(200, 500)]
    platforms.append(new_platform)
    while runing:
        if player_position[1] - new_platform[1] < 1000:
            new_platform = [random.randint(max(0, new_platform[0]-900), min(WIDTH, new_platform[0]+900)), random.randint(new_platform[1]-450, new_platform[1]-200), random.randint(200, 500)]
            platforms.append(new_platform)
        
        time.sleep(0.1)

def on_platform_check():
    '''Check if the player is on a platform'''
    print('on_platform_check started')
    global on_ground
    global runing
    platform_id = 0
    while runing:  
        time.sleep(.01)
        if player_position[1] + PLAYER_SIZE < platforms[platform_id][1] + platform_height:
            platform_id += 1
        elif platform_id > 0:
            platform_id -= 1
        
        if not (player_position[0] <= platforms[platform_id][0] + platforms[platform_id][2] and player_position[0] + PLAYER_SIZE >= platforms[platform_id][0]):
            continue
        if (player_position[1] >= platforms[platform_id][1] + platform_height and player_position[1] <= platforms[platform_id][1] + platform_height*2):
            player_position[1] = platforms[platform_id][1] + platform_height*2
            player_position_update[1] = 1
            on_ground = False
            continue
            
        if not (player_position[1] + PLAYER_SIZE <= platforms[platform_id][1] + platform_height and player_position[1] + PLAYER_SIZE >= platforms[platform_id][1]):
            continue
        if not (player_position_update[1] > 0):
            continue
        
        on_ground = True
        player_position_update[0] = 1 
        player_position_update[1] = 1
        player_position[1] = platforms[platform_id][1] - PLAYER_SIZE
        
def on_bottom_check():
    '''Check if the player is on the bottom'''
    global on_ground
    gravety_force = 1
    max_update = 20
        
    if not on_ground:
        if player_position[1] < HEIGHT - PLAYER_SIZE:
            player_position_update[1] += gravety_force
            player_position_update[1] = min(player_position_update[1], max_update)
        else:
            player_position_update[0] = 0
            player_position_update[1] = 0
            player_position[1] = HEIGHT - PLAYER_SIZE
            on_ground = True
            
def screen_scrool():
    '''Screen scrolling vertically'''
    print('screen_scrool started')
    global runing
    scrool_amount = 0
    while runing:
        time.sleep(0.01)
        if player_position[1] < HEIGHT // 2 and on_ground:
            player_position[1] += 20
            scrool_amount += 20
            for platform in platforms:
                platform[1] += 20
        if scrool_amount > 0 and player_position[1] > HEIGHT - HEIGHT // 3:
            player_position[1] -= 20
            scrool_amount -= 20
            for platform in platforms:
                platform[1] -= 20

def update_position(object, object_speed):
    """Update the position of an player"""
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
    velocity_y = 0.15
    velocity_x = 0.1
    max_update_x = 16
    max_update_y = 30
    if not keyboard.is_pressed('space') or not on_ground or player_position_update[1] == -max_update_y:
        if player_position_update[1] < 0:
            on_ground = False
        return False
    player_position_update[1] -= velocity_y
    if looking_right:
        player_position_update[0] += velocity_x
        player_position_update[0] = min(max(player_position_update[0], 2), max_update_x)
    else:
        player_position_update[0] -= velocity_x
        player_position_update[0] = max(min(player_position_update[0], -2), -max_update_x)
    player_position_update[1] = max(min(player_position_update[1], -4), -max_update_y)
    
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

# Initialize platforms
platform_height = 30
platforms = []

# Initialize pygame
pygame.init()
runing = True

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Get out of the well")

# Starts threads
threading.Thread(target=input_handler).start()
threading.Thread(target=space_handler).start()
threading.Thread(target=on_platform_check).start()
threading.Thread(target=create_platforms).start()
threading.Thread(target=screen_scrool).start()

while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
                
    # Update the position of the player
    update_position(player_position, player_position_update)
    
    # Check if the player is on the bottom of the screen
    on_bottom_check()    
                
    # Clear the screen
    screen.fill((255, 255, 255))
    
    # draw the platforms
    for platform in platforms:
        pygame.draw.rect(screen, (0, 0, 0), (platform[0], platform[1], platform[2], platform_height))
    # Draw the player
    pygame.draw.rect(screen, (0, 0, 255), (player_position[0], player_position[1], PLAYER_SIZE, PLAYER_SIZE))

    # Update the screen
    pygame.display.update()
    
    # Limit the FPS
    Clock.tick(FPS)