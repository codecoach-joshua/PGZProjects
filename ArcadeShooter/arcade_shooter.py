import pgzrun
from random import randint

# adjust screen size
WIDTH = 600
HEIGHT = 400

#custom function for creating random x, y coordinate on screen
def randomPosition():
    # fit within screen space
    x = randint(50, WIDTH - 50) 
    y = randint(50, HEIGHT - 50)
    return (x,y)

# crosshair for mouse
crosshair = Actor("crosshair")

# target set to random starting position
target = Actor("target", pos = randomPosition())

# message for hits and misses (start out as "None" until first shot attempt)
message = None
messageColor = None

messageBox = None
messageAnimation = None

# track game data
score = 0
timer = 30

# data for ranges and points
yellow_range = 12.5
red_range = 25.0
blue_range = 37.5
white_range = 50.0

yellow_points = 15
red_points = 10
blue_points = 5
white_points = 3
black_points = 1

# global data to track animation 
animation = animate(target, pos = randomPosition(), duration = 1)

# function to reset target by providing new position and animation
def resetTarget():
    global animation

    # stop any previous animation
    animation.running = False

    # provide new position and animation
    target.pos = randomPosition()
    animation = animate(target, pos = randomPosition(), duration = 1)

def updateMessage(hitTarget, points, location):
    global message, messageColor, messageBox, messageAnimation

    x, y = location

    if hitTarget:
        message = "HIT! +" + str(points)
        messageColor = "white"
    else:
        message = "MISS! " + str(points)
        messageColor = "red"

    messageBox = Rect(x, y, 80, 20)

def on_mouse_move(pos):
    # have crosshair image follow mouse
    crosshair.pos = pos

def on_mouse_down(pos):
    global score

    if timer > 0:
        # check if mouse is colliding with target
        if target.collidepoint(pos):
            # calculate distance and check range
            distance = target.distance_to(pos)

            if distance < yellow_range:
                addedPoints = yellow_points
            elif distance < red_range:
                addedPoints = red_points
            elif distance < blue_range:
                addedPoints = blue_points
            elif distance < white_range:
                addedPoints = white_points
            else:
                addedPoints = black_points
                
            score += addedPoints
            #update message with hit
            updateMessage(True, addedPoints, pos)
            #reset target
            resetTarget()
        else:
            #subtract points for misses
            score -= 5
            #update message with miss
            updateMessage(False, -5, pos)

def update():
    global animation

    if timer == 0:
        animation.running = False
        message = None
    
    # check when animation is finished running
    elif not animation.running:
        # set animation to new object with new random destination
        animation = animate(target, pos = randomPosition(), duration = 1)

def draw():
    # refresh screen with blank color
    screen.fill("forest green")

    # draw actor
    target.draw()

    # draw crosshair
    crosshair.draw()

    # display score
    screen.draw.text("Score: " + str(score),
                     (25, 25),
                     fontsize=(30),
                     color="white")

    # display time
    screen.draw.text("Time: %02d" % timer,
                     (WIDTH-125, 25),
                     fontsize=(30),
                     color="white")

    # display message for hits and misses when available
    if message is not None:
        screen.draw.textbox(message, messageBox, color=messageColor)

# use clock to schedule event for decreasing timer
def decreaseTime():
    global timer

    if timer > 0:
        timer -= 1

clock.schedule_interval(decreaseTime, 1.0)

# launch game
pgzrun.go()
