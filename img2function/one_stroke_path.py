#coding:utf-8
import cv2
import numpy as np
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from scipy.spatial import distance as dis
import sys
from sklearn import preprocessing
import time

argvs = sys.argv
argc = len(argvs)
namae = "output/" + argvs[1][0:len(argvs[1])-4]

way = []
ways = []
init_x = 0.4
init_y = 0
draw_z = 0.114
stay_z = 0.130
size_picture = 0.15


class TSP:
	def __init__(self,path=None,alpha = 1.0,beta = 1.0,Q = 1.0,vanish_ratio = 0.95):
		self.alpha = alpha					
		self.beta = beta					
		self.Q = Q							
		self.vanish_ratio = vanish_ratio	
		if path is not None:
			self.set_loc(np.array(pd.read_csv(path)))
	
	def set_loc(self,locations):
		self.loc = locations						
		self.n_data = len(self.loc)						
		self.dist = dis.squareform(dis.pdist(self.loc))	
		self.weight = np.random.random_sample((self.n_data,self.n_data))+1.0	
		self.result = np.arange(self.n_data)			
		
	def cost(self,order):
		order2 = np.r_[order[1:],order[0]]
		
		return np.sum(tsp.dist[order,order2])
	
	def plot(self,order=None):
		if order is None:
			plt.plot(self.loc[:,0],self.loc[:,1])
		else:
			plt.plot(self.loc[order,0],self.loc[order,1])
		plt.savefig(namae+"_onestroke.png",bbox_inches="tight",pad_inches=0.0)
#		plt.show()
	
	def solve(self,n_agent=1000):
		
		order = np.zeros(self.n_data,np.int) 		
		delta = np.zeros((self.n_data,self.n_data))	
		
		for k in range(n_agent):
			city = np.arange(self.n_data)
			now_city = np.random.randint(self.n_data)	
			
			city = city[ city != now_city ]
			order[0] = now_city
			
			for j in range(1,self.n_data):
				upper = np.power(self.weight[now_city,city],self.alpha)*np.power(self.dist[now_city,city],-self.beta)
				
				evaluation = upper / np.sum(upper)				
				percentage = evaluation / np.sum(evaluation)	
				
				index = self.random_index2(percentage)			
				
				now_city = city[ index ]
				city = city[ city != now_city ]
				order[j] = now_city
			
			L = self.cost(order) 
			
			delta[:,:] = 0.0
			c = self.Q / L
			for j in range(self.n_data-1):
				delta[order[j],order[j+1]] = c
				delta[order[j+1],order[j]] = c
			
			self.weight *= self.vanish_ratio 
			self.weight += delta
			
			if self.cost(self.result) > L:
				self.result = order.copy()
			
			print("Agent ... %d,\t Now Cost %lf,\t Best Cost ... %lf" % (k,L,self.cost(self.result)))
	
		return self.result

	def save(self,out_path):
		points = self.loc[ self.result ]
		f = open(out_path,"w")
		f.write("x,y\n")
		for i in range(len(points)):
			f.write(str(points[i,0]) + "," + str(points[i,1])+"\n")
		f.close()

	def path_save(self,out_path):
		#normalize to fit 150mm*150mm square and centeralize to (init_x, init_y)
		points =np.array(self.loc[ self.result ])
		max_xy = points.max(axis=0)
		min_xy = points.min(axis=0)
		retio=0
		if (max_xy[0] - min_xy[0] > max_xy[1] - min_xy[1]) :
			retio = size_picture / (max_xy[0] - min_xy[0])
		else :
			retio = size_picture / (max_xy[1] - min_xy[1])
		points = (points - [(max_xy[0]+min_xy[0])/2, (max_xy[1]+min_xy[1])/2]) * retio + [init_x, init_y]
		
		#calculate L2norm between adjoining points
		distances = []
		for i in range (len(points)-1):
		    distances.append(np.sqrt((points[i+1][0]-points[i][0])**2 + (points[i+1][1]-points[i][1])**2))
		dis_median = np.median(distances)
		redundant_edge = []
		for i in range(len(distances)):
			if distances[i] > 5 * dis_median:
				redundant_edge.append([i, i+1])
		# for i in range(len(duplicated_redundant_edge)-1):
		# 	if duplicated_redundant_edge[i][1]== duplicated_redundant_edge[i+1][0]:

		#print (redundant_edge)
		#generate trajectory
		ways = []
		ways.append([points[0, 0], points[0, 1], stay_z])
		for i in range(len(points)):
			counter = 0
			for j in range(len(redundant_edge)):
				if redundant_edge[j][0] == i:
					counter += 1
					ways.append([points[i, 0], points[i, 1], draw_z])
					ways.append([points[i, 0], points[i, 1], stay_z])
					break
				# elif redundant_edge[j][1] == i:
				# 	counter += 1
				# 	ways.append([points[i, 0], points[i, 1], stay_z])
				# 	ways.append([points[i, 0], points[i, 1], draw_z])
				# 	break
			if counter == 0:
				ways.append([points[i, 0], points[i, 1], draw_z])
		ways.append([points[len(points)-1, 0], points[len(points)-1, 1], stay_z])
		f = open(out_path,"w")
		for way in ways:
			f.write("0,90,0,0," + str(way[0]) + "," + str(way[1]) + "," + str(way[2]) + "\n")
		f.close()

		transpose_ways = np.array(ways).transpose()
		fig = plt.figure()
		ax = Axes3D(fig)
		ax.plot(transpose_ways[0], transpose_ways[1], transpose_ways[2])
		
		ax.set_xlabel('x')
		ax.set_ylabel('y')
		ax.set_zlabel('z')
		
		plt.show()

	
	def random_index(self,percentage):
		n_percentage = len(percentage)
		arg = np.argsort(percentage)
		while True:
			index = np.random.randint(n_percentage)
			y = np.random.random()
			if y < percentage[index]:
				return index

	def random_index2(self,percentage):
		n_percentage = len(percentage)
		arg = np.argsort(percentage)[::-1]
		n_arg = min(n_percentage,10)
		percentage = percentage / np.sum( percentage[arg] )
		
		while True:
			index = np.random.randint(n_arg)
			y = np.random.random()
			if y < percentage[arg[index]]:
				return arg[index]



def save_edge_points(img_path,out_path):
	img = cv2.imread(img_path)
	edge = cv2.Canny(img,100,200)
	
	h,w = edge.shape
	x = np.arange(w)
	y = -(np.arange(h))

	X,Y = np.meshgrid(x,y)

	X_true = X[ edge > 128 ]
	Y_true = Y[ edge > 128 ]

	index = np.array([X_true,Y_true]).T

	f = open(out_path,"w")
	f.write("x,y\n")
	for i in range(len(index)):
		f.write(str(index[i,0]) + "," + str(index[i,1])+"\n")
	f.close()

if __name__=="__main__":
	start_time = time.time()
	save_edge_points("pictures/"+argvs[1],namae+"_edge_points.csv")
	tsp = TSP(path=namae+"_edge_points.csv",alpha=1.0,beta=16.0,Q=1.0e3,vanish_ratio = 0.8)
	tsp.solve(1)
	print ("processing time : " + str(round(time.time()-start_time, 2)) + " seconds")
	tsp.path_save(namae+"_best_order.csv")
	#tsp.save(namae+"_best_order.csv")
	tsp.plot(tsp.result)
