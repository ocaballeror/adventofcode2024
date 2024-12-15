import time
import sys
import os

grid = {}
directions = []
robot = (0, 0)
with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    for y, line in enumerate(f):
        if line.startswith("#"):
            line = (
                line.strip()
                .replace("#", "##")
                .replace(".", "..")
                .replace("O", "[]")
                .replace("@", "@.")
            )
            for x, char in enumerate(line):
                if char == "@":
                    robot = x, y
                    char = "."
                grid[x, y] = char
        elif line:
            directions.extend(line.strip())

maxx = max(x for x, _ in grid)
maxy = max(y for _, y in grid)


def move(thing, direc, handlematching=True):
    x, y = thing
    if handlematching and grid[thing] in "[]":
        mefirst = False
        if grid[thing] == "[":
            matching = x + 1, y
            assert grid[matching] == "]"
            mefirst = direc == "<"
        elif grid[thing] == "]":
            matching = x - 1, y
            assert grid[matching] == "["
            mefirst = direc == ">"

        if mefirst:
            if thing != (newthing := move(thing, direc, False)):
                if matching != (newmatching := move(matching, direc, False)):
                    return newthing
        else:
            if matching != (newmatching := move(matching, direc, False)):
                if thing != (newthing := move(thing, direc, False)):
                    return newthing
        return thing

    other = {
        "<": (x - 1, y),
        "^": (x, y - 1),
        ">": (x + 1, y),
        "v": (x, y + 1),
    }[direc]

    if grid[other] == "#":
        return thing

    if grid[other] in "[]":
        newother = move(other, direc)
        if newother == other:
            return thing

    if grid[other] == ".":
        grid[other] = grid[thing]
        grid[thing] = "."
        return other

    return thing


def draw():
    pre = grid[robot]
    grid[robot] = "@"

    for y in range(maxy + 1):
        line = "".join(grid[x, y] for x in range(maxx + 1))
        print(line)

    grid[robot] = pre


for direc in directions:
    pre = grid.copy()
    newrobot = move(robot, direc)
    if newrobot == robot:
        grid = pre.copy()
    else:
        robot = newrobot
    # os.system('clear')
    # draw()
    # print()
    # print("Move:", direc)
    # time.sleep(.1)

draw()
gps = 0
print(f"{maxx=}, {maxy=}")
for (x, y), char in grid.items():
    if char == "[":
        gps += x + y * 100

print("Part 2:", gps)
