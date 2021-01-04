from math import fabs, sqrt, cos, sin, pi, floor, ceil, e
from random import uniform, randint, choice
from datetime import datetime
import pygame

import threading

pygame.init()
fpsClock = pygame.time.Clock()

winWidth = 800
winHeight = 600
win = pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption('Simon\'s graph')

pygame.font.init()
myFont = pygame.font.Font("fonts\pixelFont.ttf", 12)

scaleFactor = 100
################################################################################ transformations

cam = (0,0)
def param(pos):
	return (int(pos[0] * scaleFactor + winWidth/2 - cam[0]), int(pos[1] * scaleFactor + winHeight/2 - cam[1]))

def parami(pos):
	return ((pos[0] - winWidth/2 + cam[0]) / scaleFactor ,(pos[1] - winHeight/2 + cam[1]) / scaleFactor)
################################################################################ Vector math
def vecAdd(v1, v2):
	return (v1[0] + v2[0], v1[1] + v2[1])
def vecSub(v1, v2):
	return (v1[0] - v2[0], v1[1] - v2[1])
def vecMult(v, s):
	return (v[0] * s, v[1] * s)
	
################################################################################ Complex math
def mult(one, two):
	return (one[0]*two[0] - one[1]*two[1], one[0]*two[1] + one[1]*two[0])
	
def smult(one, scalar):
	return (one[0] * scalar, one[1] * scalar)
	
def add(one, two):
	return (one[0] + two[0], one[1] + two[1])
	
def div(one, two):
	den = two[0]*two[0] + two[1]*two[1]
	return ((one[0]*two[0] + one[1]*two[1])/den, (-one[0]*two[1] + one[1]*two[0])/den)

def cabs(one):
	return sqrt(one[0]*one[0] + one[1]*one[1])

def drawPoint(pos):
	pygame.draw.circle(win, (255,0,0) , param((pos[0],pos[1])) ,2)

upLeft = None
downRight = None

def closestFive(x):
	return 5 * round(x / 5)

def upLeft():
	return parami((0,0))
def downRight():
	return parami((winWidth,winHeight))

def setCam(pos):
	global cam
	cam = (pos[0] * scaleFactor, -pos[1] * scaleFactor)

################################################################################ function example

EXPLORE = 0
MAKEFULL = 1

mode = EXPLORE

mandelSurf = pygame.Surface(win.get_size())
mandelSubInit = 4
mandelSub = mandelSubInit

# parameters for mandelNormal
h2 = 1.5
angle = 45+180
v = (cos((angle * 2 * pi)/360), sin((angle * 2 * pi)/360))
RADIUS = 100

maxIterations = 100
maxIterationsSurf = myFont.render("iterations: " + str(maxIterations), False, (255,255,255))

finished = False

def smap(value,a,b,c,d):
	return (value - a)/(b - a) * (d - c) + c

def mandelColor(pos):
	a = pos[0]
	b = pos[1]
	
	ca = a
	cb = b
	
	iteration = 0
	while iteration < maxIterations:
		aa = a*a - b*b
		bb = 2*a*b

		a = aa + ca
		b = bb + cb
		
		if fabs(aa + bb) > 4:# 16
			break
		
		iteration += 1
	
	# bright = smap(iteration, 0, maxIterations, 0, 1)
	# bright = smap(sqrt(bright), 0,1,0,255)
	# if iteration == maxIterations:
		# bright = 0
	
	f = 0.1
	red = (0.5 * sin(f * iteration) + 0.5) * 255
	green = (0.5 * sin(f * iteration + 2.094) + 0.5) * 255
	blue = (0.5 * sin(f * iteration + 4.188) + 0.5) * 255
	return(red, green, blue)	
	return (bright, bright, bright)
	
def mandelNormal(pos):
	a = pos[0]
	b = pos[1]
	
	c = (a, b)
	z = (a, b)
	dc = (1, 0)
	der = (1, 0)
	iteration = 0
	
	reason = 0#not enough
	
	while iteration < maxIterations:

		new_z = add(mult(z,z), c) 
		new_der = add(mult(smult(der, 2), z), dc)
		z = (new_z[0], new_z[1])
		der = (new_der[0], new_der[1])
		
		if sqrt(z[0]*z[0] + z[1]*z[1]) > RADIUS*RADIUS:
			reason = 1
			break
		
		iteration += 1
	
	if reason == 0:
		bright = 0
	else:
		u = div(z, der)
		u = smult(u, 1/cabs(u))
		t = u[0]*v[0] + u[1]*v[1] + h2
		t = t/(1+h2)
		if t<0: t=0
		bright = t*255
	return (bright, bright, bright)

