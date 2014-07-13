#!/usr/bin/python3

version = 0.2

#############################################################
# This monstrosity was created by crash_horror (373vFS_Crash)
# and comes without warranty of any kind,
# read the licence at the bottom.
# (https://github.com/crash-horror)
#############################################################

import pygame
import sys
import math
from pygame.locals import *


# a bunch of colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
lime = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
silver = (192, 192, 192)
gray = (128, 128, 128)
darkgray = (20, 20, 20)
verydarkgray = (10, 10, 10)
maroon = (128, 0, 0)
olive = (128, 128, 0)
green = (0, 128, 0)
purple = (128, 0, 128)
teal = (0, 128, 128)
navy = (0, 0, 128)
ground = (84, 53, 10)
sky = (0, 76, 255)


pygame.init()

fpsTime = pygame.time.Clock()
fps = 20
bg = black
dispWidth = 800
dispHeight = 800
step_distance = 5
step_bearing = 5
xyDIV = 1
scalenumber = 25


myBRA = [0, 0]
enemyBRA = [0, 0]


def setscale(_myBRA, _enemyBRA):
    global xyDIV, step_distance, scalenumber
    my_distance = _myBRA[1]
    enemy_distance = _enemyBRA[1]
    if my_distance < 26 and enemy_distance < 26:
        xyDIV = 12
        step_distance = 1
        scalenumber = 25
    elif my_distance < 51 and enemy_distance < 51:
        xyDIV = 6
        step_distance = 1
        scalenumber = 50
    elif my_distance < 101 and enemy_distance < 101:
        xyDIV = 3
        step_distance = 2
        scalenumber = 100
    elif my_distance < 201 and enemy_distance < 201:
        xyDIV = 1.5
        step_distance = 5
        scalenumber = 200
    else:
        xyDIV = 1
        step_distance = 5
        scalenumber = 400


def getdistance(myPOS, enemyPOS):
    distance = math.sqrt((myPOS[0] - enemyPOS[0])**2 + (myPOS[1] - enemyPOS[1])**2)
    return int(distance)


def getbearing(myPOS, enemyPOS):
    dx = enemyPOS[0] - myPOS[0]
    dy = enemyPOS[1] - myPOS[1]
    rads = math.atan2(dy, dx)
    rads %= 2*math.pi
    degs = math.degrees(rads)
    degs += 90
    if degs >= 360:
        degs = degs-360
    return int(degs)


def drawbearing(_bearing):
    phi = math.radians(_bearing-90)
    x = 400 + 240 * math.cos(phi)
    y = 350 + 240 * math.sin(phi)

    pygame.draw.aaline(setDisplay, yellow, (400, 350), (x, y))
    pygame.draw.circle(setDisplay, yellow, (int(x), int(y)), 5)


class Bulls:
    """My first attempt in classses so: wtf shit dammit"""

    def __init__(self, dotcolor=black):
        self.BRA = [0, 0]
        self.dotcolor = dotcolor

    def position(self):
        bearing = self.BRA[0]
        distance = self.BRA[1]
        phi = math.radians(bearing-90)

        x = distance * math.cos(phi)
        y = distance * math.sin(phi)

        self.drawposition(x, y)
        return [int(x), int(y)]

    def drawposition(self, x, y):
        xdraw = x * xyDIV
        ydraw = y * xyDIV
        pygame.draw.circle(setDisplay, self.dotcolor, (int(xdraw + dispWidth/2), int(ydraw + dispHeight/2)-50), 10)


