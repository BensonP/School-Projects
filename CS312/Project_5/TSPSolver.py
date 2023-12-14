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
	'''
	The class that holds different states. Each state holds an adjacency matrix, and is initilized to be reduced. Holds a cost, and indexes of city in the order of the current path. 
	Also includes a row and column bit map, that is either 1 for not being visited, or 0 for being visited. 
	I can initilize it with a list of cities and a size, or with attributes to copy a new matrix. 

	'''
	def __init__(self,size,cities = None, cost = 0, rowBit = [], columnBit = [], cityIndexes = [], array = [[]]):
		if len(columnBit) != 0:
			self.rowBit = rowBit 
			self.columnBit = columnBit
		else:
			self.rowBit = np.full(size,1)
			self.columnBit = np.copy(self.rowBit)
		if len(cities) != 0:
			self.array = np.zeros((size,size))
			self.cost = 0
			self.fillMatrix(cities, size)
		else: 
			self.array = array
			self.cost = cost
		if len(cityIndexes) != 0:
			self.cityIndexes = cityIndexes
		else:
			self.cityIndexes = []
	

	def fillMatrix(self, cities, size): #This initilizes my matrix with the first costs of different  Time: O(n^2)
		for i in range(size):
			for j in range(size):
				self.array[i,j] = cities[i].costTo(cities[j])
		self = rowReduceMatrix(self)
		self = columnReduceMatrix(self)

	def setBitMaps(self,row,column): #sets bit map according to the row and column. This helps me know what columns and rows need to be looked at when being reduced. If 0, dont reduce that row or column. 
		self.rowBit[row] = 0
		self.columnBit[column] = 0

	def setRowAndColumns(self,i,j):
		self.cost += self.array[i,j]
		self.array[j,i] = float('inf')
		self.array[i,:] = float('inf')
		self.array[:,j] = float('inf')
		return self.array
	

	def __lt__(self, other): #Overriding my lt operator for my priority queue. If my length of cities are the same, return the state with the lowest cost. Otherwise return the state with longest solution. 

		if len(self.cityIndexes) == len(other.cityIndexes):
			return self.cost < other.cost
		else:
			return len(self.cityIndexes) > len(other.cityIndexes)
		
		
	def copy(self): #Copys the source matrix and returns a new matrix. Very helpful for generating and expanding states
		newArray = self.array.copy()
		newColumnBit = self.columnBit.copy()
		newRowBit = self.rowBit.copy()
		newCost = self.cost.copy()
		newCityIndexes = self.cityIndexes.copy()

		newState = state(newArray.shape[0],[],newCost,newRowBit,newColumnBit,newCityIndexes,newArray)
		return(newState)

		

def getPath(solution, cities) -> [City]: #This returns a list of cities when given a list of indexes. 
		path = []
		for i in range(len(solution)):
			path.append(cities[solution[i]])
		return path

def findLowestNextCity(array,i,start,citiesCount,currentLength): #Returns a tuple (cost to that city, and next city index) of the lowest next city. If it would return back to source too early, then return the second lowest. 
	lowest = (float('inf'),None)
	for j in range(array.shape[0]):
		if array[i,j] < lowest[0]:
			if j != start and currentLength < citiesCount - 1:
				lowest = (array[i,j],j)
			if j == start and currentLength == citiesCount - 1:
				lowest = (array[i,j],j)
	return lowest

def rowReduceMatrix(state) -> state: #Takes in a state and returns a state with a row reduced matrix and an adjusted cost. 
	for i in range(state.array.shape[0]):
		if state.rowBit[i] != 0:
			lowest = np.min(state.array[i,:])
			if lowest == float('inf'):
				state.cost = float('inf')
			else:
				state.array[i][:] -= lowest
				state.cost += lowest
	return state

def columnReduceMatrix(state) -> state: #Takes in a state and returns a state with its column reduced matrix and adjusted cost. 
	for j in range(state.array.shape[1]):
		if state.columnBit[j] != 0:
			lowest = np.min(state.array[:,j])
			if lowest == float('inf'):
				state.cost = float('inf')
			else:
				state.array[:,j] -= lowest
				state.cost += lowest
	return state



def checkIfRootEdge(cities, start, end) -> bool: #Check if there is a edge from the end city to the start city.
	if cities[end].costTo(cities[start]) != float('inf'):
		return True
	else:
		return False
	
