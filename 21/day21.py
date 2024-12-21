# type: ignore

import sys
from collections import deque
from functools import cache

with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    codes = [line.strip() for line in f]


num_map = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
}
dir_map = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_paths(start, end, pad):
    rev = {v: k for k, v in pad.items()}
    startpos = pad[start]
    endpos = pad[end]

    to_visit = deque([(startpos, [])])

    while to_visit:
        head, path = to_visit.popleft()
        posx, posy = head

        if head == endpos:
            yield (*path, "A")
            continue

        for other, char in [
            ((posx - 1, posy), "<"),
            ((posx + 1, posy), ">"),
            ((posx, posy - 1), "^"),
            ((posx, posy + 1), "v"),
        ]:
            if other in rev and dist(other, endpos) < dist((posx, posy), endpos):
                to_visit.append((other, path + [char]))


@cache
def score(main_path, levels):
    acc = 0
    loc = "A"
    for target in main_path:
        if levels == 1:
            path = min(find_paths(loc, target, dir_map), key=len)
            acc += len(path)
        else:
            acc += min(score(path, levels - 1) for path in find_paths(loc, target, dir_map))
        loc = target

    return acc


def best_path(levels):
    complexity = 0
    for code in codes:
        acc = 0
        loc = "A"
        for num in code:
            acc += min(score(p, levels=levels) for p in find_paths(loc, num, num_map))
            loc = num

        complexity += acc * int("".join(c for c in code if c.isnumeric()))

    return complexity


if __name__ == "__main__":
    print(best_path(2))
    print(best_path(25))
