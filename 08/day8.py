import sys
import itertools
from collections import defaultdict


with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    antennas = defaultdict(list)
    for y, line in enumerate(f):
        for x, char in enumerate(line.strip()):
            if char != '.':
                antennas[char].append((x, y))
        maxx = x
    maxy = y

def antinodes(antennas, infinite=False):
    antinodes = set()
    for name, nodes in antennas.items():
        for (onex, oney), (otherx, othery) in itertools.combinations(nodes, r=2):
            for level in (itertools.count(0) if infinite else [2]):
                changed = False
                an1 = onex - (onex - otherx) * level, oney - (oney - othery) * level
                an2 = otherx - (otherx - onex) * level, othery - (othery - oney) * level
                if 0 <= an1[0] <= maxx and 0 <= an1[1] <= maxy:
                    antinodes.add(an1)
                    changed = True
                if 0 <= an2[0] <= maxx and 0 <= an2[1] <= maxy:
                    antinodes.add(an2)
                    changed = True
                if not changed:
                    break
    return antinodes

print('Part 1:', len(antinodes(antennas, False)))
print('Part 2:', len(antinodes(antennas, True)))
