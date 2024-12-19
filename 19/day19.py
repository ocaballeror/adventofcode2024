import sys
from functools import cache

with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    have = []
    need = []
    for line in f:
        line = line.strip()
        if ',' in line:
            have = line.split(', ')
        elif line:
            need.append(line)


@cache
def fill(pattern):
    if not pattern:
        return True

    match = [towel for towel in have if pattern.startswith(towel)]
    if not match:
        return False

    match.sort(key=len, reverse=True)
    return sum(fill(pattern.removeprefix(towel)) for towel in match)


p1 = 0
p2 = 0
for pattern in need:
    ways = fill(pattern)
    if ways:
        p1  += 1
        p2 += ways

print(p1)
print(p2)
