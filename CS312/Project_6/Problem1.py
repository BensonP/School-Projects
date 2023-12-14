class Solution(object):
    def tribonacci(self, n):
        """
        :type n: int
        :rtype: int
        """
        numbers = [0,1,1]

        if n < 3:
            return numbers[n]

        for i in range( n + 1):
            numbers[0], numbers[1], numbers[2] = numbers[1], numbers[2], sum(numbers)
        return numbers[2]

Sol = Solution.tribonacci(5,5)


print(Sol)