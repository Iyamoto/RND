# Checking optimal stopping theory

import random
import collections

def genpool(size):
    """Generate pool of candidates"""
    pool = list()
    for i in range(size):
        pool.append(random.randrange(1, 100))
    return pool



def comparecandidates(c1, c2):
    """Compare candidates"""
    if c1>=c2:
        return c1
    else:
        return c2

def getbest(pool, size):
    """Return the best candidate from a given pool"""
    thebest = pool[0]
    for i in range(round(size)):
        thebest = comparecandidates(pool[i], thebest)
    return (i, thebest)


# Choose the best candidate
limit = 0.37 # Magic 37%
size = 100

qualitydata = collections.defaultdict(int)

for c in range(100):
    # Generate pool of candidates
    pool = genpool(size)

    # Learn first
    index, thebest = getbest(pool, round(size*limit))
    # print('The best from learning phase:', index, thebest)

    # Get the best with stopping strategy
    for i in range(round(size*limit), size):
        if pool[i] >= thebest:
            thebest = pool[i]
            index = i
            break

    # print('The best with stopping:', index, thebest)

    # Find absolute best candidate
    absoluteindex, absolutebest = getbest(pool, size)
    # print('The best from whole pool:', absoluteindex, absolutebest)
    quality = round(thebest/absolutebest,2)
    qualitydata[quality] += 1
    # print(round(index/absoluteindex,2), quality)

print(qualitydata)
