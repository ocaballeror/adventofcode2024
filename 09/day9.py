import sys

with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    diskmap = f.read().strip()

def group(diskmap):
    files = []
    space = []
    empty = False
    pointer = 0
    fileidx = 0
    for char in diskmap:
        if not empty:
            files.append((fileidx, int(char), pointer))
            fileidx += 1
        else:
            space.append((int(char), pointer))

        pointer += int(char)
        empty = not empty

    return files, space

def expand(diskmap):
    expanded = []
    empty = False
    fileidx = 0
    for char in diskmap:
        expanded.extend([fileidx if not empty else None for _ in range(int(char))])

        if not empty:
            fileidx += 1
        empty = not empty

    return expanded

def checksum(expanded):
    it = enumerate(expanded)
    revit = reversed(expanded)
    consumed = 0

    checksum = 0
    while True:
        try:
            idx, num = next(it)
        except StopIteration:
            break
        if num is None:
            while (num := next(revit)) is None:
                consumed += 1
            consumed += 1
        else:
            if idx >= len(expanded) - consumed:
                break
        checksum += idx * num

    return checksum


def defrag(diskmap):
    files, spaces = group(diskmap)
    newfiles = expand(diskmap)

    for fileidx, filesize, filepos in reversed(files):
        for spaceidx, (spacesize, spacepos) in enumerate(spaces):
            if spacepos >= filepos:
                break
            if spacesize >= filesize:
                for idx in range(filesize):
                    newfiles[spacepos + idx] = fileidx
                    newfiles[filepos + idx] = None
                spaces[spaceidx] = (spacesize - filesize, spacepos + filesize)
                break

    checksum = 0
    for idx, num in enumerate(newfiles):
        if num:
            checksum += idx * num

    return checksum


print('Part 1:', checksum(expand(diskmap)))
print('Part 2:', defrag(diskmap))
