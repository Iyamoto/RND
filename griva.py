"""Letters permutation"""

from itertools import permutations

word = 'грива'
perms = [''.join(p) for p in permutations(word)]

for perm in perms:
    print(perm)
