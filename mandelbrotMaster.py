from math import fabs, sqrt, cos, sin, pi, floor, ceil, e, atan2, log
from random import uniform, randint, choice
from datetime import datetime
import pygame

import time
# import threading
import multiprocessing
import os

pygame.init()
fpsClock = pygame.time.Clock()

winWidth = 1280
winHeight = 720
win = pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption('Simon\'s graph')

pygame.font.init()
myFont =  pygame.font.SysFont('Tahoma', 12, True)

scaleFactor = 200
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

def smap(value,a,b,c,d):
	return (value - a)/(b - a) * (d - c) + c

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
mandelSubInit = 20
mandelSub = mandelSubInit

THREADS = 16
HALVES = int(sqrt(THREADS))

# parameters for mandelNormal
h2 = 1.5
angle = 45+180
v = (cos((angle * 2 * pi)/360), sin((angle * 2 * pi)/360))
RADIUS = 100

maxIterations = 100
maxIterationsSurf = myFont.render("iterations: " + str(maxIterations), False, (255,255,255))

finished = False

dimsFull = (4000, 2250)

dims = win.get_size()

winDims = True

# image = pygame.image.load("assets/karim.png")
# image = pygame.transform.flip(image, False, True)

out = 4
move = -180
def smap(value,a,b,c,d):
	return (value - a)/(b - a) * (d - c) + c

def mandelColor(pos, color = 0):
	a = pos[0]
	b = pos[1]
	
	ca = a
	cb = b
	
	iteration = 0
	while iteration < maxIterations:
		#
		# za = a
		# zb = b
		#
	
		aa = a*a - b*b
		bb = 2*a*b

		a = aa + ca
		b = bb + cb
		
		# if fabs(aa) + fabs(bb) > 4:# asteroids
		# if fabs(aa + bb) > 4:# droplets
		if a*a + b*b > 4:# circular
		# if sqrt(a*a + b*b) > out:# circular
			break
		
		iteration += 1
	
	if color == 0: # colorfull, olc
		f = 0.1
		red = (0.5 * sin(f * iteration) + 0.5) * 255
		green = (0.5 * sin(f * iteration + 2.094) + 0.5) * 255
		blue = (0.5 * sin(f * iteration + 4.188) + 0.5) * 255
		return (red, green, blue)	
	
	elif color == 1: # black&white
		if iteration == maxIterations:
			return (0,0,0)
		else:
			return (255,255,255)
	
	elif color == 2:
		return (255,255,255) if iteration % 2 == 0 else (0,0,0)

