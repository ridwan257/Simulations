from lib.utils import to_string
from lib.templates import neuralnet as nn


inputs1 = [
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
    [1, 0, 1],
    [1, 1, 0],
    [1, 1, 1]
]

outputs1 = [
    [0, 0],
    [1, 0],
    [1, 0],
    [0, 1],
    [1, 0],
    [0, 1],
    [0, 1],
    [1, 1]
]

xorI = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
]

xorO = [
    [0],
    [1],
    [1],
    [0]
]

or_gateI = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
]

or_gateO = [
    [0],
    [1],
    [1],
    [1]
]

and_gateI = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
]

and_gateO = [
    [0],
    [0],
    [0],
    [1]
]

not_gateI = [
    [0],
    [1]
]

not_gateO = [
    [1],
    [0]
]

# brain.summary()


inputs = and_gateI
outputs = and_gateO


# brain = nn.Perceptron(1)

# for inp, out in zip(inputs, outputs):
#     res = brain.think(inp)
#     print(f'{inp} -> {out} | {nn.binary(res)} | {to_string(res, 6)}')

# for i in range(100_000):
#     j = nn.np.random.randint(0, len(inputs))
#     brain.train(inputs[j], outputs[j])

# print('after training...')




# for inp, out in zip(inputs, outputs):
#     res = brain.think(inp)
#     print(f'{inp} -> {out} | {nn.binary(res)} | {to_string(res, 6)}')

# brain.save('./not_gate.nn')

and_gate = nn.Perceptron.load_from_file('and_gate.nn')
or_gate = nn.Perceptron.load_from_file('or_gate.nn')
not_gate = nn.Perceptron.load_from_file('not_gate.nn')



# and_gate = nn.Perceptron(2)
# or_gate = nn.Perceptron(2)
# not_gate = nn.Perceptron(1)

# # -----------------or gate training -----------------
# for i in range(10_000):
#     j = nn.np.random.randint(0, len(or_gateI))
#     or_gate.train(or_gateI[j], or_gateO[j])
# or_gate.summary('OR GATE')
# for inp, out in zip(or_gateI, or_gateO):
#     res = or_gate.think(inp)
#     print(f'{inp} -> {out} | {nn.binary(res)} | {to_string(res, 6)}')

# # -----------------and gate training -----------------
# for i in range(10_000):
#     j = nn.np.random.randint(0, len(and_gateI))
#     and_gate.train(and_gateI[j], and_gateO[j])
# and_gate.summary('AND GATE')
# for inp, out in zip(and_gateI, and_gateO):
#     res = and_gate.think(inp)
#     print(f'{inp} -> {out} | {nn.binary(res)} | {to_string(res, 6)}')

# # -----------------not gate training -----------------
# for i in range(10_000):
#     j = nn.np.random.randint(0, len(not_gateI))
#     not_gate.train(not_gateI[j], not_gateO[j])
# not_gate.summary('NOT GATE')
# for inp, out in zip(not_gateI, not_gateO):
#     res = not_gate.think(inp)
#     print(f'{inp} -> {out} | {nn.binary(res)} | {to_string(res, 6)}')


def xor(x, y):
    yp = not_gate.think([y])
    xp = not_gate.think([x])

    xyp = and_gate.think([x, yp[0]])
    xpy = and_gate.think([xp[0], y])
    print()
    print(f'{x=}')
    print(f'{xp=}')
    print(f'{y=}')
    print(f'{yp=}')
    print(f'{xyp=}')
    print(f'{xpy=}')
    res = or_gate.think([xyp[0], xpy[0]])
    print(f'{res=}')

    return nn.binary(res)


for x, y in xorI:
    # xor(x, y)
    print(f'{x} {y} -> {xor(x, y)}')


print('------------')
for n in nn.np.linspace(0, 1, 10):
    print(f'0 {n} -> {and_gate.think([0, n])}')