import time
import sys
import os
import heapq
from functools import cache
from collections import defaultdict, Counter

grid = {}
start = (0, 0)
end = (0, 0)
with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line.strip()):
            if char == "E":
                end = x, y
                char = "."
            elif char == "S":
                start = x, y
                char = "."
            grid[x, y] = char

maxx = max(x for x, _ in grid)
maxy = max(y for _, y in grid)


def adjacent(pos):
    x, y = pos
    for other in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if other in grid:
            yield other


def dijkstra_path(start, end):
    seen = set()
    to_visit = [(0, start, [start])]
    while to_visit:
        cost, node, path = heapq.heappop(to_visit)
        if node in seen:
            continue
        seen.add(node)

        if node == end:
            return cost, path

        for other in adjacent(node):
            if other in grid and grid[other] != '#' and other not in seen:
                heapq.heappush(to_visit, (cost + 1, other, path + [other]))

    return None


@cache
def dijkstra(start, end):
    seen = set()
    to_visit = [(0, start)]
    while to_visit:
        cost, node = heapq.heappop(to_visit)
        if node in seen:
            continue
        seen.add(node)

        if node == end:
            return cost

        for other in adjacent(node):
            if other in grid and grid[other] != '#' and other not in seen:
                heapq.heappush(to_visit, (cost + 1, other))

    return None


def dist(point, other):
    return abs(point[0] - other[0]) + abs(point[1] - other[1])


def dijkstra_cheats(start, end, maxcheats=2, target_cost=0):
    seen = set()
    to_visit = [(0, start, (), (start,))]
    while to_visit:
        cost, node, cheats, path = heapq.heappop(to_visit)
        if cost > target_cost:
            return
        # ch = cheats if len(cheats) != 1 else None
        ch = cheats
        if (node, ch) in seen:
            continue
        seen.add((node, ch))

        if node == end:
            if len(cheats) == 1:
                cheats = cheats[0], node
            print(target_cost - cost + 1, cheats)
            yield target_cost - cost + 1
            continue

        # if cheats == ((8, 7),): 
        #     breakpoint()

        available = maxcheats
        if len(cheats) == 1:
            available = maxcheats - dist(node, cheats[0])
        elif len(cheats) == 2:
            available = 0

        for other in adjacent(node):
            if other in path:
                continue
            newcheats = cheats

            if other == end and len(newcheats) == 1 and available == 0:
                continue
            if grid[other] == '#':
                if available <= 0:
                    continue
                if not cheats:
                    newcheats = (node,)
            elif available == 0 and len(cheats) == 1:
                # assert len(cheats) == 1
                newcheats = cheats[0], other

            # if newcheats == ((7,6),):
            #     breakpoint()

            # elif grid[other] != '#' and grid[node] == '#':
            #     newcheats = (cheats[0], other)

            # if (other, newcheats if len(newcheats) != 1 else None) in seen:
            #     continue
            heapq.heappush(to_visit, (cost + 1, other, newcheats, (*path, other)))

    return None

p = dijkstra(start, end)
print(p)

# p = list(dijkstra_cheats(start ,end, 2, p - 1))
p = list(dijkstra_cheats(start ,end, 20, p - 100))
print(Counter(p))
print(len(p))
