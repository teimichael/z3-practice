from z3 import *


def build_solver(matrix):
    """Build solver with generated constraints from the given matrix"""
    row_len = len(matrix)
    col_len = len(matrix[0])

    solver = Optimize()
    choice = [Int('choice_%d' % i) for i in range(col_len)]
    col_value = [Real('col_value_%d' % i) for i in range(col_len)]

    for i in range(col_len):
        solver.add(And(choice[i] >= 0, choice[i] <= row_len - 1))

    solver.add(Distinct(choice))

    def else_choice(col, row):
        if row == row_len:
            return -1
        else:
            return If(choice[col] == row, matrix[row][col], else_choice(col, row + 1))

    for c in range(col_len):
        for r in range(row_len):
            solver.add(col_value[c] == else_choice(c, 0))

    col_sum = Real('col_sum')
    solver.add(col_sum == Sum(*col_value))
    solver.minimize(col_sum)
    return solver


def main():
    matrix = [[9, 8, 7.5, 7],
              [4.5, 8.5, 5.5, 6.5],
              [11.5, 9.5, 9, 9.5],
              [5, 10, 3.5, 10],
              [4.5, 12.5, 9.5, 11]]

    solver = build_solver(matrix)
    print(solver.check())
    print(solver.model())


if __name__ == "__main__":
    main()
