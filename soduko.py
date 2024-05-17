import heapq #
from copy import deepcopy

class SudokuSolver:
    def __init__(self, board):
        self.board = board

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def heuristic(self, board):
        return sum(row.count(0) for row in board)

    def a_star(self):
        start = deepcopy(self.board)
        pq = [(self.heuristic(start), start)]
        heapq.heapify(pq)
        
        while pq:
            _, current = heapq.heappop(pq)
            empty = self.find_empty(current)
            if not empty:
                return current
            row, col = empty
            
            for num in range(1, 10):
                if self.is_valid(current, row, col, num):
                    new_board = deepcopy(current)
                    new_board[row][col] = num
                    heapq.heappush(pq, (self.heuristic(new_board), new_board))
        return None

# Example Sudoku board (0 represents empty cells)
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solver = SudokuSolver(board)
solution = solver.a_star()

if solution:
    for row in solution:
        print(row)
else:
    print("No solution exists")
