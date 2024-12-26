# type: ignore
import sys

state = {}
operations = {}
with open(sys.argv[1] if len(sys.argv) > 1 else "input") as f:
    for line in f:
        if ":" in line:
            gate, value = line.split(":")
            state[gate] = int(value)
        elif "->" in line:
            inp, out = line.strip().split(" -> ")
            one, op, other = inp.split()
            assert out not in operations
            operations[out] = (op, (one, other))


def run(operations, state):
    operations = operations.copy()
    state = state.copy()
    while operations:
        for out, (op, (one, other)) in list(operations.items()):
            if one in state and other in state:
                if op == "AND":
                    val = state[one] & state[other]
                elif op == "OR":
                    val = state[one] | state[other]
                elif op == "XOR":
                    val = state[one] ^ state[other]
                assert out not in state
                state[out] = val
                operations.pop(out)

    return operations, state


def assemble(state, key="z"):
    zs = sorted((k for k in state if k.startswith(key)), reverse=True)
    out = "".join(map(str, (state[key] for key in zs)))
    return out


def p1():
    _, newstate = run(operations, state)
    val = int(assemble(newstate), base=2)
    return val


def equation(nbits):
    if nbits == 0:
        return ("XOR", ("x00", "y00"))

    first = ("XOR", (f"x{nbits:02}", f"y{nbits:02}"))
    second = ("AND", (f"x{nbits-1:02}", f"y{nbits-1:02}"))
    if nbits > 1:
        pre = equation(nbits - 1)
        assert pre[0] == "XOR"
        pre = ("AND", *pre[1:])
        third = ("OR", (second, pre))
    else:
        third = second
    return ("XOR", (first, third))


def adjust(eq):
    op, (one, two) = eq
    rev = (op, (two, one))

    if isinstance(one, str):
        assert one.startswith("x") or one.startswith("y")
        assert isinstance(two, str)
        assert two.startswith("x") or two.startswith("y")

    else:
        one = adjust(one)
        two = adjust(two)
        eq = (op, (one, two))
        rev = (op, (two, one))

    try:
        key = next(k for k in operations if operations[k] == eq or operations[k] == rev)
    except StopIteration:
        breakpoint()
        raise
    return key


def expand(op):
    if op.startswith("x") or op.startswith("y"):
        return op

    how, (one, two) = operations[op]
    return (how, (expand(one), expand(two)))


if __name__ == "__main__":
    print(p1())

    # this one requires manual debugging. basically build the equation for every bit in the input,
    # map it to the existing gates and see if it matches. if the output does not match the expected
    # z gate then something is wrong, so look through the input to see what.
    # Fortunately they are usually close to the z layer so they are pretty easy to spot.

    operations["kmb"], operations["z10"] = operations["z10"], operations["kmb"]
    operations["tvp"], operations["z15"] = operations["z15"], operations["tvp"]
    operations["dpg"], operations["z25"] = operations["z25"], operations["dpg"]
    operations["mmf"], operations["vdk"] = operations["vdk"], operations["mmf"]

    for i in range(len([k for k in operations if k.startswith('z')]) - 1):
        if not (adjust(equation(i))).startswith("z"):
            breakpoint()
            assert adjust(equation(i))
