import itertools
grid = {}

for y in itertools.count():
    try:
        for x, char in enumerate(input().strip()):
            grid[x, y] = char
    except EOFError:
        break

def adjacent(pos):
    x, y = pos
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
    for dirx, diry in dirs:
        movex, movey = pos
        acc = []
        while True:
            movex += dirx
            movey += diry
            move = movex, movey
            if move in grid:
                acc.append( grid[move])
            else:
                break
        yield ''.join(acc)

def equis(pos):
    x, y = pos
    diag1 = [(x-1, y-1), (x, y), (x+1, y+1)]
    diag2 = [(x+1, y-1), (x, y), (x-1, y+1)]
    line1 = ''.join([grid.get(move, '') for move in diag1])
    line2 = ''.join([grid.get(move, '') for move in diag2])
    if len(line1) == len(line2) == 3:
        return line1, line2
    return None


part1 = 0
part2 = 0
for pos, letter in grid.items():
    if letter == 'X':
        for other in adjacent(pos):
            if other.startswith('MAS'):
                part1 += 1
    if letter == 'A':
        diags = equis(pos)
        if diags and (diags[0] == 'MAS' or diags[0] == 'SAM')and (diags[1] == 'MAS' or diags[1] == 'SAM'):
            part2 += 1
            
print(part1)
print(part2)
