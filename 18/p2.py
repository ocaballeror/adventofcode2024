import time
import sys
import os
import heapq

if len(sys.argv) > 1:
    fname = sys.argv[1]
else:
    fname = "input"

if fname == "test":
    nbytes = 12
elif fname == "input":
    nbytes = 1024
else:
    raise ValueError("Unknown number of bytes")

blocks = []
with open(fname) as f:
    for line in f:
        a, b = line.split(',')
        blocks.append((int(a), int(b)))
maxx = max(x for x, _ in blocks)
maxy = max(y for _, y in blocks)

grid = {(x, y): '.' for y in range(maxy + 1) for x in range(maxx + 1)}


def dijkstra(start, target, blocks):
    seen = set()
    to_visit = [(0, start)]
    while to_visit:
        cost, (tx, ty) = heapq.heappop(to_visit)
        if (tx, ty) in seen:
            continue
        seen.add((tx, ty))

        # print((cost, (tx, ty)))
        if (tx, ty) == target:
            return cost

        for other in [(tx - 1, ty), (tx + 1, ty), (tx, ty - 1), (tx, ty + 1)]:
            if (
                0 <= other[0] <= maxx
                and 0 <= other[1] <= maxy
                and other not in blocks
                and other not in seen
            ):
                heapq.heappush(to_visit, (cost + 1, other))

    return None


def test(at):
    return dijkstra((0, 0), (maxx, maxy), set(blocks[:blocks.index(at) + 1])) is None


import bisect

r = bisect.bisect(blocks, False, key=test)
print(r, blocks[r])
#
# while dijkstra((0, 0), (maxx, maxy)):
#     grid[blocks[nbytes]] = '#'
#     nbytes += 1
# print(blocks[nbytes - 1])
