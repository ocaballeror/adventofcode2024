# type: ignore

import sys
import itertools

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


def move(pos, face):
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
        return move(pos, face)
    else:
        assert grid[nxt] == ".", grid[nxt]
        return nxt, face


def path(pos, face):
    seen = set()
    while pos:
        seen.add(pos)
        newpos, newface = move(pos, face)
        if newpos is None:
            return seen
        pos, face = newpos, newface


def loops(pos, face):
    seen = set()
    while pos:
        if (pos, face) in seen:
            return True
        seen.add((pos, face))
        pos, face = move(pos, face)
    if pos is None:
        return False

def blocktheguy(pos, face):
    count = 0
    spots = path(pos, face) - {pos}
    for loc in spots:
        grid[loc] = '#'
        if loops(pos, face):
            count += 1
        grid[loc] = '.'
    return count


print("Part 1:", len(path(pos, face)))
print("Part 2:", blocktheguy(pos, face))
