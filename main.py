#TODO: collision fix on high pixel per sec

#Pointer recreation in python (only way to recreate pointer concept)
#this one is useful when displaying variable values in rendered fonts
class Pointer():

    def __init__(self, value) -> None:
        self.value = value

    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value
    
    def add_value(self, value):
        self.value += value
    
    def mul_value(self, value):
        self.value *= value

#Libraries
import pygame, time, random

#Initialize pygame
pygame.init()

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
PLAYER_SPEED_NORMAL = 250   # pixel per second
PLAYER_SPEED_FOCUS = 100    # pixel per second

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

#Powerup values
POWERUP_POINT = 1
POWERUP_WEAPON = 2
POWERUP_CHARGE = 3

# in game points var (increments with point powerup)
points = Pointer(0)
points_goal = Pointer(3)

# life var
life = Pointer(0)

#Object default values
DEFAULT_X = 0
DEFAULT_Y = 0
DEFAULT_Z = 0
DEFAULT_ON = True
DEFAULT_TEXTURE_ID = 0
DEFAULT_FREE = False
DEFAULT_KEYCONTROL = False
DEFAULT_COLLIDE = False
DEFAULT_POWERUP = None
DEFAULT_POWERUP_AMOUNT = 0
DEFAULT_POWERUP_PICKUP = False
DEFAULT_FONT_ID = None
DEFAULT_FONT_TEXT = ""
DEFAULT_FONT_AA = False
DEFAULT_FONT_COLOR = (255,255,255)
DEFAULT_FONT_REPLACES = []

#Object arrays
OBJECT_COUNT_MAX = 500
x = [DEFAULT_X] * OBJECT_COUNT_MAX                                  # x pos
y = [DEFAULT_Y] * OBJECT_COUNT_MAX                                  # y pos
z = [DEFAULT_Z] * OBJECT_COUNT_MAX                                  # z layer
on = [False] * OBJECT_COUNT_MAX                                     # need to render?
texture_id = [DEFAULT_TEXTURE_ID] * OBJECT_COUNT_MAX                # texture array index
free = [True] * OBJECT_COUNT_MAX                                    # can be overwrited?
keycontrol = [DEFAULT_KEYCONTROL] * OBJECT_COUNT_MAX                # moved by keyboard?
collide = [DEFAULT_COLLIDE] * OBJECT_COUNT_MAX                      # collision enabled?
powerup = [DEFAULT_POWERUP] * OBJECT_COUNT_MAX                      # powerup type (point, charge ...) 
powerup_amount = [DEFAULT_POWERUP_AMOUNT] * OBJECT_COUNT_MAX        # powerup value (tot points, charge...)
powerup_pickup = [DEFAULT_POWERUP_PICKUP] * OBJECT_COUNT_MAX        # should pickup powerups?
font_id = [DEFAULT_FONT_ID] * OBJECT_COUNT_MAX                      # font used to render text
font_text = [DEFAULT_FONT_TEXT] * OBJECT_COUNT_MAX                  # text to render
font_color = [DEFAULT_FONT_COLOR] * OBJECT_COUNT_MAX                # color to render the text with
font_aa = [DEFAULT_FONT_AA] * OBJECT_COUNT_MAX                      # should use antialiasing?
font_replaces = [DEFAULT_FONT_REPLACES] * OBJECT_COUNT_MAX          # list of pointers with variable values to display in string

#Check collision between two objects
def checkCollision(obj1, obj2, offx=None, offy=None):
    
    if offx == None:
        offx = x[obj2]-x[obj1]

    if offy == None:
        offy = y[obj2]-y[obj1]
    
    if mask[texture_id[obj1]].overlap(mask[texture_id[obj2]], (offx, offy)):
        return True

    return False

#Find first free obj
def freeObjectID():
    for obj in range(OBJECT_COUNT_MAX):
        if free[obj] == True:
            return obj

def deleteObject(obj):
    on[obj] = False
    free[obj] = True

