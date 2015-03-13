import itertools
import math

# coil number : side length
# 1: 2
# 2: 4
# 3: 6
# generalized: (2n) for n > 1, where n is coil number
# corners can be found on: s + l, s + 2l, s + 3l and s + 4l
# where s is position in coil so far, and l is side length.
# ex:
# for coil 2, s is 1 and l is 2
# first corner is 1 + 2 = 3
# second corner is 1 + 4 = 5
# third corner is 1 + 6 = 7
# fourth corner is 1 + 8 = 9
# for coil 3, s is 9 (the last corner of the previous coil) and l is 4
# first corner is 9 + 4 = 13
# second corner is 9 + 8 = 17
# third corner is 9 + 12 = 21
# fourth corner is 9 + 16 = 25
# this is consistent with the example given in the problem.

# first we need to find s for a given coil number.
# looking at the example we have
# coil number : s
# 1 : 1
# 2 : 9
# 3 : 25
# 4 : 49
# these are the squares of odd numbers
# generalized: (2n - 1)^2 for n > 1, where n is coil number


def find_s(n):
    return (2 * n - 1) ** 2


def side_length(n):
    return 2 * n


def get_corners(n):
    s = find_s(n)
    l = side_length(n)

    return (s + l), (s + 2 * l), (s + 3 * l), (s + 4 * l)

# and now to generate corners for n up to 4 and compare with the example in the problem

corners = []
for i in range (1, 4):
    corners.append(get_corners(i))

print(corners)
# output: [(3, 5, 7, 9), (13, 17, 21, 25), (31, 37, 43, 49)]
# this is correct but missing the 1 in the middle of the spiral, we'll adjust for that later

# to compute the ratio, we need to know which numbers are actually prime
# let's implement this primality test:
# http://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Deterministic_variants_of_the_test
def is_prime(n):
    if n < 2:
        return False

    # write n−1 as 2s·d by factoring powers of 2 from n−1
    s = 0
    d = n-1
    while d & 1 == 0:
        s += 1
        d >>= 1

    # assume hat we don't need primes > ~4.7 billion
    for a in [2, 7, 61]:
        if not 2 <= a <= min(n - 1, int(2 * math.log(n) ** 2)):
            break
        if (pow(a, d, n) != 1):
            if (all(pow(a, 2 ** r * d, n) != (n - 1) for r in range(0, s))):
                return False
    return True


# some tests based on the examples in the problem
print(is_prime(13))
# output: True
print(is_prime(25))
# output: False
print(is_prime(43))
# output: True
print(is_prime(49))
# output: False

# this looks correct

# initialize nonprimes to 1 to account for the 1 in the middle of the spiral
primes = 0
nonprimes = 1
def ratio(corners):
    global primes
    global nonprimes

    for n in corners:
        if (is_prime(n)):
            primes += 1
        else:
            nonprimes += 1

    return primes / (nonprimes + primes)

# testing it with the corners we found earlier
for i in range(1, 4):
    print(ratio(get_corners(i)))
# output: 0.6153...
# this is consistent with the example given in the problem

# so now we just need to test for bigger and bigger spirals until ratio < 0.1
# there's one more caveat though,we've defined side length to be the circumference / 4
# to make it easy to compute the corners, since they are now exactly 1 side length from each other.
# however a side really has two corners, so we simply add 1 to the final answer

# initialize nonprimes to 1 to account for the 1 in the middle of the spiral
primes = 0
nonprimes = 1
coil = 1
while(True):
    if (ratio(get_corners(coil)) < 0.1):
        print(side_length(coil) + 1)
        break
    coil += 1
# output: 26241, the correct answer!
