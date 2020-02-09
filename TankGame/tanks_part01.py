import pgzrun

#### GLOBAL VARIABLES FOR THE GAME CODE ####

# setup screen size
WIDTH = 800
HEIGHT = 600

# tank image for the main player
tank = Actor("tank")
# position to start in center of screen
tank.pos=(WIDTH/2, HEIGHT/2)

# position to start in center of screen
gameover = False

#### GLOBAL VARIABLES FOR THE GAME CODE ####

def update():
    # only update the game when not gameover
    if not gameover:
        pass # will add in section 2

def draw():
    # white background
    screen.fill("white") 
    # draw tank
    tank.draw()
    # draw game over text when end of game
    if gameover:
        screen.draw.text("GAME OVER", pos=(WIDTH/3, HEIGHT/2),
                          fontsize=50, color="red")


pgzrun.go()
