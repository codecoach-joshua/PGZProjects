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

# global variables to track when to move the tank
moving_up = False
moving_down = False
moving_left = False
moving_right = False

# global variable for setting movement speed of the tank
tank_speed = 5

# missile image for projectiles
missile = Actor("missile")
# cooldown setting for how long to wait between shots (in frames)
shotCooldown = 45
# cooldown timer for when to shoot
cooldownTimer = 0
# speed setting for how fast the missile moves across the screen (pixels/second)
missileSpeed = 900 
# track when animation is currently active in the game
missileAnimation = None #start out with no animation

#### GLOBAL VARIABLES FOR THE GAME CODE ####

def on_mouse_down(pos):
    global missileAnimation, cooldownTimer

    # check timer if player is allowed to shoot
    if cooldownTimer <= 0:
        # set cooldown
        cooldownTimer = shotCooldown

        # reset missile position to tank
        missile.pos = tank.pos

        # have missile point towards the mouse
        angle = missile.angle_to(pos)
        missile.angle = angle

        # calculate the time it will take for the missile to travel to target
        distance = missile.distance_to(pos)
        time = distance / missileSpeed

        # update animation variable for missile
        missileAnimation = animate(missile, pos=pos, duration=time)

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
    global cooldownTimer
    
    # update cooldown
    if cooldownTimer > 0:
        cooldownTimer -= 1
        
    if moving_up:
        tank.y -= tank_speed
        
    if moving_down:
        tank.y += tank_speed
        
    if moving_left:
        tank.x -= tank_speed
        
    if moving_right:
        tank.x += tank_speed

    #only handle missile's collision if there is an animation active and running
    if missileAnimation and missileAnimation.running:
        pass # TODO in part 3

def draw():
    # white background
    screen.fill("white") 

    #draw tank
    tank.draw()

    #draw crosshair
    crosshair.draw()

    #only draw missile if there is an animation active and running
    if missileAnimation and missileAnimation.running:
        missile.draw()

pgzrun.go()
