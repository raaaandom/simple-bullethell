#TODO: CUSTOM ICON, MAP LIMIT

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
PLAYER_SPEED_FOCUS = 150     # pixel per frame

#Window vars
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_CAPTION = "simple bullethell"
WINDOW_FILL_COLOR = (0,0,0)

#Window creation
WINDOW = pygame.display.set_mode(WINDOW_SIZE, pygame.NOFRAME)
pygame.display.set_caption(WINDOW_CAPTION)

#Object default values
DEFAULT_X = 0
DEFAULT_Y = 0
DEFAULT_Z = 0
DEFAULT_ON = False
DEFAULT_TEXTURE_ID = 0
DEFAULT_FREE = True
DEFAULT_KEYCONTROL = False

#Object arrays
OBJECT_COUNT_MAX = 500
x = [DEFAULT_X] * OBJECT_COUNT_MAX                                  # x pos
y = [DEFAULT_Y] * OBJECT_COUNT_MAX                                  # y pos
z = [DEFAULT_Z] * OBJECT_COUNT_MAX                                  # z layer
on = [DEFAULT_ON] * OBJECT_COUNT_MAX                                # need to render?
texture_id = [DEFAULT_TEXTURE_ID] * OBJECT_COUNT_MAX                # texture array index
free = [DEFAULT_FREE] * OBJECT_COUNT_MAX                            # can be overwrited?
keycontrol = [DEFAULT_KEYCONTROL] * OBJECT_COUNT_MAX                # moved by keyboard?

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
                    _keycontrol = DEFAULT_KEYCONTROL
                ):
    id = freeObjectID()
    x[id] = _x
    y[id] = _y
    z[id] = _z
    on[id] = _on
    texture_id[id] = _texture_id
    free[id] = _free
    keycontrol[id] = _keycontrol

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

#Create the player [DEBUG]
createObject(800,400,0,True,1,False,True)

#Create the ingame ui bg
createObject(0,0,9,True,ID_TEXTURE_INGAMEUIBG,False,False)

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

            # speed * input dir * delta = frame motion
            x[obj] += speed * input_dir_x * clockfix_dt
            y[obj] += speed * input_dir_y * clockfix_dt
    
    #Render system
    WINDOW.fill(WINDOW_FILL_COLOR)  # clear
    for _z in range(Z_LAYER_COUNT): # sort z layer
        for obj in range(OBJECT_COUNT_MAX): # loop objects
            if z[obj] == _z:                    # if both on same z layer
                if on[obj]:                         # if on
                    WINDOW.blit(texture[texture_id[obj]], (x[obj], y[obj])) # render it
    pygame.display.flip()   # update
    
    