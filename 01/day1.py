from collections import Counter
first = []
second = []
while True:
    try:
        line = input()
    except EOFError:
        break
    a, b = line.split()
    first.append(int(a))
    second.append(int(b))

dist = 0
for a, b in zip(sorted(first), sorted(second)):
    dist += abs(a - b)
print(dist)

similarity = 0
count = Counter(second)
for n in first:
    similarity += n * count[n]
print(similarity)
