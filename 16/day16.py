import time
import sys
import os
import heapq
from collections import defaultdict

grid = {}
deer = (0, 0)
end = (0, 0)
with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line.strip()):
            if char == "E":
                end = x, y
                char = "."
            elif char == "S":
                deer = x, y
                char = "."
            grid[x, y] = char


def dijkstra(start, end):
    seen = defaultdict(set)
    best = None
    tiles = set()
    to_visit = [(0, start, ">", {start})]

    while to_visit:
        cost, (x, y), face, path = heapq.heappop(to_visit)

        if best is not None and cost > best:
            return best, tiles

        if (x, y) == end:
            best = cost
            tiles.update(path)

        if path <= seen[x, y, face]:
            continue

        seen[x, y, face].update(path)

        if face == ">":
            other = x + 1, y
            rotates = "^v"
        elif face == "v":
            other = x, y + 1
            rotates = "<>"
        elif face == "<":
            other = x - 1, y
            rotates = "^v"
        else:
            assert face == "^"
            other = x, y - 1
            rotates = "<>"

        if grid[other] == ".":
            new = path | {other}
            if not new.issubset(seen[x, y, face]):
                heapq.heappush(to_visit, (cost + 1, other, face, new))

        for newface in rotates:
            if not path.issubset(seen[x, y, newface]):
                heapq.heappush(to_visit, (cost + 1000, (x, y), newface, path))


cost, path = dijkstra(deer, end)
print("Part 1:", cost)
print("Part 2:", len(path))
