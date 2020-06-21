import math

pi =    3.14159265359
euler = 2.71828182846

width = 500
height = 500

def smap(value,a,b,c,d):
	return (value - a)/(b - a) * (d - c) + c


def julia(x1,x2,y1,y2, frame, t):
	global width,height
	
	folder = "outputFolder"
	file_name = folder + "/" + "output_c4d_" + str(frame).zfill(4) + ".obj"
	
	file = open(file_name, 'w')
	file.write("g object\n")
	
	for x in range(width):
		for y in range(height):
			
			a = smap(x,0,width,x1,x2)
			b = smap(y,0,height,y1,y2)
			
			ca = 0.7885 * math.cos(t)
			cb = 0.7885 * math.sin(t)
			
			iteration = 0
			#100 is fine:
			maxiter = 100
			while iteration < maxiter:
				aa = a*a
				bb = b*b
				#4-16 is fine:
				if math.fabs(aa + bb) > 16:
					break
				twoab = 2 * a * b
				a = aa - bb + ca
				b = twoab + cb
				iteration += 1
			bright = smap(iteration, 0, maxiter, 0, 1)
			bright = smap(math.sqrt(bright), 0,1,0,255)
			
			#if iteration == maxiter:
			#	bright = 0
			
			#write vertx
			file.write("v "+str(x)+" "+str(y)+" "+str(bright)+"\n")
	#faces:
	file.write("\n")
	for j in range(0,width-1):
		for i in range(1,height):
			file.write("f "+str(i+j*width)+" "+str(i+j*width+1)+" "+str(width+1+i+j*width)+" "+str(width+i+j*width)+"\n")
		#print proccess percentage:
		if j % (width/10) == 0:
			print(j/width * 100,"%")
	file.close()



def mand(x1,x2,y1,y2, frame,t):
	global width,height
	
	folder = "outputFolder"
	file_name = folder + "/" + "output_c4d_" + str(frame).zfill(4) + ".obj"
	
	file = open(file_name, 'w')
	file.write("g object\n")
	
	for x in range(width):
		for y in range(height):
			a = smap(x,0,width,x1,x2)
			b = smap(y,0,height,y1,y2)
			ca = a
			cb = b

			iteration = 0
			#100 is fine:
			maxiter = t+100
			while iteration < maxiter:
				aa = a*a - b*b
				bb = 2*a*b
				a = aa + ca
				b = bb + cb
				#4-16 is fine:
				if math.fabs(aa + bb) > 16:
					break
			
				iteration += 1
			#bright = smap(iteration, 0, maxiter, 0, 1)
			#bright = smap(math.sqrt(bright), 0,1,0,255)
			bright = 255 * (math.log(maxiter - iteration + 1) / math.log(maxiter + 1))
			
			#if iteration == maxiter:
			#	bright = 0
			#write vertx
			file.write("v "+str(x)+" "+str(y)+" "+str(bright)+"\n")
	#faces:
	file.write("\n")
	for j in range(0,width-1):
		for i in range(1,height):
			file.write("f "+str(i+j*width)+" "+str(i+j*width+1)+" "+str(width+1+i+j*width)+" "+str(width+i+j*width)+"\n")
		#print proccess percentage:
		if j % (width/10) == 0:
			print(j/width * 100,"%")
	file.close()


# squared size of math plane
size = 2

x2zoom = -0.761574
y2zoom = -0.08475612417389153

def zoomfunc(x):
	#return 1/x**2
	#return 5*math.exp(-x)
	return 5*math.exp(-0.1*x)
	#return 1/x

# animation variable t: t0 -> t1
t0 = 330
t1 = 350
step = 1

finished = False
t = t0

frame_counter = t
run = True
while run:
	
	# The Julia Loop
	if not finished:
		#for mandelbrot, recommended (-size-0.5,size-0.5,-size,size)
		mand(x2zoom-zoomfunc(t),x2zoom+zoomfunc(t),y2zoom-zoomfunc(t),y2zoom+zoomfunc(t), frame_counter, t)
		
		t += step
		frame_counter += 1
		
		if t >= t1:
			finished = True
			print("Done")
			run = False




