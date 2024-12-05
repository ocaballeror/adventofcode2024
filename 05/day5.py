# type: ignore

import sys
from collections import defaultdict

pages = []
before = defaultdict(list)

lines = open("input" if len(sys.argv) < 2 else sys.argv[1]).read().splitlines()
for line in lines:
    if "|" in line:
        a, b = line.split("|")
        before[int(b)].append(int(a))
    elif "," in line:
        pages.append(list(map(int, line.split(","))))


def fix(page) -> bool:
    dirty = True
    fixed = False
    while dirty:
        last = None
        dirty = False
        for idx, num in enumerate(page):
            if last is None or last in before[num]:
                last = num
            elif num in before[last]:
                page[idx - 1] = num
                page[idx] = last
                dirty = True
                fixed = True
            else:
                raise RuntimeError
    return fixed


part1 = 0
part2 = 0
for page in pages:
    if fix(page):
        fix(page)
        part2 += page[len(page) // 2]
    else:
        part1 += page[len(page) // 2]

print(part1)
print(part2)
