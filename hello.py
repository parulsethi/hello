import networkx as nx
import random
import numpy
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D

random.seed(1)

#: [s, d]
configs = [
	[(0, 0), (0,2)],
	[(0, 0), (3,1)],
	[(0, 0), (2,4)],
	[(0,0), (1,3)],
	[(0,0), (3,5)],
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
	print(path)
	print(len(path)-1)
	return path, len(path)-1



def route_length_iterator(config,no_of_iteration):
	for i in range(no_of_iteration):
		p, pl =  route(config)
		yield pl


def optimal_vs_average_distance(config,no_of_iteration):
	x2 = config[1][0]
	x1 = config[0][0]
	y2 = config[1][1]
	y1 = config[0][1]
	optimal_distance = 2*((x2-x1)+(y2-y1))
	seq = [ x for x in route_length_iterator(config,no_of_iteration)]
	average_distance = sum(seq)/len(seq)
	print(seq)
	print(average_distance)
	return optimal_distance,average_distance


def plot_optimal_vs_average_distance(no_of_iteration):

	to_plot = [optimal_vs_average_distance(i,no_of_iteration) for i in configs]
	optimal_distance = [x[0] for x in to_plot]
	average_distance = [x[1] for x in to_plot]
	plt.plot(optimal_distance,average_distance)
	plt.show()

def optimal_vs_deviation(config,no_of_iteration):

	x2 = config[1][0]
	x1 = config[0][0]
	y2 = config[1][1]
	y1 = config[0][1]
	optimal_distance = 2*((x2-x1)+(y2-y1))
	dev = [ y-optimal_distance for y in route_length_iterator(config,no_of_iteration)]
	deviation = sum(dev)/len(dev)
	return optimal_distance,deviation


def plot_optimal_vs_deviation(no_of_iteration):

	to_plot = [optimal_vs_deviation(i,no_of_iteration) for i in configs]
	optimal_distance = [x[0] for x in to_plot]
	deviation = [x[1] for x in to_plot]
	plt.plot(optimal_distance,deviation)
	plt.show()


def path_length_distribution(dis_interval,config,no_of_iteration):

	q = [math.floor(_/dis_interval)*dis_interval for _ in route_length_iterator(config,no_of_iteration)]
	print(q)
	b = [q.count(_) for _ in range(0,max(q)+dis_interval,dis_interval)]
	print(b)
	plt.plot(b)
	plt.show()



if __name__ == "__main__":
	no_of_iteration = 100
	path_length_distribution(5,configs[0],no_of_iteration)
