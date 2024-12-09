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
    if len(items) == 1:
        return test == items[0]
    if items[0] >= test:
        return False

    return (
        matches(test, [items[0] + items[1], *items[2:]], with_concat)
        or matches(test, [items[0] * items[1], *items[2:]], with_concat)
        or (with_concat and matches(test, [concat(items[0], items[1]), *items[2:]], with_concat))
    )


def check_parts(equation):
    test, items = equation
    if matches(test, items, with_concat=False):
        return test, test
    elif matches(test, items, with_concat=True):
        return 0, test
    return 0, 0


part1 = 0
part2 = 0

for check1, check2 in map(check_parts, equations):
    part1 += check1
    part2 += check2

print("Part 1:", part1)
print("Part 2:", part2)
