# type: ignore

import sys

grid = {}
with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line.strip()):
            grid[x, y] = char


def adjacent(pos):
    x, y = pos
    for other in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        yield other


def angles(point):
    corners = 0
    char = grid[point]
    x, y = point
    for other1, other2 in [
        ((x + 1, y), (x, y + 1)),
        ((x + 1, y), (x, y - 1)),
        ((x - 1, y), (x, y + 1)),
        ((x - 1, y), (x, y - 1)),
    ]:
        if grid.get(other1) != char and grid.get(other2) != char:
            corners += 1
        if grid.get(other1) == grid.get(other2) == char != grid.get((other1[0], other2[1])):
            corners += 1
    return corners


def fence(point, seen):
    perim = 0
    area = 1
    discounted = angles(point)
    seen.add(point)
    for other in adjacent(point):
        if grid.get(other) != grid[point]:
            perim += 1
        elif other not in seen:
            a, b, c = fence(other, seen)
            area += a
            perim += b
            discounted += c

    return area, perim, discounted


seen = set()
part1 = 0
part2 = 0
for pos, val in grid.items():
    if pos in seen:
        continue
    area, perim, discounted = fence(pos, seen)
    part1 += perim * area
    part2 += discounted * area

print("Part 1:", part1)
print("Part 2:", part2)
