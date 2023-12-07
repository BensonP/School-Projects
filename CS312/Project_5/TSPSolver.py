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
		self.solution = []
		self.cityIndexes = []

	def fillMatrix(self, cities, size):
		for i in range(size):
			for j in range(size):
				self.array[i,j] = cities[i].costTo(cities[j])
		#print(self.array)
		self = rowReduceMatrix(self)
		#print(self.array)
		#print(self.cost)
		self = columnReduceMatrix(self)
		#print(self.array)
		#print(self.cost)
		#print(float('inf') - float('inf'))

	def setBitMaps(self,row,column):
		self.array[column,row] = float('inf')
		self.rowBit[row] = 0
		self.columnBit[column] = 0

	def setRowAndColumns(self,i,j):
		self.cost += self.array[i,j]
		self.array[j,i] = float('inf')
		self.array[i,:] = float('inf')
		self.array[:,j] = float('inf')
		return self.array

	def __lt__(self, other):
		if len(self.solution) == len(other.solution):
			return self.cost < other.cost
		else:
			return len(self.solution) > len(other.solution)

def findLowestNextCity(array,i,start,citiesCount,currentLength): #Returns a tuple (cost to that city, and next city index)
	lowest = (float('inf'),None)
	for j in range(array.shape[0]):
		if array[i,j] < lowest[0]:
			if j != start and currentLength < citiesCount - 1:
				lowest = (array[i,j],j)
			if j == start and currentLength == citiesCount - 1:
				lowest = (array[i,j],j)
	return lowest

def rowReduceMatrix(state):
	for i in range(state.array.shape[0]):
		if state.rowBit[i] != 0:
			lowest = np.min(state.array[i,:])
			if lowest == float('inf'):
				state.cost = float('inf')
			else:
				state.array[i][:] -= lowest
				state.cost += lowest
	return state

def columnReduceMatrix(state):
	for j in range(state.array.shape[1]):
		if state.columnBit[j] != 0:
			lowest = np.min(state.array[:,j])
			if lowest == float('inf'):
				state.cost = float('inf')
			else:
				state.array[:,j] -= lowest
				state.cost += lowest
	return state



def checkIfRootEdge(cities, start, end):
	if cities[end].costTo(cities[start]) != float('inf'):
		return True
	else:
		return False
	
def generateChildrenStates(parentState, currentCity, states, priorityQueue, bssf, totalCities, stateNumber, cities, pruned):
	#print(parentState.array, parentState.cost)
	if len(parentState.cityIndexes) == totalCities:
		if checkIfRootEdge(cities, 0, currentCity):
			print(parentState.array[currentCity,0])
			parentState.cost += parentState.array[currentCity,0]
			return True,stateNumber, pruned
		else:
			pruned +=1
			return False,stateNumber,pruned
	for j in range(parentState.array.shape[0]):
		childState = copy.deepcopy(parentState)
		stateNumber += 1
		if parentState.array[currentCity,j] != float('inf'):
			childState.setBitMaps(currentCity, j)
			childState.setRowAndColumns(currentCity, j)
			rowReduceMatrix(childState)
			columnReduceMatrix(childState)
			#print(childState.array, childState.cost)
			childState.cityIndexes.append(j)
			childState.solution.append(cities[j])
			if j == 0 and len(childState.cityIndexes) < totalCities: 
				pruned +=1
				continue
			if childState.cost > bssf: 
				pruned +=1
				continue
			priorityQueue.append(childState)
		else:
			pruned +=1
	heapq.heapify(priorityQueue)
	return False,stateNumber,pruned

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
		results = {}
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
			next = findLowestNextCity(greedyState.array,start,start,ncities,0)
			greedyState.cost += next[0]
			currentTour = []
			while next[0] != float('inf'):
				currentTour.append(cities[current])
				greedyState.setBitMaps(current,next[1])
				greedyState.setRowAndColumns(current,next[1])
				current = next[1]
				greedyState.cost += next[0]
				#print(greedyState.array)
				greedyState = rowReduceMatrix(greedyState)
				greedyState = columnReduceMatrix(greedyState)
				#print(greedyState.array, greedyState.cost)
				next = findLowestNextCity(greedyState.array,current,start,ncities,len(currentTour))
			if all(greedyState.columnBit[:] == 0):
				count +=1
				if greedyState.cost < bssf:
					bssf = greedyState.cost
					foundTour = currentTour
					time_spent = time.time() - start_time
					results['cost'] = bssf
					results['time'] = time_spent
					results['count'] = count
					results['soln'] = TSPSolution(foundTour)
					results['max'] = None
					results['total'] = None
					results['pruned'] = None
					
			start += 1
		return results



	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution,
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints:
		max queue size, total number of states created, and number of pruned states.</returns>
	'''

	def branchAndBound( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		count = 0
		bssf = self.greedy()['cost']
		start_time = time.time()
		startState = state(ncities,cities)
		startState.cityIndexes.append(0)
		startState.solution.append(cities[0])
		priorityQueue = []
		states = {}
		priorityQueue.append(startState)
		states[startState.cost] = startState
		stateNumber = 1
		pruned = 0

		while time.time()-start_time < time_allowance:
			if len(priorityQueue) != 0 :
				currentState = heapq.heappop(priorityQueue)
				if currentState.cost <= bssf:
					currentCity = currentState.cityIndexes[-1]
					result,stateNumber, pruned = generateChildrenStates(currentState, currentCity, states,priorityQueue, bssf, ncities, stateNumber, cities, pruned)
					if result:
						bssf = currentState.cost
						results['cost'] = bssf
						results['time'] = time.time() - start_time
						results['count'] = count
						results['soln'] = TSPSolution(currentState.solution)
						results['max'] = None
						results['total'] = stateNumber
						results['pruned'] = pruned
				else:
					pruned +=1
			else:
				return results
		return results



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
