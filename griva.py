"""Letters permutation"""

from itertools import permutations
import os

word = 'грива'

# Get permutations
perms = [''.join(p) for p in permutations(word)]
print(len(set(perms)))

# Load Russian wordlist
with open(os.path.join('data', 'zaliznjak_forms.txt')) as word_file:
    words = set(word.strip().lower() for word in word_file)

print(words)

for perm in sorted(set(perms)):
    print(perm)
