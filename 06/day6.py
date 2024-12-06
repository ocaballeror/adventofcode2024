# type: ignore

import sys
import itertools
import multiprocessing
from functools import partial

grid = {}

face = (0, -1)
pos = (0, 0)
with open("input" if len(sys.argv) < 2 else sys.argv[1]) as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line.strip()):
            if char == "^":
                pos = x, y
                char = '.'
            grid[x, y] = char


def move(grid, pos, face):
    x, y = pos
    movex, movey = face
    nxt = x + movex, y + movey
    if nxt not in grid:
        return None, face
    elif grid[nxt] == "#":
        face = {
            (0, -1): (1, 0),
            (1, 0): (0, 1),
            (0, 1): (-1, 0),
            (-1, 0): (0, -1),
        }.get(face)
        return move(grid, pos, face)
    else:
        assert grid[nxt] == ".", grid[nxt]
        return nxt, face


def path(grid, pos, face):
    seen = set()
    while pos:
        seen.add(pos)
        newpos, newface = move(grid, pos, face)
        if newpos is None:
            return seen
        pos, face = newpos, newface


def loops(blockat, pos, face):
    seen = set()
    newgrid = grid.copy()
    newgrid[blockat] = '#'
    while pos:
        if (pos, face) in seen:
            return True
        seen.add((pos, face))
        pos, face = move(newgrid, pos, face)

    return False

def p2(grid, pos, face):
    count = 0
    spots = path(grid, pos, face) - {pos}
    # multiprocessing is not required here, but it does bring the runtime down from 10s to 2s
    with multiprocessing.Pool() as pool:
        func = partial(loops, pos=pos, face=face)
        for res in pool.imap_unordered(func, spots):
            count += res

    return count


print("Part 1:", len(path(grid, pos, face)))
print("Part 2:", p2(grid, pos, face))
