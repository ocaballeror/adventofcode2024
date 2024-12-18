import time
import sys
import os
import heapq
import bisect

if len(sys.argv) > 1:
    fname = sys.argv[1]
else:
    fname = "input"

blocks = []
with open(fname) as f:
    for line in f:
        a, b = line.split(',')
        blocks.append((int(a), int(b)))
maxx = max(x for x, _ in blocks)
maxy = max(y for _, y in blocks)


def dijkstra(blocks):
    seen = set()
    to_visit = [(0, (0, 0))]
    while to_visit:
        cost, (tx, ty) = heapq.heappop(to_visit)
        if (tx, ty) in seen:
            continue
        seen.add((tx, ty))

        # print((cost, (tx, ty)))
        if (tx, ty) == (maxx, maxy):
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


if fname == "test":
    nbytes = 12
elif fname == "input":
    nbytes = 1024
else:
    raise ValueError("Unknown number of bytes")

p1 = dijkstra(blocks[:nbytes])
print(p1)

p2 = bisect.bisect(blocks, False, key=lambda at: dijkstra(set(blocks[:blocks.index(at) + 1])) is None)
print(blocks[p2])
