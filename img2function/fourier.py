import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import sys

argvs = sys.argv
argc = len(argvs)

def calc_ft(plot_path,n):

	namae = plot_path[0:len(plot_path)-4]

	with open(plot_path) as f:
		reader = csv.reader(f)
		header = next(reader)
		xp, yp = next(reader)
		xp = int(xp)
		yp = int(yp)
		for row in reader:
			xp = np.append(xp,int(row[0]))
			yp = np.append(yp,int(row[1]))


	l = len(xp)
	print(l)

	a = np.zeros(l)
	b = np.zeros(l)

	for i in range(n):
		for j in range(l-1):
			t = (2*np.pi)/l*j
			b[i] += (xp[j]*np.sin(i*t))
			a[i] += (xp[j]*np.cos(i*t))
	
	func_x = "("+str(round(a[0],2))+"/2)"
	x = 0
	
	for i in range(1,n):
		func_x += ("+(" + str(round(a[i],2)) + ")Cos[(" + str(i) + ")t]+(" + str(round(b[i],2)) + ")Sin[(" + str(i) + ")t]")
	for tt in range(0,l):
		t = 2*np.pi/l*tt
		x = np.append(x,0)
		x[tt] += a[0]/2
		for i in range(1,n):
			x[tt] += (a[i]*np.cos(i*t)+b[i]*np.sin(i*t))
	x = np.delete(x,-1)


	a = np.zeros(l)
	b = np.zeros(l)

	for i in range(n):
		for j in range(l-1):
			t = (2*np.pi)/l*j
			b[i] += (yp[j]*np.sin(i*t))
			a[i] += (yp[j]*np.cos(i*t))

	func_y = "("+str(round(a[0],2))+"/2)"
	y = 0
	for i in range(1,n):
		func_y += ("+(" + str(round(a[i],2)) + ")Cos[(" + str(i) + ")t]+(" + str(round(b[i],2)) + ")Sin[(" + str(i) + ")t]")
	for tt in range(0,l):
		t = 2*np.pi/l*tt
		y = np.append(y,0)
		y[tt] += a[0]/2
		for i in range(1,n):
			y[tt] += (a[i]*np.cos(i*t)+b[i]*np.sin(i*t))
	y = np.delete(y,-1)


	f = open(namae+"_func_"+argvs[2]+".txt","w")
	
	f.write("ParametricPlot[{" + func_x + "},{" + func_y + "},{t,0,2Pi}]")

	plt.plot(x,y)
	plt.gca().set_aspect('equal',adjustable='box')
#	plt.show()
	plt.savefig(namae+'_graph_'+argvs[2]+".png",bbox_inches="tight",pad_inches=0.0)
	print ("Completed")

if __name__ == '__main__':
	calc_ft(argvs[1],int(argvs[2]))
	plt.figure()


