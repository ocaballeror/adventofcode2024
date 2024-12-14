import time
import os
import sys
import itertools

robots = []
with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    for line in f:
        parts = line.split()
        p = parts[0].split("=")[1].split(",")
        v = parts[1].split("=")[1].split(",")
        robots.append(((int(p[0]), int(p[1])), (int(v[0]), int(v[1]))))

    maxx = max([r[0][0] for r in robots]) + 1
    maxy = max([r[0][1] for r in robots]) + 1


def sim_one(pos, vel, seconds=100):
    posx, posy = pos
    velx, vely = vel
    return (
        (posx + (velx * seconds)) % maxx,
        (posy + (vely * seconds)) % maxy
    )


def sim(robots, times=1):
    newrobots = []
    for pos, vel in robots:
        newpos = sim_one(pos, vel, times)
        newrobots.append((newpos, vel))
    return newrobots


def dangerat(robots, iterations=100):
    quads = [0, 0, 0, 0]
    robots = sim(robots, iterations)
    for pos, _ in robots:
        midx = (maxx - 1) // 2
        midy = (maxy - 1) // 2
        if pos[0] > midx:
            if pos[1] > midy:
                quads[3] += 1
            elif pos[1] < midy:
                quads[2] += 1
        elif pos[0] < midx:
            if pos[1] > midy:
                quads[1] += 1
            elif pos[1] < midy:
                quads[0] += 1
    return quads[0] * quads[1] * quads[2] * quads[3]

def draw(robots):
    where = {r[0] for r in robots}
    for y in range(maxy):
        line = ['.' if (x, y) not in where else 'X' for x in range(maxx)]
        print(''.join(line))

def touches(robots):
    count = 0
    for one, other in itertools.combinations(robots, 2):
        one, other = one[0], other[0]
        if abs(one[0] - other[0]) <= 1 or abs(one[1] - other[1]) <= 1:
            count += 1
    return count


def thetree(robots):
    base = touches(robots[::4])
    for it in itertools.count(1):
        robots = sim(robots, 1)
        if touches(robots[::4]) > base * 1.5:
            os.system('clear')
            draw(robots)
            return it


print("Part 1:", dangerat(robots, 100))
print("Part 2 (I think):", thetree(robots))
