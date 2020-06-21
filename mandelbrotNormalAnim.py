import pygame
import math
import colorsys
from color import *
pygame.init()

winWidth = 100
winHeight = 100

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
#pygame.draw.line(win, BLACK, (0,0), (100,200)) for lines
#win.fill(BLACK, ((50,50), (1, 1))) for pixels
#background:
win.fill((255,255,255))

h2 = 1.5
angle = 45
v = (math.cos((angle * 2 * math.pi)/360), math.sin((angle * 2 * math.pi)/360))
R = 100


def mand(point, width, height):
	global winWidth,winHeight
	for x in range(winWidth):
		for y in range(winHeight):
			
			a = smap(x, 0, winWidth, point[0] - width/2, point[0] + width/2)
			b = smap(y, 0, winHeight, point[1] - height/2, point[1] + height/2)
			c = (a, b)
			z = (a, b)
			
			# -0.7269
			# 0.1889
			
			dc = (1, 0)
			der = (1, 0)
			iteration = 0
			maxiter = 128
			reason = 0#not enough
		
			while iteration < maxiter:
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
			

def julia(center, point_c, width, height):
	c = (point_c[0], point_c[1])
	global winWidth,winHeight
	for x in range(winWidth):
		for y in range(winHeight):
			
			a = smap(x, 0, winWidth, center[0] - width/2, center[0] + width/2)
			b = smap(y, 0, winHeight, center[1] - height/2, center[1] + height/2)
			
			z = (a, b)
			
			# -0.7269
			# 0.1889
			
			dc = (1, 0)
			der = (1, 0)
			iteration = 0
			maxiter = 128
			reason = 0#not enough
		
			while iteration < maxiter:
				new_z = add(mult(z,z), c) 
				new_der = add(mult(smult(der, 2), z), dc)
				z = (new_z[0], new_z[1])
				der = (new_der[0], new_der[1])
				

				if math.sqrt(z[0]**2 + z[1]**2) > R*R:
					reason = 1#outside
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
			win.fill((bright,bright,bright), ((x,y), (1, 1)))
			
		# if x % (winWidth/10) == 0:
			# print(x/winWidth * 100,"%")
	# pygame.image.save(win, "mandelbrotPaint.png")
	# mut_s.play()
			
def anim_cardioid(t):
	x = (2*math.cos(t) - math.cos(2*t))/4
	y = (2*math.sin(t) - math.sin(2*t))/4
	return (x, y)

size = 3
current = (0,0)

# julia((0, 0), size, size)
# mand(current, size, size)


# animation setup:
points = []
t_start = 0
t_end = 2 * math.pi
step = t_end / 200
t = t_start
while t < t_end:
	points.append(anim_cardioid(t))
	t += step

# print(points)

# render:
frame = 0
folder = "output"
for point in points:
	julia((0,0), point, size, size)
	file_name = folder + "/" + "output_" + str(frame).zfill(4) + ".png"
	pygame.image.save(win, file_name)
	print(frame)
	frame += 1


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
	run = False
	
	#update game
	pygame.display.update() 
pygame.quit()




















