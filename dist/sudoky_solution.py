import copy

class SudokuSolver:
    def solve(puzzle):
        solution = copy.deepcopy(puzzle)
        if SudokuSolver.solveHelper(solution):
            return solution
        return None

    def solveHelper(solution):
        min_count = None
        while True:
            min_count = None
            for i in range(9):
                for j in range(9):
                    if solution[i][j] != '.':
                        continue
                    values = SudokuSolver.find_possible_values(i, j, solution)
                    n = len(values)
                    if n == 0:
                        return False
                    if n == 1:
                        solution[i][j] = values.pop()
                    if not min_count or \
                            n < len(min_count[1]):
                        min_count = ((i, j), values)
            if not min_count:
                return True
            elif 1 < len(min_count[1]):
                break
        q1, q2 = min_count[0]
        for v in min_count[1]:
            board_2 = copy.deepcopy(solution)
            board_2[q1][q2] = v
            if SudokuSolver.solveHelper(board_2):
                for q1 in range(9):
                    for q2 in range(9):
                        solution[q1][q2] = board_2[q1][q2]
                return True
        return False

    def find_possible_values(row, columns, puzzle):
        values = {v for v in range(1, 10)}
        values -= SudokuSolver.get_row(row, puzzle)
        values -= SudokuSolver.get_column(columns, puzzle)
        values -= SudokuSolver.get_values(row, columns, puzzle)
        return values

    def get_row(row, puzzle):
        return set(puzzle[row][:])

    def get_column(columnIndex, puzzle):
        return {puzzle[r][columnIndex] for r in range(9)}

    def get_values(row, columns, puzzle):
        a = 3 * (row // 3)
        b = 3 * (columns // 3)
        return {puzzle[a + r][b + c] for r in range(3) for c in range(3)}


def read_sudoku(filename):
    matrix = []
    s = []
    with open(f"sudoku_options/{filename}") as f:
        for line in f:
            for item in line:
                if len(s) == 9:
                    matrix.extend([s])
                    s = []

                if item == '.':
                    s.append('.')
                if item.isdigit():
                    s.append(int(item))

        if len(s) == 9:
            matrix.extend([s])

    return matrix
