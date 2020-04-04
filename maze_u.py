import pygame, random, sys
from pygame.locals import *

import numpy as np

from time import time,sleep
from random import randint as r


pygame.init()

window_height = 900
window_width = 900

blue = (0, 255, 255)
black = (0, 0, 0)
white = (0, 0, 255)

def terminate():        # to end the program
    pygame.quit()
    sys.exit()


def load_image(imagename):
    return pygame.image.load(imagename)

def waitforkey():
    while True :                                        # to wait for user to start
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:     # to terminate if the user presses the escape key
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return

def drawtext(text, font, surface, x, y):        # to display text on the screen
    textobj = font.render(text, 1, blue)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

mainClock = pygame.time.Clock()
Canvas = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Artificial Intelligence')

font = pygame.font.SysFont("Times new Roman", 48)

startimage = load_image('maze2.png')
startimagerect = startimage.get_rect()
startimagerect.centerx = window_width/2
startimagerect.centery = window_height/2

pygame.mixer.music.load('mario_theme.wav')
gameover = pygame.mixer.Sound('mario_dies.wav')
pygame.mixer.music.play(-1, 0.0)

Canvas.blit(startimage, startimagerect)
drawtext('Maze You', font, Canvas, (window_width/3 + 50), (window_height/5))
drawtext('Click any button to continue', font, Canvas, (window_width/3.3 - 100), (window_height/1.5))

pygame.display.update()
waitforkey()
   
#--------------------------------------------------------------------------------------------------------
n = 9  #represents no. of side squares(n*n total squares)
scrx = n*100
scry = n*100
background = (0,0,0) #used to clear screen while rendering
screen = pygame.display.set_mode((scrx,scry)) #creating a screen using Pygame
colors = [(0,0,0) for i in range(n**2)] 
reward = np.zeros((n,n))
terminals = []
penalities = 10
while penalities != 0:
    i = r(0,n-1)
    j = r(0,n-1)
    if reward[i,j] == 0 and [i,j] != [0,0] and [i,j] != [n-1,n-1]:
        reward[i,j] = -1
        penalities-=1
        colors[n*i+j] = (255,0,255)
        terminals.append(n*i+j)
reward[n-1,n-1] = 1
colors[n**2 - 1] = (255,255,0)
terminals.append(n**2 - 1)


Q = np.zeros((n**2,4)) #Initializing Q-Table
actions = {"up": 0,"down" : 1,"left" : 2,"right" : 3} #possible actions
states = {}
k = 0
for i in range(n):
    for j in range(n):
        states[(i,j)] = k
        k+=1
alpha = 0.01
gamma = 0.9
#-----------
current_pos = [0,0]
#---------
epsilon = 0.25



def select_action(current_state):
    global current_pos,epsilon
    possible_actions = []
    if np.random.uniform() <= epsilon:
        if current_pos[0] != 0:
            possible_actions.append("up")
        if current_pos[0] != n-1:
            possible_actions.append("down")
        if current_pos[1] != 0:
            possible_actions.append("left")
        if current_pos[1] != n-1:
            possible_actions.append("right")
        action = actions[possible_actions[r(0,len(possible_actions) - 1)]]
    else:
        m = np.min(Q[current_state])
        if current_pos[0] != 0: #up
            possible_actions.append(Q[current_state,0])
        else:
            possible_actions.append(m - 100)
        if current_pos[0] != n-1: #down
            possible_actions.append(Q[current_state,1])
        else:
            possible_actions.append(m - 100)
        if current_pos[1] != 0: #left
            possible_actions.append(Q[current_state,2])
        else:
            possible_actions.append(m - 100)
        if current_pos[1] != n-1: #right
            possible_actions.append(Q[current_state,3])
        else:
            possible_actions.append(m - 100)
        action = random.choice([i for i,a in enumerate(possible_actions) if a == max(possible_actions)]) #randomly selecting one of all possible actions with maximin value
    return action
      
      
def episode():
    global current_pos,epsilon
    current_state = states[(current_pos[0],current_pos[1])]
    action = select_action(current_state)
    if action == 0: #move up
        current_pos[0] -= 1
    elif action == 1: #move down
        current_pos[0] += 1
    elif action == 2: #move left
        current_pos[1] -= 1
    elif action == 3: #move right
        current_pos[1] += 1
    new_state = states[(current_pos[0],current_pos[1])]
    if new_state not in terminals:
        Q[current_state,action] += alpha*(reward[current_pos[0],current_pos[1]] + gamma*(np.max(Q[new_state])) - Q[current_state,action])
    else:
        Q[current_state,action] += alpha*(reward[current_pos[0],current_pos[1]] - Q[current_state,action])
        current_pos = [0,0]
        if epsilon > 0.05:
            epsilon -= 3e-4 #reducing as time increases to satisfy Exploration & Exploitation Tradeoff
            
            
            
def layout():
    c = 0
    for i in range(0,scrx,100):
        for j in range(0,scry,100):
            pygame.draw.rect(screen,(0,0,255),(j,i,j+100,i+100),0)
            pygame.draw.rect(screen,colors[c],(j+3,i+3,j+95,i+95),0)
            c+=1
            pygame.draw.circle(screen,(25,129,230),(current_pos[1]*100 + 50,current_pos[0]*100 + 50),30,10)
run = True

while run:
    # sleep(0.3)
    screen.fill(background)
    layout()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
    episode()
#pygame.quit()
pygame.mixer.music.stop()





