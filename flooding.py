import networkx as nx
from collections import OrderedDict

configs = [
	[(0,0), (1,2)], 
	[(0, 0), (3,1)], 
	[(0, 0), (3,2)], 
	[(0, 0), (2,4)], 
	[(0, 0), (3,4)], 
	[(0,0), (3,5)],  
	[(0,0), (4,5)], 
	[(0,0), (5,5)],
	[(0,0), (6,6)],
	[(0,0), (7,7)],
	[(0,0), (8,8)],
	[(1,1), (10,10)],
	[(1,1), (11,11)]
]



def route(config,l):

	L = l
	G = nx.grid_2d_graph(L,L)
	s= config[0]
	d = config[1]
	current_node = s

	router = OrderedDict()

	drop_count = 0
	success_count = 0 

	for x in G.nodes():
		G.node[x]['vis'] = False

	neighb = G.neighbors(current_node)
	router[current_node] = neighb

	
	for key in router.keys():

		if key == d:
			del router[key]
			success_count+=1


		else:
			G.node[key]['vis'] = True

			if all([G.node[y]['vis'] for y in router[key]]):
				drop_count+=1
				del router[key]
			else:
				for valus in router[key]:
					if G.node[valus]['vis'] == True:
						continue
					else:
						router[valus] = G.neighbors(valus)
			
	print("success:{0}  dropped:{1}".format(success_count,drop_count))


if __name__ == '__main__':

	for config in configs:
		route(config,12)

