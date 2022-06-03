from z3 import *

# Define global parameters
column_size = 9
row_size = 9

# Create Z3 Solver
s = Solver()

cells = [[Int('cell%d%d' % (r, c)) for c in range(column_size)] for r in range(row_size)]

# Add digit constraints: dom(val(cell in cells)) = [1, 9]
for r in range(row_size):
    for c in range(column_size):
        s.add(cells[r][c] >= 1)
        s.add(cells[r][c] <= 9)

# Add row constraints
for r in range(row_size):
    s.add(Distinct(cells[r][0],
                   cells[r][1],
                   cells[r][2],
                   cells[r][3],
                   cells[r][4],
                   cells[r][5],
                   cells[r][6],
                   cells[r][7],
                   cells[r][8]))

# Add column constraints
for c in range(row_size):
    s.add(Distinct(cells[0][c],
                   cells[1][c],
                   cells[2][c],
                   cells[3][c],
                   cells[4][c],
                   cells[5][c],
                   cells[6][c],
                   cells[7][c],
                   cells[8][c]))

# Add 3*3 grid constrains
for r in range(0, row_size, 3):
    for c in range(0, column_size, 3):
        s.add(Distinct(cells[r + 0][c + 0],
                       cells[r + 0][c + 1],
                       cells[r + 0][c + 2],
                       cells[r + 1][c + 0],
                       cells[r + 1][c + 1],
                       cells[r + 1][c + 2],
                       cells[r + 2][c + 0],
                       cells[r + 2][c + 1],
                       cells[r + 2][c + 2]))

# Add cage constrains from the file
f = open('cage_constraints', 'r')

for line in f:
    cage = []
    e = line.split(' ')
    for i in range(1, len(e)):
        cage.append(cells[int(e[i][0]) - 1][int(e[i][1]) - 1])
    s.add(Distinct(*cage))
    s.add(Sum(*cage) == e[0])

f.close()

# Start solving
s.check()
m = s.model()

# Output result matrix
for r in range(row_size):
    for c in range(column_size):
        print(str(m[cells[r][c]]) + ' ', end='')
    print()
