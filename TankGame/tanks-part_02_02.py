import pgzrun

#### GLOBAL VARIABLES FOR THE GAME CODE ####

# setup screen size
WIDTH = 800
HEIGHT = 600

# tank image for the main player
tank = Actor("tank")
# position to start in center of screen
tank.pos=(WIDTH/2, HEIGHT/2)

# crosshair image to show where the tank is aiming
crosshair = Actor("crosshair")

# position to start in center of screen
gameover = False

# global variables to track when to move the tank
moving_up = False
moving_down = False
moving_left = False
moving_right = False

# global variable for setting movement speed of the tank
tank_speed = 5

#### GLOBAL VARIABLES FOR THE GAME CODE ####

def on_mouse_move(pos):
    # calculate angle
    angle = tank.angle_to(pos)
    # set orientation of tank
    tank.angle = angle

    #update crosshair's position
    crosshair.pos = pos

def on_key_down(key):
    global moving_up, moving_down
    global moving_left, moving_right

    # set global variables to True when the key is being pressed down
    if key == keys.W:
        moving_up = True
    elif key == keys.S:
        moving_down = True
    elif key == keys.A:
        moving_left = True
    elif key == keys.D:
        moving_right = True

def on_key_up(key):
    global moving_up, moving_down
    global moving_left, moving_right
    
    # set global variables to False when the key is being pressed down
    if key == keys.W:
        moving_up = False
    elif key == keys.S:
        moving_down = False
    elif key == keys.A:
        moving_left = False
    elif key == keys.D:
        moving_right = False

def update():
    # only update the game when not gameover
    if not gameover:
        if moving_up:
            tank.y -= tank_speed
            
        if moving_down:
            tank.y += tank_speed
            
        if moving_left:
            tank.x -= tank_speed
            
        if moving_right:
            tank.x += tank_speed

def draw():
    # white background
    screen.fill("white") 

    #draw tank
    tank.draw()

    #draw crosshair
    crosshair.draw()
    
    # draw game over text when end of game
    if gameover:
        screen.draw.text("GAME OVER", pos=(WIDTH/3, HEIGHT/2),
                          fontsize=50, color="red")

pgzrun.go()
