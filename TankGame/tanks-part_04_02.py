import pgzrun
from random import random
from math import cos, sin
from pygame import mixer

mixer.init()
mixer.music.load('sounds/explosion.mp3')

# class for basic enemy that follows after a target (ie, the player)
class FollowingEnemy:
    def __init__(self, actor, velocity=2):
        # image data
        self.actor = actor
        # movement data
        self.totalVelocity = velocity
        # track whether or not enemy is still active
        self.alive = True

    # checks actor's collision with point on screen
    def collidepoint(self, point):
        return self.alive and self.actor.collidepoint(point)
            
    def update(self, target):
        # only move if still alive
        if self.alive:
            # re-orient enemy towards target
            angleDegrees = self.actor.angle_to(target)
            self.actor.angle = angleDegrees
            
            # calculate movement in the x and y direction
            radians = angleDegrees * 3.14 / 180.0
            vx = cos(radians) * self.totalVelocity
            vy = -sin(radians) * self.totalVelocity

            # update position
            self.actor.x += vx
            self.actor.y += vy

    def draw(self):
        # only draw if still alive
        if self.alive:
            self.actor.draw()

# class for handling explosions that exist for a short time
class Explosion:
    def __init__(self, actor, lifetime=40):
        #image data
        self.actor = actor
        #time in frames explosion lasts
        self.lifetime = lifetime

    #collision detection
    def collidepoint(self, point):
        return self.lifetime > 0 and self.actor.collidepoint(point)

    def update(self):
        #countdown lifetime
        if self.lifetime > 0:
            self.lifetime -= 1

    def draw(self):
        #only draw active explosions
        if self.lifetime > 0:
            self.actor.draw()
            
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

# crosshair image to show where the tank is aiming
crosshair = Actor("crosshair")

# global variables to track when to move the tank
moving_up = False
moving_down = False
moving_left = False
moving_right = False

# setting movement speed of the tank
tank_speed = 5

# missile image for projectiles
missile = Actor("missile")
# cooldown setting for how long to wait between shots (in frames)
shotCooldown = 45
# cooldown timer for when to shoot
cooldownTimer = 0
# speed setting for how fast the missile moves across the screen (pixels/second)
missileSpeed = 800 
# track when animation is currently active in the game
animation = None #start out with no animation

# list to keep track of enemies in game
enemyList = []

# track the player's score
score = 0

# list to track explosions in game
explosionList = []

#### GLOBAL VARIABLES FOR THE GAME CODE ####

def on_mouse_down(pos):
    global animation, cooldownTimer

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
        animation = animate(missile, pos=pos, duration=time)

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
    global cooldownTimer, gameover, score

    # only update the game when not gameover
    if not gameover:
        # update enemies in list
        for enemy in enemyList:
            # check collision with missile if animation is running
            if animation:
                if animation.running:
                    if enemy.collidepoint(missile.pos):
                        #add to score
                        score += 100
                        #set enemy dead
                        enemy.alive = False
                        #stop missile animation
                        animation.running = False
                        #add explosion
                        actor = Actor("explosion", pos=(missile.pos))
                        explosionList.append(Explosion(actor))
                        #play sound effect
                        mixer.music.play(-1)
                        
            # only update active enemies
            if enemy.alive:
                enemy.update(tank.pos)
                # check collision with tank
                if tank.collidepoint(enemy.actor.pos):
                    gameover = True
                    break

        # loop through explosions
        for explosion in explosionList:
            explosion.update()
            #check enemies
            for enemy in enemyList:
                if explosion.collidepoint(enemy.actor.pos):
                    enemy.alive = False
                    score += 100
        
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
            
def draw():
    # white background
    screen.fill("white")
    
    # draw enemies in list
    for enemy in enemyList:
        enemy.draw()
        
    for explosion in explosionList:
        #draw explosion
        explosion.draw()

    #draw tank
    tank.draw()

    #draw crosshair
    crosshair.draw()

    #only draw missile if its animation is active and running
    if animation:
        if animation.running:
            missile.draw()

    # draw game over text when end of game
    if gameover:
        screen.draw.text("GAME OVER", pos=(WIDTH/3, HEIGHT/2),
                          fontsize=50, color="red")

    screen.draw.text("Score: " + str(score), pos=(25, 25),
                          fontsize=30, color="green")

# spawn a new enemy at a random location a set distance away from the player
def spawn_enemy(distance = 500):
    # calculate a random angle (in radians) to spawn away from the player
    angle = random() * 3.14

    # calculate spawn point
    delta_x = cos(angle) * distance
    delta_y = -sin(angle) * distance
    spawn_point = (tank.x + delta_x, tank.y + delta_y)

    # create new actor at the spawn point
    newActor = Actor("zombie", pos=spawn_point)

    # create enemy and at it to list
    enemyList.append(FollowingEnemy(newActor))

clock.schedule_interval(spawn_enemy, 1) #spawn an enemy every second

pgzrun.go()
