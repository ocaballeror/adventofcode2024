# type: ignore

import itertools
import sys

with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    readlock = False
    readkey = False
    locks = []
    keys = []
    for line in f:
        line = line.strip()
        if not line:
            readlock = False
            readkey = False
            continue

        if not readlock and not readkey:
            if set(line) == {"#"}:
                readlock = True
                locks.append([0] * len(line))
            else:
                readkey = True
                keys.append([-1] * len(line))
        elif readlock:
            for idx, col in enumerate(line):
                locks[-1][idx] += col == "#"
        elif readkey:
            for idx, col in enumerate(line):
                keys[-1][idx] += col == "#"

count = sum(
    not any(one + other >= 6 for one, other in zip(key, lock))
    for key, lock in itertools.product(keys, locks)
)
print(count)
