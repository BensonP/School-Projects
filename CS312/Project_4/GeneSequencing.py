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

import random

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

class GeneSequencing:

	def __init__( self ):
		pass

	def getLeft(self,x,y):  #returns the left neighbor value plus the cost for inserting.
		if self.banded:
			if self.distFromDiagonal == -MAXINDELS: #returns infinity if the neighbor does not exist.
				return float('inf'), None
		return (self.table[(x,y-1)][0] + INDEL,(x,y-1))
	
	
	def getTop(self,x,y): #returns the top neighbor value plus cost for deleting.
		if self.banded:
			if self.distFromDiagonal == MAXINDELS: #Returns infinity in the neighbor does not exist for banded. 
				return float('inf'), None
		return (self.table[(x-1, y)][0] + INDEL,(x-1,y))
	
	def getDiagonal(self,x,y,seq1,seq2): #returns diaganal neighbor plus the cost of diagonal. Diagonal neighbor will always exist.
		if seq1[x-1] == seq2[y-1]:
			return (self.table[(x-1,y-1)][0] + MATCH,(x-1,y-1))
		else: return(self.table[(x-1,y-1)][0] + SUB,(x-1,y-1))

	
	def loadBaseCases(self,seq1,seq2): #Load bases. If banded, only loads bases on first row and column of K + 1 (band length + 1)
		self.table[(0,0)] = 0,None   #O(i + j) speed for unbanded, O(2K + 1) speed for banded
		if self.banded:				 #O(i + j) space for unbanded, O(2k + 1) space for banded
			for j in range(1, MAXINDELS+1):
				self.table[(j,0)] = 5*j,(j-1,0)
			for i in range(1, MAXINDELS+1):
				self.table[(0,i)] = 5*i,(0,i-1)
		else:
			for j in range(1,len(seq1)+1):
				self.table[(j,0)] = 5*j,(j-1,0)
			for i in range(1,len(seq2)+1):
				self.table[(0,i)] = 5*i,(0,i-1)

	def getLowestScore(self,x,y,seq1,seq2): #recieves all neighbors and compares the lowest cost to put in current box and returns it.
		left = self.getLeft(x,y)
		top = self.getTop(x,y)
		diagonal = self.getDiagonal(x,y,seq1,seq2)

		lowestScore = (float('inf'),None)
		if left[0] < lowestScore[0]:
			lowestScore = left
		if top[0] < lowestScore[0]:
			lowestScore = top
		if diagonal[0] < lowestScore[0]:
			lowestScore = diagonal
		return lowestScore
	
	def getAlignmentStrings(self,x,y,seq1,seq2): #back tracks and returns aligned strings. O(i + j) for time and space for both banded and unbanded. 

		s1 = ""
		s2 = ""
		
		while x != 0 or y != 0:
			if self.table[x,y][1] == (x,y-1): #going left
				s2 = seq2[-1] + s2
				seq2 = seq2[:-1]
				s1 = '-'  + s1
				y = y-1
			elif self.table[x,y][1] == (x-1,y): #going top
				s2 = '-' + s2
				s1 = seq1[-1] + s1
				seq1 = seq1[:-1]
				x = x-1
			elif self.table[x,y][1] == (x-1, y-1): #going diagonal
				s1 = seq1[-1] + s1
				s2 = seq2[-1] + s2
				x = x-1
				y = y-1
				seq1 = seq1[:-1]
				seq2 = seq2[:-1]
		return s1, s2
	

	def align( self, seq1, seq2, banded, align_length): #O(ij) speed and space for unbanded, O(kn) speed and space for banded
		self.banded = banded
		self.MaxCharactersToAlign = align_length
		self.table = {}
		self.loadBaseCases(seq1, seq2) #O(i + j) for unbanded, O(2k + 1) for banded
		if len(seq1)>align_length:
			seq1 = seq1[:align_length]
		if len(seq2)>align_length:
			seq2 = seq2[:align_length]

		for x in range(1,len(seq1) + 1) : #iterates through each row
			if banded: # if banded, only iterates through -k through k, or 2k + 1 at max. 
				min = x - MAXINDELS
				if min < 1:
					min = 1
				max = x + MAXINDELS
				if max > len(seq2):
					max = len(seq2)
				for y in range(min, max + 1):
					self.distFromDiagonal = y-x
					self.table[(x,y)] = self.getLowestScore(x,y,seq1,seq2) 
			else: #iterate through each column when unbanded.
				for y in range(1,len(seq2) + 1):
					self.table[(x,y)] = self.getLowestScore(x,y,seq1,seq2)
		
		if self.table.get((len(seq1),len(seq2))) == None:
			score = float('inf')
			alignment1,alignment2 = "No Alignment Possible","No Alignment Possible"

		else:
			score = self.table[len(seq1), len(seq2)][0]
			alignment1,alignment2 = self.getAlignmentStrings(x,y,seq1,seq2) #O(i + j) on average, best would be O(i) if it was all diagonal. 

		return {'align_cost':score, 'seqi_first100':alignment1[:100], 'seqj_first100':alignment2[:100]}
