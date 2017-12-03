"""Letters permutation"""

from itertools import permutations

word = 'грива'
perms = [''.join(p) for p in permutations(word)]

print(len(set(perms)))

for perm in sorted(set(perms)):
    print(perm)
