##My Python file!
##This is a test!

def fibExp(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    if n == 2:
        return 1
    return (fibExp(n-1) + fibExp(n-2) * fibExp(n-3))

print (fibExp(100))

def fabLinear(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    if n == 2:
        return 1
    array = [1,1,1]
    for x in range(3, n + 1):
        array.append(x)
    for x in range(3,n + 1):
        array[x] = array[x-1] + array[x-2] * array[x-3]
    add = (len(array) - 3) *2
    mult = (len(array) - 3) 
    return array[n],add, mult

print(fabLinear(10))