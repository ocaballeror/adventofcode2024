import re
import sys
import heapq

machines = []
with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    a = None
    b = None
    prize = None
    for line in f:
        if "Button A" in line:
            parts = re.search("X\+(\d+), Y\+(\d+)", line).groups()
            a = tuple(map(int, parts))
        if "Button B" in line:
            parts = re.search("X\+(\d+), Y\+(\d+)", line).groups()
            b = tuple(map(int, parts))
        if "Prize" in line:
            parts = re.search("X=(\d+), Y=(\d+)", line).groups()
            prize = tuple(map(int, parts))
            machines.append((a, b, prize))


def dijkstra(target, a, b):
    print(f"find {target=} with {a=}, {b=}")
    targetx, targety = target
    seen = set()
    ax, ay = a
    bx, by = b
    to_visit = [(0, target)]
    while to_visit:
        cost, (tx, ty) = heapq.heappop(to_visit)
        if (tx, ty) in seen:
            continue
        seen.add((tx, ty))

        # print((cost, (tx, ty)))
        if (tx, ty) == (0, 0):
            return cost

        new = (tx - ax, ty - ay)
        if new not in seen and new[0] >= 0 and new[1] >= 0:
            heapq.heappush(to_visit, (cost + 3, new))

        new = (tx - bx, ty - by)
        if new not in seen and new[0] >= 0 and new[1] >= 0:
            heapq.heappush(to_visit, (cost + 1, new))


def cramer(eq1, eq2):
    x1, y1, r1 = eq1
    x2, y2, r2 = eq2

    det = (x1 * y2) - (x2 * y1)
    d1 = r1 * y2 - y1 * r2
    d2 = x1 * r2 - r1 * x2

    return d1 / det, d2 / det


p1 = 0
for a, b, prize in machines:
    cost = dijkstra(prize, a, b)
    p1 += cost or 0
print("part 1:", p1)

p2 = 0
for a, b, prize in machines:
    # this is just a set of equations:
    #  targetx = ax * x + bx * y
    #  targety = ay * x + by * y
    # solve it with cramers rule
    r1, r2 = cramer(
        (a[0], b[0], prize[0] + 10000000000000), (a[1], b[1], prize[1] + 10000000000000)
    )
    if int(r1) == r1 and int(r2) == r2:
        cost = int(r1 * 3 + r2)
        p2 += cost or 0
print("part 2:", p2)
