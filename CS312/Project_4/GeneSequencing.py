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

	def getLeft(self,x,y):
		return (self.table[(x,y-1)][0] + 5,(x,y-1))
	
	def getTop(self,x,y):
		return (self.table[(x-1, y)][0] + 5,(x-1,y))
	
	def getDiagonal(self,x,y,seq1,seq2):
		if seq1[x-1] == seq2[y-1]:
			return (self.table[(x-1,y-1)][0] - 3,(x-1,y-1))
		else: return(self.table[(x-1,y-1)][0] + 1,(x-1,y-1))

	
	def loadBaseCases(self,seq1,seq2):
		self.table[(0,0)] = 0,None
		for j in range(1,len(seq1)+1) :
			self.table[(j,0)] = 5*j + self.table[0,0][0],None
		for i in range(1,len(seq2)+1):
			self.table[(0,i)] = 5*i + self.table[0,0][0],None

	def getLowestScore(self,x,y,seq1,seq2):
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
	
	def getAlignmentStrings(self,x,y,seq1,seq2):
		seq1 = list(seq1)
		seq2 = list(seq2)
		s1 = ""
		s2 = ""
		while x != 0 and y != 0:
			if self.table[x,y][1] == (x,y-1): #going left
				s1 = s1 + seq1.pop()
				s2 = s2 + '-'
				y = y-1
			elif self.table[x,y][1] == (x-1,y): #going top
				s1 = s1 + '-'
				s2 = s2 + seq2.pop()
				x = x-1
			elif self.table[x,y][1] == (x-1, y-1): #going diagonal
				s1 = s1 + seq1.pop()
				s2 = s2 + seq2.pop()
				x = x-1
				y = y-1
		return s1, s2
	

# This is the method called by the GUI.  _seq1_ and _seq2_ are two sequences to be aligned, _banded_ is a boolean that tells
# you whether you should compute a banded alignment or full alignment, and _align_length_ tells you
# how many base pairs to use in computing the alignment

	def align( self, seq1, seq2, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length
		self.table = {}
		self.loadBaseCases(seq1, seq2)
		if len(seq1)>align_length:
			seq1 = seq1[:align_length]
		if len(seq2)>align_length:
			seq2 = seq2[:align_length]

		for x in range(1,len(seq1) + 1) :
			for y in range(1,len(seq2) + 1):
				self.table[(x,y)] = self.getLowestScore(x,y,seq1,seq2)
		
		#print(self.table)

###################################################################################################
# your code should replace these three statements and populate the three variables: score, alignment1 and alignment2
		score = self.table[len(seq1), len(seq2)][0]
		alignment1,alignment2 = self.getAlignmentStrings(x,y,seq1,seq2)
		#alignment1 = 'abc-easy  DEBUG:({} chars,align_len={}{})'.format(
		#	len(seq1), align_length, ',BANDED' if banded else '')
		#alignment2 = 'as-123--  DEBUG:({} chars,align_len={}{})'.format(
		#	len(seq2), align_length, ',BANDED' if banded else '')
		
###################################################################################################

		return {'align_cost':score, 'seqi_first100':alignment1, 'seqj_first100':alignment2}
