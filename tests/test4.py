
from classes.Rocket import *
print('hi')
pop = []
# np.random.seed(1)
for i in range(5):
    d = Rocket(0)
    d.dna.random(11)
    pop.append(d)

for p in pop:
    print(p.dna.get())

print('-'*10)

children = reproduce(pop, 0, 25)

# for p in children:
#     print(p.dna.get())

