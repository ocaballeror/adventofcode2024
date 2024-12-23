import sys
from collections import deque, defaultdict
from functools import cache


@cache
def proc(n):
    n = ((n * 64) ^ n) % 16777216
    n = ((n // 32) ^ n) % 16777216
    n = ((n * 2048) ^ n) % 16777216
    return n


with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    numbers = [int(line) for line in f]


def p1():
    acc = 0
    for num in numbers:
        for _ in range(2000):
            num = proc(num)
        acc += num
    return acc


def p2():
    reg = defaultdict(int)
    for num in numbers:
        buffer = ()
        seen = set()
        for _ in range(2000):
            pre = num % 10
            num = proc(num)
            diff = num % 10 - pre

            if len(buffer) < 4:
                buffer = (*buffer, diff)
                continue

            buffer = (*buffer[1:], diff)
            if buffer not in seen:
                seen.add(buffer)
                reg[buffer] += num % 10

    return max(reg.values())

print(p1())
print(p2())
