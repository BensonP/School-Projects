import random


def prime_test(N, k):
    return run_fermat(N,k), run_miller_rabin(N,k)


def mod_exp(x, y, N): # Time complexity = O(N^3)
    if y == 0:
        return 1 
    z = mod_exp(x, y//2, N)  #Y = N for bit wise, and y // 2 is a bit shift. Therefore, N number of times results in O(N)
    if y % 2 == 0:       # If else block will result in an O(N^2)
        return z**2 % N
    else:
        return (x * z**2) % N
    

def fprobability(k):  
    return (1 - 1/(2**k))


def mprobability(k):
    return  (1 - 1/(4**k))


def run_fermat(N,k): # O(K * N^3)
    for i in range(k): #Ran K number of times, if we consider K large enough to matter. 
        a = random.randint(1, N - 1)
        if mod_exp(a,N-1,N) == 1: #This is O(N^3)
            return 'prime'
        else:
            return 'composite'


def run_miller_rabin(N,k): #Total run time is O(K*log(N)*N^3). Largest dominates, so O(K*N^3)
    for i in range(k): #Ran K number of times
        a = random.randint(1, N - 1)
        n = N-1
        if  mod_exp(a,n,N) == 1:
            while n % 2 == 0: #Ran Log(N-1) number of times, so log(N) This is due to n,
                n = n/2       # the exponent, being divided by 2 each time. 
                r = mod_exp(a,n,N) #Ran N^3 number of times
                if r == N - 1:
                    break
                if r != 1:
                    return 'composite'
                if r == 1 and n % 2 == 1:
                    break
        else:
            return 'composite'
    return 'prime'
