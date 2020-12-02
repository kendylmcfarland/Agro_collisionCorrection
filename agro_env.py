import pygame
import math
import numpy as np
from pygame.math import Vector2

obs = [((0,0),(0,750)), ((0,0),(700,0)), ((700,0),(700,750)), ((0,750),(700,750)), ((50,100),(100,50)), ((150,350),(200,400)), ((70,450),(100,450)), ((100,450),(100,475)), ((250,300),(500,300)), ((250,500),(500,500)), ((250,300),(250,500)), ((500,300),(500,500)), ((40,720),(60,680)), ((270,550),(270,600)), ((620,700),(680,600)), ((600,400),(650,400)), ((600,450),(600,400)), ((650,400),(650,450))]

achange = 0

def drawagro(a,b,c):
    pygame.draw.line(screen, WHITE, a, b, 3)
    pygame.draw.line(screen, RED, b, c, 3)

def intersect(p1,p2,p3,p4):
    global achange
    (x1,y1) = p1
    (x2,y2) = p2
    (x3,y3) = p3
    (x4,y4) = p4
    if max(x1,x2) < min(x3,x4):
        return False
    if x1-x2 == 0: m1 = 0
    else: m1 = (y1-y2)/(x1-x2)
    if x3-x4 == 0: m2 = 0
    else: m2 = (y3-y4)/(x3-x4)
    b1 = y1-m1*x1
    b2 = y3-m2*x3
    if m1 == m2 and b1 == b2:
        return True #on top of each other
    elif m1 == m2:
        return False #parallel lines
    if m1-m2 == 0: xa = 0
    else: xa = (b2-b1)/(m1-m2)
    # ya = m1 *xa +b1
    # ya = m2 *xa +b2
    if((xa < max(min(x1,x2), min(x3,x4))) or (xa > min(max(x1,x2),max(x3,x4)))):
        return False #intersection out of bounds
    else:
        achange = np.arctan((m2-m1)/(1+m2*m1))
        return True

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

PI = 3.141592653
 
# Set the height and width of the screen
size = (700, 750)
screen = pygame.display.set_mode(size)
#player = Player((10,10))
#playersprite = pygame.sprite.RenderPlain((player))
 
pygame.display.set_caption("Agro Environment")
 
# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
framerate=100
dt=1/framerate

l = 18
d = 9
vel = 0
angle = 0
angle2 = 0
x_coord = 10
y_coord = 10

while not done:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                angle += -0.1
            elif event.key == pygame.K_RIGHT:
                angle += 0.1
            elif event.key == pygame.K_UP:
                vel += 1
            elif event.key == pygame.K_DOWN:
                vel -= 1
    
    vel = np.clip(vel, -50, 50)
    angle = np.clip(angle, -np.pi, np.pi)

    ######################################
    angle2dot = 2*(vel * np.sin(angle))/l
    angle2 += angle2dot*dt
    xdot = vel * np.cos(angle2)
    ydot = vel * np.sin(angle2)

    # if (x_coord + xdot)
    x_coord = np.clip((x_coord+xdot*dt), 0, 700)
    y_coord = np.clip((y_coord+ydot*dt), 0, 750)

    a = (x_coord,y_coord)
    b = (x_coord+l*np.cos(angle2), y_coord+l*np.sin(angle2))
    c = (x_coord+l*np.cos(angle2)+d*np.cos(angle2+angle), y_coord+l*np.sin(angle2)+d*np.sin(angle+angle2))

    dist = (vel**2)/(2*9.81*.8)
    p_x = dist * np.cos(angle2)
    p_y = dist * np.cos(angle2)

    for (p1,p2) in obs:
        if intersect(a,b,p1,p2)==True:
            print("You crashed agro")
            print("vel= {}, angle= {}".format(vel, achange))
            done = True
        elif intersect(a,(p_x,p_y),p1,p2)==True:
            print("You were about to crash")
            vel = 0

    # if crash(x_coord,y_coord)==True:
    #     print("You crashed agro!")
    #     print("x={}, y={}".format(x_coord,y_coord))
    #     done = True

    screen.fill(BLACK)

    drawagro(a,b,c)
 
    # Draw obstacles
    for (p1,p2) in obs:
        pygame.draw.line(screen, GREEN, p1, p2, 5)

    pygame.display.flip()
 
    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(framerate)
 
# Be IDLE friendly
pygame.quit()