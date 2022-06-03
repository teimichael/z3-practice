import numpy as np

f = open('cage_constraints', 'r')

counter = np.zeros((9, 9))

for line in f:
    e = line.split(' ')
    for i in range(1, len(e)):
        counter[int(e[i][0]) - 1][int(e[i][1]) - 1] += 1

print(counter)
f.close()