def runMainLoop():
    global myBRA, enemyBRA, step_bearing
    while True:
        for event in pygame.event.get():
            # print(event) # <<------------ debug fossil
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # reset button press
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if resetbuttonRECT.collidepoint(pos):
                    myBRA = [0, 0]
                    enemyBRA = [0, 0]

        # step button press
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if stepbuttonRECT.collidepoint(pos):
                    if step_bearing == 5:
                        step_bearing =1
                    else:
                        step_bearing = 5

        # mousewheel UP
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                pos = pygame.mouse.get_pos()
            # bearing up
                if mybearingRECT.collidepoint(pos):
                    myBRA[0] += step_bearing
                    if myBRA[0] >= 360:
                        myBRA[0] -= 360
                if enemybearingRECT.collidepoint(pos):
                    enemyBRA[0] += step_bearing
                    if enemyBRA[0] >= 360:
                        enemyBRA[0] -= 360
            # distance up
                if mydistanceRECT.collidepoint(pos):
                    myBRA[1] += step_distance
                if enemydistanceRECT.collidepoint(pos):
                    enemyBRA[1] += step_distance

        # mousewheel DOWN
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                pos = pygame.mouse.get_pos()
            # bearing down
                if mybearingRECT.collidepoint(pos):
                    myBRA[0] -= step_bearing
                    if myBRA[0] < 0:
                        myBRA[0] = 360 + myBRA[0]
                if enemybearingRECT.collidepoint(pos):
                    enemyBRA[0] -= step_bearing
                    if enemyBRA[0] < 0:
                        enemyBRA[0] = 360 + enemyBRA[0]

            # distance down
                if mydistanceRECT.collidepoint(pos):
                    myBRA[1] -= step_distance
                    if myBRA[1] < 0:
                        myBRA[1] = 0
                if enemydistanceRECT.collidepoint(pos):
                    enemyBRA[1] -= step_distance
                    if enemyBRA[1] < 0:
                        enemyBRA[1] = 0

    # start drawing stuff
        setDisplay.fill(bg)
        setDisplay.blit(ring, (100, 50))
        setDisplay.blit(logo, (720, 20))

    # set the scale
        setscale(myBRA, enemyBRA)

    # scale label
        setDisplay.blit(scalelabelTXT, (405, 275))
        scalenumberTXT = hugefont.render(str(scalenumber), True, darkgray)
        setDisplay.blit(scalenumberTXT, (405, 340))

    # draw reset button
        resetbuttonRECT = pygame.draw.rect(setDisplay, darkgray, ((10, 550), (110, 55)))
        setDisplay.blit(resetbuttonTXT, (15, 545))

    # draw step button
        stepbuttonRECT = pygame.draw.rect(setDisplay, darkgray, ((680, 550), (110, 55)))
        setDisplay.blit(stepbuttonTXT, (695, 545))
        stepnumberTXT = hugefont.render(str(step_bearing), True, darkgray)
        setDisplay.blit(stepnumberTXT, (715, 475))

    # draw info line
        setDisplay.blit(infoTXT1, (20, 20))
        setDisplay.blit(infoTXT2, (23, 45))

    # draw bullseye title
        setDisplay.blit(infoTXT3, (300, 315))
        setDisplay.blit(infoTXT4, (280, 350))

    # position logic calls
        myplane.BRA = myBRA
        myPOS = myplane.position()

        enemyplane.BRA = enemyBRA
        enemyPOS = enemyplane.position()

        distance = getdistance(myPOS, enemyPOS)
        bearing = getbearing(myPOS, enemyPOS)

    # draw bearing line
        drawbearing(bearing)

    # draw center stub circle
        pygame.draw.circle(setDisplay, black, (400, 350), 5)

    # very dark grey face
        pygame.draw.rect(setDisplay, verydarkgray, ((10, 700), (780, 90)))

    # my plane data rects
        mybearingRECT = pygame.draw.rect(setDisplay, darkgray, ((10, 700), (125, 90)))
        mydistanceRECT = pygame.draw.rect(setDisplay, darkgray, ((135, 700), (125, 90)))

    # enemy plane data rects
        enemybearingRECT = pygame.draw.rect(setDisplay, darkgray, ((540, 700), (125, 90)))
        enemydistanceRECT = pygame.draw.rect(setDisplay, darkgray, ((665, 700), (125, 90)))

    # my plane numbers
        mybearingTXT = largeboldfont.render(str(myBRA[0]), True, cyan)
        setDisplay.blit(mybearingTXT, (50, 720))
        mydistanceTXT = largeboldfont.render(str(myBRA[1]), True, cyan)
        setDisplay.blit(mydistanceTXT, (150, 720))

    # enemy numbers
        enemybearingTXT = largeboldfont.render(str(enemyBRA[0]), True, red)
        setDisplay.blit(enemybearingTXT, (580, 720))
        enemydistanceTXT = largeboldfont.render(str(enemyBRA[1]), True, red)
        setDisplay.blit(enemydistanceTXT, (680, 720))

    # pilot info results
        bearingTXT = largeboldfont.render(str(bearing), True, white)
        setDisplay.blit(bearingTXT, (300, 720))

        distanceTXT = largeboldfont.render(str(distance), True, white)
        setDisplay.blit(distanceTXT, (420, 720))

    # small labels
        setDisplay.blit(bearinglabelTXT, (50, 770))
        setDisplay.blit(distancelabelTXT, (150, 770))

        setDisplay.blit(bearinglabelTXT, (300, 770))
        setDisplay.blit(distancelabelTXT, (420, 770))

        setDisplay.blit(bearinglabelTXT, (580, 770))
        setDisplay.blit(distancelabelTXT, (680, 770))

    # large labels
        setDisplay.blit(youlabelTXT, (90, 625))
        setDisplay.blit(banditlabelTXT, (570, 625))

        # print('me=', myPOS, 'enemy=', enemyPOS, 'distance=', distance, 'bearing=', bearing) # <<-- DEBUG fossil
        pygame.display.update()
        fpsTime.tick(fps)

# ---------------------------------------------------


# setup
icon = pygame.image.load('64roundel.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('"Λαμόγιας" BullsEye Calculator v' + str(version))
setDisplay = pygame.display.set_mode((dispWidth, dispHeight))


# images
logo = pygame.image.load('373top.jpg')
ring = pygame.image.load('ring_grey_lines.png')


# fonts
largeboldfont = pygame.font.SysFont("tahoma", 45)
labelfont = pygame.font.SysFont("tahoma", 15)
hugefont = pygame.font.SysFont("tahoma", 65)
ingofont = pygame.font.SysFont("tahoma", 25)


# text
bearinglabelTXT = labelfont.render('bearing', True, gray)
distancelabelTXT = labelfont.render('distance', True, gray)

scalelabelTXT = hugefont.render('scale', True, darkgray)

youlabelTXT = hugefont.render('me', True, darkgray)
banditlabelTXT = hugefont.render('bandit', True, darkgray)

resetbuttonTXT = largeboldfont.render('reset', True, black)
stepbuttonTXT = largeboldfont.render('step', True, black)

infoTXT1 = ingofont.render('use mouse wheel', True, darkgray)
infoTXT2 = ingofont.render('to change values', True, darkgray)

infoTXT3 = ingofont.render('BullsEye', True, darkgray)
infoTXT4 = ingofont.render('Calculator', True, darkgray)


# objects
myplane = Bulls(cyan)
enemyplane = Bulls(red)


# run the thing
runMainLoop()


# notes
# -------------------------------------------------------
"""
cx_freeze switch:
--base-name=Win32GUI
"""


# licence
# -------------------------------------------------------
"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>
"""