def mandelImage(pos):
	a = pos[0]
	b = pos[1]
	
	ca = a
	cb = b
	
	iteration = 0
	while iteration < maxIterations:
		#
		# za = a
		# zb = b
		#
	
		aa = a*a - b*b
		bb = 2*a*b

		a = aa + ca
		b = bb + cb
		
		# if fabs(aa) + fabs(bb) > 4:# asteroids
		# if fabs(aa + bb) > 4:# droplets
		# if a*a + b*b > 4:# circular
		if sqrt(a*a + b*b) > out:# circular
			break
		
		iteration += 1
		
	
	# a*=50
	# b*=50
	pos = (image.get_width()//2, image.get_height()//2)
	
	# col = ((pos[0] + int(za))% image.get_width(), (pos[1] + int(zb)) % image.get_height())
	
	x = (atan2(a, b) * (1/pi) + 1)/2
	x *= image.get_width()
	x = int((x + move) % image.get_width())

	
	mag = sqrt(a*a + b*b)
	if not out < mag < out*out:
		y = 1
	else:
		y = log(mag / out) / log(out)
	y = smap(y, 0, 1, 0, image.get_height() - 1)
	
	y = int(y)
	
	""" no log:
	mag = sqrt(a*a + b*b)
	if not out <= mag <= out*out:
		y = 0
	else:
		y = (mag - out)/(out*out - out)
	y *= image.get_height()
	y = int(y)
	if y > image.get_height():
		return image.get_height()
	"""
	
	# x /= image.get_width()
	# x *= 255
	# x = int((x + move) % 255)
	# print(x)
	# return (x, x, x)
	return image.get_at((x,y))

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

def mandelStep(box=-1):
	# print("s")
	global mandelSub, mandelSurf
	
	width = downRight()[0] - upLeft()[0]
	height = downRight()[1] - upLeft()[1]

	row = box // HALVES
	col = box % HALVES

	rangeX = (int(row * (mandelSurf.get_width()//HALVES)), int(row * (mandelSurf.get_width()//HALVES) + (mandelSurf.get_width()//HALVES)))
	rangeY = (int(col * (mandelSurf.get_height()//HALVES)), int(col * (mandelSurf.get_height()//HALVES) + (mandelSurf.get_height()//HALVES)))

	# print(rangeX, rangeY)
	if box == -1:
		rangeX = (0, mandelSub)
		rangeY = (0, mandelSub)

	for hor in range(rangeX[0], rangeX[1]):
		xSamp = upLeft()[0] + (width / mandelSub) * hor
		
		for ver in range(rangeY[0], rangeY[1]):
			ySamp = upLeft()[1] + (height / mandelSub) * ver
			
			mandelSurf.set_at((hor, ver), system((xSamp,ySamp)))
	mandelSub += 5
	if mandelSub >= winWidth:
		mandelSub = winWidth

def mandelMake(box=-1):
	global mandelSurf, finished
	
	# totalSteps = winWidth * winHeight
	# count = 0
	
	width = downRight()[0] - upLeft()[0]
	height = downRight()[1] - upLeft()[1]
	
	row = box // HALVES
	col = box % HALVES

	rangeX = (int(row * (mandelSurf.get_width()//HALVES)), int(row * (mandelSurf.get_width()//HALVES) + (mandelSurf.get_width()//HALVES)))
	rangeY = (int(col * (mandelSurf.get_height()//HALVES)), int(col * (mandelSurf.get_height()//HALVES) + (mandelSurf.get_height()//HALVES)))
		
	for ver in range(rangeY[0], rangeY[1]):
		ySamp = upLeft()[1] + (height / winHeight) * ver
		
		for hor in range(rangeX[0], rangeX[1]):
			xSamp = upLeft()[0] + (width / winWidth) * hor
			
			mandelSurf.set_at((hor, ver), system((xSamp,ySamp)))
	
	finished = True
	print("thread fin: ", box)

	# print(box)
	#win.blit(mandelSurf, (0,0))
	pygame.image.save(mandelSurf, "gallery/mands/" + str(box) + ".png")
	pygame.display.update()

def mandelMakeout(box, camera, scaling, system, iterations, dims=win.get_size()):
	global mandelSurf, finished, cam, scaleFactor, maxIterations
	
	maxIterations = iterations
	cam = camera
	scaleFactor = scaling
	
	width = downRight()[0] - upLeft()[0]
	height = downRight()[1] - upLeft()[1]
	
	row = box // HALVES
	col = box % HALVES

	rangeX = (int(row * (dims[0]//HALVES)), int(row * (dims[0]//HALVES) + (dims[0]//HALVES)))
	rangeY = (int(col * (dims[1]//HALVES)), int(col * (dims[1]//HALVES) + (dims[1]//HALVES)))
	
	boxSurf = pygame.Surface((rangeX[1] - rangeX[0], rangeY[1] - rangeY[0]))
	
	for ver in range(0, rangeY[1] - rangeY[0]):
		ySamp = upLeft()[1] + (height / dims[1]) * (ver + rangeY[0])
		
		for hor in range(0, rangeX[1] - rangeX[0]):
			xSamp = upLeft()[0] + (width / dims[0]) * (hor + rangeX[0])
			
			boxSurf.set_at((hor, ver), system((xSamp,ySamp)))
	
	finished = True

	pygame.image.save(boxSurf, "gallery/mands/" + str(box) + ".png")
	pygame.display.update()


################################################################################ Main Loop

if __name__ == '__main__':
	finished = False
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
				if event.key == pygame.K_3:
					system = mandelImage
					mandelSub = mandelSubInit
				if event.key == pygame.K_d:
					if winDims == True:
						winDims = False
						dims = dimsFull
					else:
						winDims = True
						dims = win.get_size()
				# if event.key == pygame.K_9:
					# move -= 1
				# if event.key == pygame.K_0:
					# move += 1
		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			run = False
		if keys[pygame.K_UP]:
			maxIterations += 1
			maxIterationsSurf = myFont.render("iterations: " + str(maxIterations), False, (255,255,255))
		if keys[pygame.K_DOWN]:
			maxIterations -= 1
			maxIterationsSurf = myFont.render("iterations: " + str(maxIterations), False, (255,255,255))
		if keys[pygame.K_9]:
			move -= 1
		if keys[pygame.K_0]:
			move += 1
		if mousePressed:
			current = (pygame.mouse.get_pos()[0] / scaleFactor, pygame.mouse.get_pos()[1] / scaleFactor)
			cam = vecAdd(camPrev, vecMult(vecSub(point, current), scaleFactor))
			mandelSub = mandelSubInit
		
		
		# step:
		if mode == EXPLORE:
			mandelSurf = pygame.Surface((mandelSub, mandelSub))
			mandelStep(-1)
			
		if mode == MAKEFULL and not finished:

			mandelSurf = pygame.Surface(dims)
			start = time.time()
			pool = [multiprocessing.Process(target=mandelMakeout, args=[i, cam, scaleFactor, system, maxIterations, dims]) for i in range(THREADS)]
			for i in range(THREADS):
				pool[i].start()
				pygame.event.pump()
			for i in range(THREADS):
				pool[i].join()
			finished = True
			done = time.time()
			print("time taken:", done - start)
			
			for i in range(THREADS):
				file = "gallery/mands/" + str(i) + ".png"
				partial = pygame.image.load(file)
				x = i // HALVES
				y = i % HALVES
				mandelSurf.blit(partial, (x * partial.get_width(), y * partial.get_height()))
				os.remove(file)

			
		# draw:
		# win.fill((255,255,255))
		
		win.blit(pygame.transform.scale(mandelSurf, (winWidth, winHeight)), (0,0))
		win.blit(maxIterationsSurf, (10, winHeight - 20))
		
		
		
		pygame.display.update()
		fpsClock.tick(60)
	pygame.quit()






