import sys
from functools import cache
from collections import Counter

with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    stones = list(map(int, f.read().split()))


def split(stone):
    strstone = str(stone)
    if stone == 0:
        return (1,)
    elif len(strstone) % 2 == 0:
        return (
            int(strstone[: len(strstone) // 2]),
            int(strstone[len(strstone) // 2 :]),
        )
    else:
        return (stone * 2024,)


def blink(stones, times):
    for _ in range(times):
        newstones = []
        for each in stones:
            newstones.extend(split(each))
        stones = newstones

    return len(stones)


def smartblink(stones, times):
    stones = Counter(stones)
    for _ in range(times):
        newstones = Counter()
        for unique, count in stones.items():
            others = split(unique)
            for x in others:
                newstones[x] += count

        stones = newstones

    return sum(stones.values())


print("Part 1:", blink(stones, 25))
print("Part 2:", smartblink(stones, 75))
