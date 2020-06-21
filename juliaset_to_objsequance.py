import math

pi =    3.14159265359
euler = 2.71828182846

width = 2000
height = 2000

def smap(value,a,b,c,d):
	return (value - a)/(b - a) * (d - c) + c


def julia(x1,x2,y1,y2, frame, t):
	global width,height
	
	folder = "outPut folder here"
	file_name = folder + "/" + "output_c4d_" + str(frame).zfill(4) + ".obj"
	
	file = open(file_name, 'w')
	file.write("g object\n")
	count = 0
	
	for x in range(width):
		for y in range(height):
			
			a = smap(x,0,width,x1,x2)
			b = smap(y,0,height,y1,y2)
			
			ca = -0.7269
			cb = 0.1889
			
			iteration = 0
			#100 is fine:
			maxiter = 1000
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
			count += 1
			#write vertx
			file.write("v "+str(x)+" "+str(y)+" "+"{:.3f}".format(bright)+"\n")
			#print proccess
			if count % ((width**2)/10) == 0:
				print(count/(width**2) * 100,"%")
	#faces:
	file.write("\n")
	for j in range(0,width-1):
		for i in range(1,height):
			file.write("f "+str(i+j*width)+" "+str(i+j*width+1)+" "+str(width+1+i+j*width)+" "+str(width+i+j*width)+"\n")
		print proccess percentage:
		if j % (width/10) == 0:
			print(j/width * 100,"%")
	file.close()



def mand(x1,x2,y1,y2):
	global width,height
	
	file = open("output_c4d.obj", 'w')
	file.write("g object\n")
	
	count = 0
	
	for x in range(width):
		for y in range(height):
			a = smap(x,0,width,x1,x2)
			b = smap(y,0,height,y1,y2)
			ca = a
			cb = b

			iteration = 0
			#100 is fine:
			maxiter = 100
			while iteration < maxiter:
				aa = a*a - b*b
				bb = 2*a*b
				a = aa + ca
				b = bb + cb
				#4-16 is fine:
				#if math.fabs(aa + bb) > 16:
				#	break
				if aa**2 + bb**2 > 2**2:
					break
			
				iteration += 1
			#bright = smap(iteration, 0, maxiter, 0, 1)
			#bright = smap(math.sqrt(bright), 0,1,0,255)
			#bright = 255 * (math.log(maxiter - iteration + 1) / math.log(maxiter + 1))
			#bright = 255 * 1/(maxiter**60) * (iteration-maxiter)**60
			#bright = 255 * ((-1/maxiter) * iteration + 1)
			bright = 255 * math.exp(- 0.3 * iteration)
			
			#if iteration == maxiter:
			#	bright = 0
			count += 1
			#write vertx
			file.write("v "+str(x)+" "+str(y)+" "+"{:.3f}".format(bright)+"\n")
			#print proccess
			if count % ((width**2)/10) == 0:
				print(count/(width**2) * 100,"%")
			
	#faces:
	file.write("\n")
	for j in range(0,width-1):
		for i in range(1,height):
			file.write("f "+str(i+j*width)+" "+str(i+j*width+1)+" "+str(width+1+i+j*width)+" "+str(width+i+j*width)+"\n")
	file.close()


# squared size of math plane
size = 0.3

# animation variable t: t0 -> t1
t0 = 0
t1 = 1
step = 1

finished = False
t = t0

frame_counter = 0
run = True
while run:
	
	# The Julia Loop
	if not finished:
		#for mandelbrot, recommended (-size-0.5,size-0.5,-size,size)
		#mand(-size-0.5,size-0.5,-size,size)
		julia(-size-0.5,size-0.5,-size,size, frame_counter,t)
		
		t += step
		frame_counter += 1
		
		if t >= t1:
			finished = True
			print("Done")
			run = False