def generateChildrenStates(parentState, priorityQueue, bssf, stateNumber, pruned):
	'''
	The bulk of my branch and bound algorithm. Given a state, a priority Queue, a BSSF, State number, and pruned, 
	return true if the parentState is a valid solution, false if otherwise.
	Return updated stateNumber for total states	
	Return updated pruned number for total states pruned. 
	Looks at every possible child state from a parent state. Only adds those states whos cost is < than BSSF and is not an incomplete solution. I.E. a solution that is mising some cities. 

	'''
	totalCities = parentState.array.shape[0]
	currentCity = parentState.cityIndexes[-1]
	if len(parentState.cityIndexes) == totalCities: #Check if current parentState is a valid solution
		if parentState.array[currentCity,0] != float('inf'):
			parentState.cost += parentState.array[currentCity,0]
			return True,stateNumber, pruned
		else:
			pruned +=1
			return False,stateNumber,pruned
	
	for j in range(parentState.array.shape[0]):
		childState:state = parentState.copy() #Makes a copy to iterate off of. 
		stateNumber += 1
		if parentState.array[currentCity,j] != float('inf') and parentState.columnBit[j] == 1:
			childState.setBitMaps(currentCity, j)
			childState.setRowAndColumns(currentCity, j)
			rowReduceMatrix(childState)
			columnReduceMatrix(childState)
			childState.cityIndexes.append(j)
			
			if j == 0 and len(childState.cityIndexes) < totalCities: 
				pruned +=1
				continue
			if childState.cost > bssf: 
				pruned +=1
				continue
			priorityQueue.append(childState)
		else:
			pruned +=1
	heapq.heapify(priorityQueue) #Orders my PQ by len of current solution, then lower state cost. 
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
		'''
		Greedy algorithm is a modified version of my branch and bound. 
		It iterates through each city for it to be treated as a start city.
		If a invalid solution is found, continue to next city.
		If a valid solution is found, wherean edge from end to start exists and the le(solution) is equal to len(cities),
		Then set that as my current bssf if it is lower then the previous bssf. 
		Do this for each city.
		'''
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = float('inf')
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
				greedyState = rowReduceMatrix(greedyState)
				greedyState = columnReduceMatrix(greedyState)
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
		'''
		This starts at city 0 and creates a starting matrix based off of that using cities and length of cities. 
		The first city is popped onto my priority queue
		At the start of my while loop, pop off first state, and then expand it. 
		If my priority Queue size updates, then update maxSize.
		If result is true, meaning that the passed in state was a valid solution, then I set it to BSSF if it is lower then the current BSSF. 
		I continue this until my PQ is empty or I run out of time. I only expand those that are a valid soution and are less than or equal to current BSSF. 
		time complexity: 
		space complexity: 
		
		'''
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		solutionCount = 0  #count of total solutions found
		greedyResults = self.greedy()
		bssf = greedyResults['cost']
		greedySolution = greedyResults['soln']#gets my bssf from greedy
		start_time = time.time()
		startState = state(ncities,cities) #starting state
		startState.cityIndexes.append(0)
		priorityQueue = []
		states = {}
		priorityQueue.append(startState)
		states[startState.cost] = startState
		stateNumber = 0
		maxSize = 0
		pruned = 0

		while time.time()-start_time < time_allowance:
			if len(priorityQueue) != 0 :
				currentState = heapq.heappop(priorityQueue) #Returns state top of my PQ
				if currentState.cost <= bssf: #If the state is bigger than BSSF, prune it
					result,stateNumber, pruned = generateChildrenStates(currentState, priorityQueue, bssf, stateNumber, pruned) #my priorityQueue is updated within the function, and returns my updated pruned and stateNumbers. 
					results['total'] = stateNumber + pruned #State number is only what was added to the PriorityQueue, so have to add it. 
					results['pruned'] = pruned
					if len(priorityQueue) > maxSize:
						maxSize = len(priorityQueue)
						results['max'] = maxSize
					if result:
						solutionCount += 1
						bssf = currentState.cost
						results['cost'] = bssf
						results['time'] = time.time() - start_time
						results['count'] = solutionCount
						results['soln'] = TSPSolution(getPath(currentState.cityIndexes, cities))

						
				else:
					pruned +=1 #Update pruned and set total and pruned again. 
					results['total'] = stateNumber + pruned
					results['pruned'] = pruned
			else:
				
				return results
		if solutionCount == 0:
					results['pruned'] = pruned + len(priorityQueue)
					results['cost'] = bssf
					results['time'] = time.time() - start_time
					results['count'] = solutionCount
					results['soln'] = greedySolution
		return results