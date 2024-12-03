import re
program = ""
while True:
    try:
        program += input().strip()
    except EOFError:
        break

total = 0
for a, b in re.findall(r"mul\((\d+),(\d+)\)", program):
    total += int(a) * int(b)
print(total)

enabled = True
total = 0
for op, arg1, arg2, _, _ in re.findall(r"(mul\((\d+),(\d+)\)|don't()|do())", program):
    if op == "don't":
        enabled = False
    elif op == "do":
        enabled = True
    else:
        if enabled:
            total += int(arg1) * int(arg2)
print(total)
