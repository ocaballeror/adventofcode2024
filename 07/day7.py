import functools
import operator
import itertools
import sys

from multiprocessing import Pool

equations = []
with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    for line in f:
        test, rest = line.split(":")
        ops = list(map(int, rest.split()))
        equations.append((int(test), ops))


def concat(a, b):
    return int(f"{a}{b}")


def matches(test, items, with_concat=False):
    ops = (operator.add, operator.mul)
    if with_concat:
        ops = (*ops, concat)

    for attempt in itertools.product(ops, repeat=len(items) - 1):
        value = functools.reduce(
            lambda acc, item: item[0](acc, item[1]),
            zip(attempt, items[1:]),
            items[0],
        )
        if value == test:
            return True

    return False


def check_parts(equation):
    test, items = equation
    if matches(test, items, with_concat=False):
        return test, test
    elif matches(test, items, with_concat=True):
        return 0, test
    return 0, 0


part1 = 0
part2 = 0

with Pool() as pool:
    for check1, check2 in pool.imap_unordered(check_parts, equations):
        part1 += check1
        part2 += check2

print("Part 1:", part1)
print("Part 2:", part2)
