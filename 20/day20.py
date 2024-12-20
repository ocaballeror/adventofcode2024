import time
import sys
import os
import heapq
from functools import cache
from collections import defaultdict, deque, Counter

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


def adjacent(pos, dist=1):
    for x in range(-dist, dist + 1):
        y = dist - abs(x)
        other = pos[0] + x, pos[1] + y
        if other in grid and grid[other] == '.':
            yield other
        if y != 0:
            other = pos[0] + x, pos[1] - y
            if other in grid and grid[other] == '.':
                yield other


def distance(pos, other):
    return abs(pos[0] - other[0]) + abs(pos[1] - other[1])


def bfs(start, end):
    head = start
    path = [start]
    # set copy of path for faster lookups
    seen = {start}

    while head != end:
        others = [pos for pos in adjacent(head) if pos not in seen]
        assert len(others) == 1
        head = others[0]
        path.append(others[0])
        seen.add(others[0])

    return path


def cheat(path, maxcheats, threshold):
    # dict copy of path for faster lookups
    pathidx = {pos: idx for idx, pos in enumerate(path)}

    count = 0
    for cheats in range(2, maxcheats + 1):
        for idx, pos in enumerate(path):
            for other in adjacent(pos, cheats):
                otheridx = pathidx[other]
                if otheridx >= idx + cheats + threshold:
                    count += 1

    return count



if __name__ == "__main__":
    path = bfs(start, end)

    print(cheat(path, 2, 100))
    print(cheat(path, 20, 100))
