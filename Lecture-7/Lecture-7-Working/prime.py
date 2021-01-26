import math

def is_prime(n):

    # numbers less than 2 are not prime so dont check them
    if n < 2:
        return False

    # range of numbers to check if they are prime
    for i in range(2, int(math.sqrt(n)) + 1 ):

        # if (i) modulous is zero return False - not prime
        if n % i == 0:
            return False

    # return True if (i) modulus is not equal to zero - is prime
    return True

