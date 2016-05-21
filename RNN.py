import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt
import math
import copy

np.random.seed(0)

class RNN(object):

	def __init__(self,L=20):

		self.G = nx.grid_2d_graph(L,L)
		self.alpha = 0.1
		self.input_dim = 2
		self.hidden_dim = 16
		self.output_dim = 1
		self.synapse_0 = 2*np.random.random((self.input_dim,self.hidden_dim)) - 1
		self.synapse_1 = 2*np.random.random((self.hidden_dim,self.output_dim)) - 1
		self.synapse_h = 2*np.random.random((self.hidden_dim,self.hidden_dim))

		self.synapse_0_update = np.zeros_like(self.synapse_0)
		self.synapse_1_update = np.zeros_like(self.synapse_1)
		self.synapse_h_update = np.zeros_like(self.synapse_h)


	# true values for shortest x
	def x_shortest(self,source,destination):

		path = nx.shortest_path(self.G,source,destination)
		x_path = [i[0] for i in path]
		return x_path[1:len(x_path)]
		
	# true values for shortest y
	def y_shortest(self,source,destination):

		path = nx.shortest_path(self.G,source,destination)
		y_path = [i[0] for i in path]
		return y_path

	def sigmoid(self,x):

		output = 1/(1+np.exp(-x))
		return output

	def sigmoid_derivative(self,x):

		return x*(1-x)

	# sigmoid-inverse
	def logit(self,u):

		out = -np.log((1/u)-1)
		return out


	# just x-series for now
	def train(self,src = (0,0),des = (5,10)):


		for j in range(100):

			#truth values for x
			c = self.x_shortest(src,des)

			d = np.zeros_like(c)
			overallError = 0

			layer_2_deltas = list()
			layer_1_values = list()
			layer_1_values.append(np.zeros(self.hidden_dim))

			out_seq = []

			for position in range(len(d)):

				if position==0:
					prev_x = self.sigmoid(src[0])
					prev_prev_x = self.sigmoid(des[0])

				# two inputs (the previous two co-ordinates)
				x = np.array([[prev_x,prev_prev_x]])
				y = np.array([[self.sigmoid(c[position])]]).T

				layer_1 = self.sigmoid(np.dot(x,self.synapse_0) + np.dot(layer_1_values[-1],self.synapse_h))

				layer_2 = self.sigmoid(np.dot(layer_1,self.synapse_1))

				out_seq.append(layer_2[0][0])
				prev_prev_x = prev_x
				prev_x = layer_2[0][0]

				layer_2_error = y - layer_2

				layer_2_deltas.append((layer_2_error)*self.sigmoid_derivative(layer_2))

				overallError += np.abs(layer_2_error[0])

				d[position] = np.round(layer_2[0][0])

				layer_1_values.append(copy.deepcopy(layer_1))

			future_layer_1_delta = np.zeros(self.hidden_dim)

			for position in range(len(d)):

				if position == len(d)-1:
					p = src[0]
					q = des[0]
					X = np.array([[p,q]])
				else:
					X = np.array([[out_seq[-position-1],out_seq[-position-2]]])
				
				layer_1 = layer_1_values[-position-1]
				prev_layer_1 = layer_1_values[-position-2]
				
				# error at output layer
				layer_2_delta = layer_2_deltas[-position-1]
				# error at hidden layer
				layer_1_delta = (future_layer_1_delta.dot(self.synapse_h.T) + layer_2_delta.dot(self.synapse_1.T)) * self.sigmoid_derivative(layer_1)

				# update all weights to try again
				self.synapse_1_update += np.atleast_2d(layer_1).T.dot(layer_2_delta)
				self.synapse_h_update += np.atleast_2d(prev_layer_1).T.dot(layer_1_delta)
				self.synapse_0_update += X.T.dot(layer_1_delta)
				
				future_layer_1_delta = layer_1_delta
		
			self.synapse_0 += self.synapse_0_update * self.alpha
			self.synapse_1 += self.synapse_1_update * self.alpha
			self.synapse_h += self.synapse_h_update * self.alpha    

			self.synapse_0_update *= 0
			self.synapse_1_update *= 0
			self.synapse_h_update *= 0

		# sigmoid on true value seq 
		for i in range(len(c)):
			c[i] = self.sigmoid(c[i])


		# inverse-sigmoid to get comparitive values
		for x in range(len(out_seq)):
			out_seq[x] = self.logit(out_seq[x])


		print("error\n"+str(layer_2_error))
		print("shortest seq\n"+str(c))
		print("output seq\n"+str(out_seq))