#TODO: basic powerup (points)

#Libraries
import pygame, time

#FPS related stuff
CLOCK_TOOL = pygame.time.Clock()
CLOCK_FPS_LIMIT = 144

#Keybinds
KEY_MOVE_LEFT = pygame.K_LEFT
KEY_MOVE_RIGHT = pygame.K_RIGHT
KEY_MOVE_UP = pygame.K_UP
KEY_MOVE_DOWN = pygame.K_DOWN
KEY_FOCUS = pygame.K_z

#Player values
PLAYER_SPEED_NORMAL = 250   # pixel per frame
PLAYER_SPEED_FOCUS = 100     # pixel per frame

#Window vars
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_CAPTION = "simple bullethell"
WINDOW_FILL_COLOR = (0,0,0)
WINDOW_ICON = pygame.image.load("data/textures/icon.png")

#Window creation
WINDOW = pygame.display.set_mode(WINDOW_SIZE, pygame.NOFRAME)
pygame.display.set_caption(WINDOW_CAPTION)
pygame.display.set_icon(WINDOW_ICON)

#Object default values
DEFAULT_X = 0
DEFAULT_Y = 0
DEFAULT_Z = 0
DEFAULT_ON = False
DEFAULT_TEXTURE_ID = 0
DEFAULT_FREE = True
DEFAULT_KEYCONTROL = False
DEFAULT_COLLIDE = False

#Object arrays
OBJECT_COUNT_MAX = 500
x = [DEFAULT_X] * OBJECT_COUNT_MAX                                  # x pos
y = [DEFAULT_Y] * OBJECT_COUNT_MAX                                  # y pos
z = [DEFAULT_Z] * OBJECT_COUNT_MAX                                  # z layer
on = [DEFAULT_ON] * OBJECT_COUNT_MAX                                # need to render?
texture_id = [DEFAULT_TEXTURE_ID] * OBJECT_COUNT_MAX                # texture array index
free = [DEFAULT_FREE] * OBJECT_COUNT_MAX                            # can be overwrited?
keycontrol = [DEFAULT_KEYCONTROL] * OBJECT_COUNT_MAX                # moved by keyboard?
collide = [DEFAULT_COLLIDE] * OBJECT_COUNT_MAX                      # collision enabled?

#Find first free obj
def freeObjectID():
    for obj in range(OBJECT_COUNT_MAX):
        if free[obj] == True:
            return obj

#Generate an object
def createObject(
                    _x = DEFAULT_X,
                    _y = DEFAULT_Y,
                    _z = DEFAULT_Z,
                    _on = DEFAULT_ON,
                    _texture_id = DEFAULT_TEXTURE_ID,
                    _free = DEFAULT_FREE,
                    _keycontrol = DEFAULT_KEYCONTROL,
                    _collide = DEFAULT_COLLIDE
                ):
    id = freeObjectID()
    x[id] = _x
    y[id] = _y
    z[id] = _z
    on[id] = _on
    texture_id[id] = _texture_id
    free[id] = _free
    keycontrol[id] = _keycontrol
    collide[id] = _collide

#Z Layers
Z_LAYER_COUNT = 10

#Texture values
TEXTURE_COUNT = 500
ID_TEXTURE_DEFAULT = 0
ID_TEXTURE_PLAYER = 1
ID_TEXTURE_INGAMEUIBG = 2

#Texture array
texture = [None] * TEXTURE_COUNT
texture[ID_TEXTURE_DEFAULT] = pygame.image.load("data/textures/default.png")
texture[ID_TEXTURE_PLAYER] = pygame.image.load("data/textures/player.png")
texture[ID_TEXTURE_INGAMEUIBG] = pygame.image.load("data/textures/ingame_ui_bg.png")

#Collision Mask array (IDs same as textures)
mask = [None] * TEXTURE_COUNT
mask[ID_TEXTURE_PLAYER] = pygame.mask.from_surface(texture[ID_TEXTURE_PLAYER])
mask[ID_TEXTURE_INGAMEUIBG] = pygame.mask.from_surface(texture[ID_TEXTURE_INGAMEUIBG])

#Create the player [DEBUG]
createObject(800,400,0,True,1,False,True,True)

#Create the ingame ui bg
createObject(0,0,9,True,ID_TEXTURE_INGAMEUIBG,False,False,True)

# !!! NEEDS TO BE LAST INIT CALL !!!
clockfix_now = 0
clockfix_past = time.time()
clockfix_dt = 0

#Game loop
running_flag = True
while running_flag:
    
    #Clock FPS fix
    CLOCK_TOOL.tick(CLOCK_FPS_LIMIT)
    clockfix_now = time.time()
    clockfix_dt = clockfix_now - clockfix_past
    clockfix_past = clockfix_now

    #Event system
    for event in pygame.event.get():

        #On quit
        if event.type == pygame.QUIT:
            running_flag = False
    
    #Get frame's input
    pressed_keys = pygame.key.get_pressed()
    
    #keyboard movement
    for obj in range(OBJECT_COUNT_MAX):
        if keycontrol[obj]:

            # input recognition
            input_dir_x = 0
            input_dir_y = 0
            if pressed_keys[KEY_MOVE_LEFT]: input_dir_x -= 1
            if pressed_keys[KEY_MOVE_RIGHT]: input_dir_x += 1
            if pressed_keys[KEY_MOVE_UP]: input_dir_y -= 1
            if pressed_keys[KEY_MOVE_DOWN]: input_dir_y += 1

            # focus check
            if pressed_keys[KEY_FOCUS]: speed = PLAYER_SPEED_FOCUS
            else: speed = PLAYER_SPEED_NORMAL

            # precalculate next frame pos
            # speed * input dir * delta = frame motion
            next_x = x[obj] + (speed * input_dir_x * clockfix_dt)
            next_y = y[obj] + (speed * input_dir_y * clockfix_dt)

            # collision flag
            collision_flag_x = False
            collision_flag_y = False

            # check collision
            if collide[obj]:
                
                # check other rendered colliders
                for obs in range(OBJECT_COUNT_MAX):

                    #Ignore self
                    if obs == obj:
                        continue

                    if collide[obs]:
                        if on[obs]:
                            
                            # calculate mask offset for both current and next frame
                            next_off_x = x[obs] - next_x
                            next_off_y = y[obs] - next_y
                            off_x = x[obs] - x[obj]
                            off_y = y[obs] - y[obj]

                            # check overlapping points in both x and y axis
                            if mask[texture_id[obj]].overlap(mask[texture_id[obs]], (next_off_x, off_y)):
                                collision_flag_x = True
                            if mask[texture_id[obj]].overlap(mask[texture_id[obs]], (off_x, next_off_y)):
                                collision_flag_y = True
            
            # if there's no collision then update the position
            if not collision_flag_x:
                x[obj] = next_x
            if not collision_flag_y:
                y[obj] = next_y
                
    
    #Render system
    WINDOW.fill(WINDOW_FILL_COLOR)  # clear
    for _z in range(Z_LAYER_COUNT): # sort z layer
        for obj in range(OBJECT_COUNT_MAX): # loop objects
            if z[obj] == _z:                    # if both on same z layer
                if on[obj]:                         # if on
                    WINDOW.blit(texture[texture_id[obj]], (x[obj], y[obj])) # render it
    pygame.display.flip()   # update
    
    