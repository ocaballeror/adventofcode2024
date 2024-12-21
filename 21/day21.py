import sys
from collections import deque


with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    codes = [line.strip() for line in f]


num_map = {
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '0': (1, 3),
    'A': (2, 3),
}
dir_map = {
    '^': (1, 0),
    'A': (2, 0),
    '<': (0, 1),
    'v': (1, 1),
    '>': (2, 1),
}

print(codes)


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def howto(start, end, pad):
    rev = {v: k for k, v in pad.items()}
    startpos = pad[start]
    endpos = pad[end]

    to_visit = deque([(startpos, [start])])

    while to_visit:
        head, path = to_visit.popleft()
        posx, posy = head

        if head == endpos:
            yield path
            continue

        for other, char in [
            ((posx - 1, posy), '<'),
            ((posx + 1, posy), '>'),
            ((posx, posy - 1), '^'),
            ((posx, posy + 1), 'v'),
        ]:
            if other in rev and dist(other, endpos) < dist(
                (posx, posy), endpos
            ):
                to_visit.append((other, path + [char]))


main_pad = 'A'
first_pad = 'A'
second_pad = 'A'
complexity = 0
for code in codes[:1]:
    # main_pad = 'A'
    # first_pad = 'A'
    # second_pad = 'A'
    r = []
    for num in code:
        for first in howto(main_pad, num, num_map):
            print(''.join(first))
            for firstchar in first:
                for second in howto(first_pad, firstchar, dir_map):
                    print('    ', ''.join(second))
                    for secondchar in second:
                        best = min(howto(second_pad, secondchar, dir_map), key=len)
                        print('        ', ''.join(best))


# complexity += len(r) * int(''.join(c for c in code if c.isnumeric()))

# print(complexity)
