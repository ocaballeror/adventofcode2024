import sys

reg = {"a": 0, "b": 0, "c": 0}

with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    linea, lineb, linec, _, code = f.readlines()
    reg["a"] = int(linea.split(":")[1])
    reg["b"] = int(lineb.split(":")[1])
    reg["c"] = int(linec.split(":")[1])
    program = list(map(int, code.split(":")[1].split(",")))


def combo(arg):
    if arg == 4:
        arg = reg["a"]
    elif arg == 5:
        arg = reg["b"]
    elif arg == 6:
        arg = reg["c"]
    return arg


def run():
    pc = 0
    buffer = []
    while pc < len(program):
        jumped = False
        inst = program[pc]
        arg = program[pc + 1]

        if inst == 0:
            reg["a"] = reg["a"] // 2 ** combo(arg)
        elif inst == 1:
            reg["b"] = reg["b"] ^ arg
        elif inst == 2:
            reg["b"] = combo(arg) % 8
        elif inst == 3:
            if reg["a"] != 0:
                pc = arg
                jumped = True
        elif inst == 4:
            reg["b"] = reg["b"] ^ reg["c"]
        elif inst == 5:
            buffer.append(combo(arg) % 8)
        elif inst == 6:
            reg["b"] = reg["a"] // 2 ** combo(arg)
        elif inst == 7:
            reg["c"] = reg["a"] // 2 ** combo(arg)

        if not jumped:
            pc += 2

    return buffer

def rev_engineer():
    pre = reg.copy()
    res = "X" * len(program)
    i = 0
    for idx in range(1, len(program) + 1):
        while res[-idx] != program[-idx]:
            i += 2 ** ((len(program) - idx) * 3)
            reg.update(pre)
            reg["a"] = i
            res = run()

    assert res == program
    return i

print("Part 1:", ",".join(map(str, run())))
print("Part 2:", rev_engineer())
