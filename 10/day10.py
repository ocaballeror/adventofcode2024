import sys
from functools import cache

grid = {}
heads = []
targets = []
with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line.strip()):
            grid[x, y] = int(char) if char.isnumeric() else -1
            if char == '0':
                heads.append((x, y))
            elif char == '9':
                targets.append((x, y))


def adjacent(pos):
    x, y = pos
    for other in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if other in grid:
            yield other

@cache
def pathsto(pos, dest):
    if pos == dest:
        return 1

    return sum(
        pathsto(other, dest)
        for other in adjacent(pos)
        if grid[other] == grid[pos] + 1
    )


part1 = 0
part2 = 0
for head in heads:
    for target in targets:
        new = pathsto(head, target)
        if new:
            part1 += 1
            part2 += new
print(part1)
print(part2)
