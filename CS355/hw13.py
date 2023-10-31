def findContiguousSubSequence(A):
	currSum = 0
	maxSum = None
	currSubSequence = []
	maxSubSequence = []
	for i in A:
		if maxSum is None:
			maxSum = i
		currSum += i
		currSubSequence.append(i)
		if currSum >= maxSum:
			maxSum = currSum
			maxSubSequence = currSubSequence.copy()
		if currSum <= 0:
			currSum = 0
			currSubSequence = []
	return maxSubSequence, maxSum


A = [-5,-10,-10,-20,-40,50,-5,-10,-5,-10,-5,10,5,20,-30]
print(findContiguousSubSequence(A))