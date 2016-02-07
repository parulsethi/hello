import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D
import scipy.signal

random.seed(1)

#: [s, d]
configs = [
	[(0, 0), (0,1)], 
	[(0, 0), (0,2)], 
	[(0,0), (1,2)], 
	[(0, 0), (3,1)], 
	[(0, 0), (3,2)], 
	[(0, 0), (2,4)], 
	[(0, 0), (3,4)], 
	[(0,0), (3,5)],  
	[(0,0), (4,5)], 
	[(0,0), (5,5)]
]

L=6
out = {}
fout = {}
cout = {}
counter = 0

def route(config):
	s= config[0]
	d = config[1]
	path = []
	current_node = ()
	previous_node = ()
	G = nx.grid_2d_graph(L,L)
	count = 0 

	while current_node != d:
		if not current_node:
			current_node = s
		neighb = G.neighbors(current_node)
		nxt = random.choice(neighb)
		while nxt==previous_node:
			nxt = random.choice(neighb)
		path.append(current_node)
		previous_node = current_node
		current_node = nxt
		count+=1
	path.append(d)
	return path, len(path)-1


def route_length_iterator(config,no_of_iteration):
	for i in range(no_of_iteration):
		p, pl =  route(config)
		yield pl


def optimal_distance(config):

	x2 = config[1][0]
	x1 = config[0][0]
	y2 = config[1][1]
	y1 = config[0][1]
	optimal_distance = 2*((x2-x1)+(y2-y1))
	return optimal_distance

def average_distance(config,no_of_iteration):

	avg = [ y for y in route_length_iterator(config,no_of_iteration)]
	avg_dis = sum(avg)/len(avg)
	return avg_dis


def path_length_distribution(dis_interval,config,no_of_iteration):

	q = [math.floor(_/dis_interval)*dis_interval for _ in route_length_iterator(config,no_of_iteration)]
	b = [q.count(_) for _ in range(0,max(q)+dis_interval,dis_interval)]
	print(b)
	plt.plot(b)
	plt.show()


def average_distance_freq(config,max_limit_iteration):
	freq_avg = []
	for i in range(1,max_limit_iteration):
		avg_dis = average_distance(config,i)
		freq_avg.append(avg_dis)

	freq_avg = scipy.signal.savgol_filter(freq_avg, 51,0)
	plt.plot(freq_avg)

	
def loop_average_distance_freq(max_limit_iteration):

	for config in configs:
		average_distance_freq(config,max_limit_iteration)
	plt.show()


def FreqAvg_vs_FreqOpt(no_of_iteration):

	x = []
	y = []
	for config in configs:
		x.append(optimal_distance(config))
		y.append(average_distance(config,no_of_iteration))

	y = scipy.signal.savgol_filter(y,3,0)
	plt.plot(x,y)
	plt.show()


if __name__ == "__main__":
	print("	keep calm and wait! ")
	FreqAvg_vs_FreqOpt(900)
