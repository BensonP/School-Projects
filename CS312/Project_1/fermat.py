import random


def prime_test(N, k):
    # This is the main function connected to the Test button. You don't need to touch it.
    return run_fermat(N,k), run_miller_rabin(N,k)


def mod_exp(x, y, N):
    if y == 0:
        return 1 
    z = mod_exp(x, y//2, N)
    if y % 2 == 0:
        return z**2 % N
    else:
        return (x * z**2) % N
    

def fprobability(k):
    # You will need to implement this function and change the return value.   
    return (1 - 1/(2**k))


def mprobability(k):
    # You will need to implement this function and change the return value.   
    return  (1 - 3/(4**k))


def run_fermat(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    for i in range(k):
        a = random.randint(1, N - 1)
        if mod_exp(a,N-1,N) ==1:
            return 'prime'
        else:
            return 'composite'
        
print(run_fermat(7,5))
print(fprobability(5))


def run_miller_rabin(N,k):
    for i in range(k):
        a = random.randint(1, N - 1)
        n = N-1
        if  mod_exp(a,n,N) == 1:
            while n % 2 == 0:
                n = n/2
                r = mod_exp(a,n,N)
                if r == N - 1:
                    break
                if r != 1:
                    return 'composite'
                if r == 1 and n % 2 == 1:
                    break
        else:
            return 'composite'
    return 'prime'
    

print(run_miller_rabin(8,1))
print(mprobability(1))
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