#Generate an object
def createObject(
                    _x = DEFAULT_X,
                    _y = DEFAULT_Y,
                    _z = DEFAULT_Z,
                    _on = DEFAULT_ON,
                    _texture_id = DEFAULT_TEXTURE_ID,
                    _free = DEFAULT_FREE,
                    _keycontrol = DEFAULT_KEYCONTROL,
                    _collide = DEFAULT_COLLIDE,
                    _powerup = DEFAULT_POWERUP,
                    _powerup_amount = DEFAULT_POWERUP_AMOUNT,
                    _powerup_pickup = DEFAULT_POWERUP_PICKUP,
                    _font_id = DEFAULT_FONT_ID,
                    _font_text = DEFAULT_FONT_TEXT,
                    _font_color = DEFAULT_FONT_COLOR,
                    _font_aa = DEFAULT_FONT_AA,
                    _font_replaces = DEFAULT_FONT_REPLACES
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
    powerup[id] = _powerup
    powerup_amount[id] = _powerup_amount
    powerup_pickup[id] = _powerup_pickup
    font_id[id] = _font_id
    font_text[id] = _font_text
    font_color[id] = _font_color
    font_aa[id] = _font_aa
    font_replaces[id] = _font_replaces

#Z Layers
Z_LAYER_COUNT = 10

#Font values
FONT_VAR_PLACEHOLDER = "$x"
FONT_COUNT = 20

ID_FONT_CIRNO = 1
HEIGHT_FONT_CIRNO = 32

#Font array
font = [None] * FONT_COUNT
font[ID_FONT_CIRNO] = pygame.font.Font("data/fonts/cirno.ttf", HEIGHT_FONT_CIRNO)

#Texture values
TEXTURE_COUNT = 500
ID_TEXTURE_DEFAULT = 0
ID_TEXTURE_PLAYER = 1
ID_TEXTURE_INGAMEUIBG = 2
ID_TEXTURE_POINT = 3
ID_TEXTURE_WEAPON = 4
ID_TEXTURE_CHARGE = 5

#Texture array
texture = [None] * TEXTURE_COUNT
texture[ID_TEXTURE_DEFAULT] = pygame.image.load("data/textures/default.png")
texture[ID_TEXTURE_PLAYER] = pygame.image.load("data/textures/player.png")
texture[ID_TEXTURE_INGAMEUIBG] = pygame.image.load("data/textures/ingame_ui_bg.png")
texture[ID_TEXTURE_POINT] = pygame.image.load("data/textures/point.png")
texture[ID_TEXTURE_WEAPON] = pygame.image.load("data/textures/weapon.png")
texture[ID_TEXTURE_CHARGE] = pygame.image.load("data/textures/charge.png")

#Collision Mask array (IDs same as textures)
mask = [None] * TEXTURE_COUNT
mask[ID_TEXTURE_PLAYER] = pygame.mask.from_surface(texture[ID_TEXTURE_PLAYER])
mask[ID_TEXTURE_INGAMEUIBG] = pygame.mask.from_surface(texture[ID_TEXTURE_INGAMEUIBG])
mask[ID_TEXTURE_POINT] = pygame.mask.from_surface(texture[ID_TEXTURE_POINT])
mask[ID_TEXTURE_WEAPON] = pygame.mask.from_surface(texture[ID_TEXTURE_WEAPON])
mask[ID_TEXTURE_CHARGE] = pygame.mask.from_surface(texture[ID_TEXTURE_CHARGE])

#Create the player
createObject(
_x=800,
_y=400,
_z=4,
_texture_id=ID_TEXTURE_PLAYER,
_keycontrol=True,
_collide=True,
_powerup_pickup=True
)

#Create the ingame ui bg
createObject(
_x=0,
_y=0,
_z=8,
_texture_id=ID_TEXTURE_INGAMEUIBG,
_collide=True
)

#Create powerup [debug]
createObject(
_x=600,
_y=300,
_z=3,
_texture_id=ID_TEXTURE_POINT,
_powerup=POWERUP_POINT,
_powerup_amount=1
)

#Create ui text
createObject(
_x=50,
_y=50,
_z=9,
_font_id=ID_FONT_CIRNO,
_font_text="Points: $x / $x",
_font_color=(255,255,255),
_font_aa=True,
_font_replaces=[points, points_goal]
)

#Create ui text
createObject(
_x=50,
_y=75,
_z=9,
_font_id=ID_FONT_CIRNO,
_font_text="Life: $x",
_font_color=(255,255,255),
_font_aa=True,
_font_replaces=[life]
)

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

                    # ignore self
                    if obs == obj:
                        continue

                    # collision check
                    if collide[obs]:
                        if on[obs]: # only on rendered 
                            
                            # calculate mask offset for next frame
                            next_off_x = x[obs] - next_x
                            next_off_y = y[obs] - next_y

                            # check overlapping points in both x and y axis
                            collision_flag_x = checkCollision(obj, obs, offx=next_off_x)
                            collision_flag_y = checkCollision(obj, obs, offy=next_off_y)
            
            # if there's no collision then update the position
            if not collision_flag_x:
                x[obj] = next_x
            if not collision_flag_y:
                y[obj] = next_y

    #Check if you have enough points to get a life
    if points.get_value() >= points_goal.get_value():
        points_goal.mul_value(2)
        life.add_value(1)
        

    #Manage powerups
    for obj1 in range(OBJECT_COUNT_MAX):
        if powerup[obj1] != None: # if it is a powerup

            if on[obj1]: # only on rendered powerups

                for obj2 in range(OBJECT_COUNT_MAX):
                    if powerup_pickup[obj2]: # get pickup obj

                        #check collision to see if picked up
                        if checkCollision(obj1, obj2):

                            #POINTS POWERUP
                            if powerup[obj1] == POWERUP_POINT:
                                points.add_value(powerup_amount[obj1])
                            
                            #CLEAR POWERUP
                            deleteObject(obj1)

                            #Create powerup [debug]
                            createObject(
                            _x=random.randrange(400,700),
                            _y=random.randrange(350,500),
                            _z=3,
                            _texture_id=ID_TEXTURE_POINT,
                            _powerup=POWERUP_POINT,
                            _powerup_amount=1
                            )

    #Render system
    WINDOW.fill(WINDOW_FILL_COLOR)  # clear

    for _z in range(Z_LAYER_COUNT): # sort z layer
        for obj in range(OBJECT_COUNT_MAX): # loop objects
            if z[obj] == _z:                    # if both on same z layer
                if on[obj]:                         # if on

                    if font_id[obj] == None:
                        WINDOW.blit(texture[texture_id[obj]], (x[obj], y[obj])) # render object
                    else:

                        temp = font_text[obj]
                        
                        for i in range(len(font_replaces[obj])): #replace all var placeholder occurrencies
                            temp = temp.replace(FONT_VAR_PLACEHOLDER, str(font_replaces[obj][i].get_value()),1)

                        WINDOW.blit( font[font_id[obj]].render(temp,font_aa[obj],font_color[obj]) , (x[obj], y[obj])) # render font
                        
    
    pygame.display.flip()   # update

#On game close, call pygame.quit
pygame.quit()
