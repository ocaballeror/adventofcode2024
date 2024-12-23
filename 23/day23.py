# type: ignore
import sys
from collections import defaultdict


connections = defaultdict(set)
with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    for line in f:
        one, other = line.strip().split("-")
        connections[one].add(other)
        connections[other].add(one)


def p1():
    here = set()
    for key, others in connections.items():
        if key.startswith("t"):
            for other in others:
                for third in connections[other]:
                    if key != other != third and third in connections[key]:
                        here.add(tuple(sorted((key, other, third))))
    return len(here)


def inter(here):
    if len(here) == 1:
        return here

    for thing in here:
        new = here.intersection(connections[thing])
        if new:
            return {thing} | inter(new)
    return set()


def p2():
    best = max(connections, key=lambda key: len(inter(connections[key])))
    sol = ",".join(sorted({best, *inter(connections[best])}))
    return sol


if __name__ == "__main__":
    print(p1())
    print(p2())
