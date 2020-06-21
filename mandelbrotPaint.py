import pygame
import math
import colorsys
from color import *
pygame.init()

winWidth = 500
winHeight = 500

win = pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption("caption")
mut_s = pygame.mixer.Sound("sfx/mut.wav")

def smap(value,a,b,c,d):
	return (value - a)/(b - a) * (d - c) + c

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
	return math.sqrt(one[0]*one[0] + one[1]*one[1])

################################################################################ Setup

win.fill((255,255,255))

h2 = 1.5
angle = 45+180
v = (math.cos((angle * 2 * math.pi)/360), math.sin((angle * 2 * math.pi)/360))
R = 100

def mand(point, width, height):
	global winWidth,winHeight
	for x in range(winWidth):
		for y in range(winHeight):
			
			a = smap(x, 0, winWidth, point[0] - width/2, point[0] + width/2)
			b = smap(y, 0, winHeight, point[1] - height/2, point[1] + height/2)
			
			# ca = a
			# cb = b
			c = (a, b)
			
			z = (a, b)
			
			dc = (1, 0)
			
			der = (1, 0)
			
			iteration = 0
			maxiter = 1000
			
			reason = 0#not enough
			
			while iteration < maxiter:
				# aa = a*a - b*b
				# bb = 2*a*b
				
				# a = aa + ca
				# b = bb + cb
				
				new_z = add(mult(z,z), c) 
				
				new_der = add(mult(smult(der, 2), z), dc)
				
				z = (new_z[0], new_z[1])
				
				der = (new_der[0], new_der[1])
				
				
				
				if math.sqrt(z[0]**2 + z[1]**2) > R*R:
					reason = 1#outside
					break
				# if math.fabs(aa + bb) > 16: break
				# if math.sqrt(a**2 + b**2) > R*R: break
				# if math.pow(abs(a), 0.4) + math.pow(abs(b), 0.4) > 2: break
				
				iteration += 1
			
			# bright = smap(iteration, 0, maxiter, 0, 1)
			# bright = smap(math.sqrt(bright), 0,1,0,255)
			# if iteration == maxiter:
				# bright = 0
			#3
			#bright = smap(iteration, 0, maxiter, 0, 255)
			#if iteration == maxiter:
			#	bright = 0
			#2
			#bright = smap(iteration, 0, maxiter, 0, 255)
			#1
			# bright = (iteration * 16) % 255
			
			# bright = 0.5 * math.sin(iteration) + 0.5
			# bright *= 255
			
			# bright = 255 if iteration % 2 == 0 else 0
			# win.fill((bright,bright,bright), ((x,y), (1, 1)))
			
			# bright = 
			
			# f = 0.1
			# n = iteration
			# red = 0.5 * math.sin(f * n) + 0.5
			# green = 0.5 * math.sin(f * n + 2.094) + 0.5
			# blue = 0.5 * math.sin(f * n + 4.188) + 0.5
			# red *= 255
			# green *= 255
			# blue *= 255
			# win.fill((red, green, blue), ((x,y), (1, 1)))
			
			if reason == 0:
				bright = 0
			else:
				u = div(z, der)
				u = smult(u, 1/cabs(u))
				t = u[0]*v[0] + u[1]*v[1] + h2
				t = t/(1+h2)
				if t<0: t=0
				bright = t*255
			win.fill((bright,bright,bright), ((x,y), (1, 1)))
			
		if x % (winWidth/10) == 0:
			print(x/winWidth * 100,"%")
	pygame.image.save(win, "mandelbrotPaint.png")
	mut_s.play()
			

size = 0.01
current = (	-0.525, -0.523)
# (-0.524, -0.516) 0.04
mand(current, size, size)

################################################################################ Main Loop
run = True
while run:
	pygame.time.delay(1)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONUP:
			x,y = event.pos
			x = smap(x, 0, winWidth, current[0] - size/2, current[0] + size/2)
			y = smap(y, 0, winHeight, current[1] - size/2, current[1] + size/2)
			current = (x,y)
			size /= 10
			mand(current,size, size)
			print(current, size)
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False
		
	#steps
	
	
	#update game
	pygame.display.update() 
pygame.quit()




