system = mandelColor

def mandelStep(box=None):
	# print("s")
	global mandelSub, mandelSurf
	
	mandelSurf = pygame.Surface((mandelSub, mandelSub))
	width = downRight()[0] - upLeft()[0]
	height = downRight()[1] - upLeft()[1]

	

	for hor in range(mandelSub):
		xSamp = upLeft()[0] + (width / mandelSub) * hor
		
		for ver in range(mandelSub):
			ySamp = upLeft()[1] + (height / mandelSub) * ver
			
			mandelSurf.set_at((hor, ver), system((xSamp,ySamp)))
	mandelSub += 5
	if mandelSub >= winWidth:
		mandelSub = winWidth

def mandelMake():
	global mandelSurf, finished
	
	totalSteps = winWidth * winHeight
	count = 0
	
	mandelSurf = pygame.Surface((winWidth, winHeight))
	width = downRight()[0] - upLeft()[0]
	height = downRight()[1] - upLeft()[1]

	for hor in range(winWidth):
		xSamp = upLeft()[0] + (width / winWidth) * hor
		
		for ver in range(winHeight):
			ySamp = upLeft()[1] + (height / winHeight) * ver
			
			mandelSurf.set_at((hor, ver), system((xSamp,ySamp)))
		
		# loading rect:
		count += winHeight
		ratio = count / totalSteps
		pygame.draw.rect(win, (0,255,0), ((0,0), (int(ratio * winWidth), 5)))
		pygame.display.update()
	
	finished = True
	print("fin")
	
	
############## threads:



################################################################################ Main Loop

mousePressed = False
run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			point = (pygame.mouse.get_pos()[0] / scaleFactor, pygame.mouse.get_pos()[1] / scaleFactor) 
			mousePressed = True
			camPrev = (cam[0], cam[1])
		# mouse control
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			mousePressed = False
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
			origin = param((0,0))
			mouse = pygame.mouse.get_pos()
			adjust = (mouse[0] - origin[0], mouse[1] - origin[1])
			cam = vecAdd(cam, vecMult(adjust, 0.2))
			scaleFactor += 0.2 * scaleFactor
			mandelSub = mandelSubInit
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
			origin = param((0,0))
			mouse = pygame.mouse.get_pos()
			adjust = (mouse[0] - origin[0], mouse[1] - origin[1])
			cam = vecSub(cam, vecMult(adjust, 0.2))
			scaleFactor -= 0.2 * scaleFactor
			mandelSub = mandelSubInit
		# keys pressed once
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_h:
				cam = (0,0)
				scaleFactor = 100
			if event.key == pygame.K_p:
				now = datetime.now()
				dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
				string = "gallery/mands/" + dt_string + ".png"
				pygame.image.save(mandelSurf, string)
			if event.key == pygame.K_m:
				mode = MAKEFULL
				finished = False
			if event.key == pygame.K_e:
				mode = EXPLORE
				mandelSub = mandelSubInit
			if event.key == pygame.K_1:
				system = mandelColor
				mandelSub = mandelSubInit
			if event.key == pygame.K_2:
				system = mandelNormal
				mandelSub = mandelSubInit
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False
	if keys[pygame.K_UP]:
		maxIterations += 1
		maxIterationsSurf = myFont.render("iterations: " + str(maxIterations), False, (255,255,255))
	if keys[pygame.K_DOWN]:
		maxIterations -= 1
		maxIterationsSurf = myFont.render("iterations: " + str(maxIterations), False, (255,255,255))
	if mousePressed:
		current = (pygame.mouse.get_pos()[0] / scaleFactor, pygame.mouse.get_pos()[1] / scaleFactor)
		cam = vecAdd(camPrev, vecMult(vecSub(point, current), scaleFactor))
		mandelSub = mandelSubInit
	
	
	# step:
	if mode == EXPLORE:
		# mandelStep()
		# print("S")
		pool = [threading.Thread(None, mandelStep, None, [i]) for i in range(16)]
		pool[0].start()
		pool[0].join()
	if mode == MAKEFULL and not finished:
		mandelMake()
	
	
	# draw:
	# win.fill((255,255,255))
	
	win.blit(pygame.transform.scale(mandelSurf, (winWidth, winHeight)), (0,0))
	win.blit(maxIterationsSurf, (10, winHeight - 20))
	
	
	
	pygame.display.update()
	fpsClock.tick(60)
pygame.quit()







