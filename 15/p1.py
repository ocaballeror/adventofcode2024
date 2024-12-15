import time
import sys
import os

grid = {}
directions = []
robot = (0, 0)
with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    for y, line in enumerate(f):
        if line.startswith("#"):
            for x, char in enumerate(line.strip()):
                if char == "@":
                    robot = x, y
                    char = "."
                grid[x, y] = char
        elif not line.strip():
            pass
        else:
            directions.extend(line.strip())


def move(thing, direc):
    x, y = thing
    other = {
        "<": (x - 1, y),
        "^": (x, y - 1),
        ">": (x + 1, y),
        "v": (x, y + 1),
    }[direc]
    if grid[other] == "#":
        return thing
    if grid[other] == "O":
        move(other, direc)

    if grid[other] == ".":
        grid[other] = grid[thing]
        grid[thing] = "."
        return other
    return thing


def draw():
    pre = grid[robot]
    grid[robot] = '@'

    maxx = max(x for x, _ in grid)
    maxy = max(y for _, y in grid)

    for y in range(maxy + 1):
        line = ''.join(grid[x,y] for x in range(maxx + 1))
        print(line)

    grid[robot] = pre

for new in directions:
    robot = move(robot, new)
    # os.system('clear')
    # draw()
    # print()
    # print("Move:", new)
    # time.sleep(1)

gps = 0
for (x, y), char in grid.items():
    if char == 'O':
        gps += y * 100 + x
print('Part 1:', gps)
