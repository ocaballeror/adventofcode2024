def safe(report):
    last = None
    incr = None
    for level in report:
        if last is None:
            last = level
            continue
        if level == last:
            return False
        newincr = level > last
        if incr is None:
            incr = newincr
        elif incr != newincr:
            return False

        if abs(level - last) > 3:
            return False
        last = level
        
    return True


def safe2(report):
    if safe(report):
        return True

    for idx in range(len(report)):
        copy = report.copy()
        copy.pop(idx)
        if safe(copy):
            return True
    return False

part1 = 0
part2 = 0
while True:
    try:
        line = input()
    except EOFError:
        break

    report = list(map(int, line.split()))

    part1 += safe(report)
    part2 += safe2(report)

print(part1)
print(part2)
