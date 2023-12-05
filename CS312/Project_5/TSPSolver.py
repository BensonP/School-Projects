#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


import time
import numpy as np
from TSPClasses import *
import heapq
import itertools
import random
import copy

class state:
	def __init__(self,size,cities):
		self.array = np.zeros((size,size))
		self.cost = 0
		self.rowBit = np.full(size,1)
		self.columnBit = np.copy(self.rowBit)
		self.fillMatrix(cities, size)

	def fillMatrix(self, cities, size):
		for i in range(size):
			for j in range(size):
				self.array[i,j] = cities[i].costTo(cities[j])
		print(self.array)
		lowest = findLowestNextCity(self.array,0)
		print(lowest)
		self = rowReduceMatrix(self)
		print(self.array)
		print(self.cost)
		self = columnReduceMatrix(self)
		print(self.array)
		print(self.cost)

	def setBitMaps(self,row,column):
		self.array[column,row] = float('inf')
		self.rowBit[row] = 0
		self.columnBit[column] = 0

def findLowestNextCity(array,i): #Returns a tuple (cost to that city, and next city index)
	lowest = (float('inf'),None)
	for j in range(array.shape[0]):
		if array[i,j] < lowest[0]:
			lowest = (array[i,j],j)
	return lowest

def rowReduceMatrix(state):
	for i in range(state.array.shape[0]):
		if state.rowBit[i] != 0:
			lowest = findLowestNextCity(state.array,i)
			state.array[i][:] -= lowest[0]
			state.cost += lowest[0]
	return state

def columnReduceMatrix(state):
	for j in range(state.array.shape[1]):
		if state.columnBit[j] != 0:
			lowest = np.min(state.array[:,j])
			state.array[:,j] -= lowest
			state.cost += lowest
	return state

def setRowAndColumns(array,i,j):
	array[j,i] = float('inf')
	array[i,:] = float('inf')
	array[:,j] = float('inf')
	return array

	




class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution,
		time spent to find solution, number of permutations tried during search, the
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this
		algorithm</returns>
	'''

	def greedy( self,time_allowance=60.0 ):
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = float('inf')
		found = False
		time_spent = 0
		start_time = time.time()

		startState = state(ncities,cities)
		current = 0
		start = 0
		while time.time()-start_time < time_allowance and start < ncities:
			current = start
			greedyState = copy.deepcopy(startState)
			next = findLowestNextCity(greedyState.array,start)
			currentTour = []
			while next[0] != float('inf'):
				currentTour.append(current)
				greedyState.setBitMaps(current,next[1])
				greedyState.array = setRowAndColumns(greedyState.array,current,next[1])
				current = next[1]
				print(greedyState.array)
				greedyState = rowReduceMatrix(greedyState)
				greedyState = columnReduceMatrix(greedyState)
				print(greedyState.array, greedyState.cost)
				next = findLowestNextCity(greedyState.array,current)
			if all(greedyState.columnBit[:] == 0):
				count +=1
				if greedyState.cost < bssf:
					bssf = greedyState.cost
					foundTour = currentTour
					time_spent = time.time()
					
			start += 1

		return int(bssf),int(time_spent),int(count),foundTour,None,None,None



	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''

	def branchAndBound( self, time_allowance=60.0 ):
		pass



	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number of solutions found during search, the
		best solution found.  You may use the other three field however you like.
		algorithm</returns>
	'''

	def fancy( self,time_allowance=60.0 ):
		pass
