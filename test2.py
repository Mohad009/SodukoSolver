import heapq #This is used to implement priority queue for A* algorithm
from copy import deepcopy #deepcopy function used to create deep copies of objects without modifying the original
import tkinter as tk # GUI library
from tkinter import messagebox #this is to show the message

#This class implement the A* algorithm
class SudokuSolver:
    def __init__(self, board): # the constructor will initializes the board
        self.board = board

    #This method will checks the validity of the sudoku according to sudoku rules
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
    #This method finds the next emtpy cell in the board
    #it return the location of the empty cell
    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None
    #this method estimates the cost to reach the goal state
    def heuristic(self, board):
        return sum(row.count(0) for row in board)
    
    #implementatoin of A* algorithm
    def a_star(self):
        start = deepcopy(self.board)
        pq = [(self.heuristic(start), start)]
        heapq.heapify(pq)
        steps=0
        
        while pq:
            _, current = heapq.heappop(pq)
            steps+=1
            empty = self.find_empty(current)
            if not empty:
                return current
            row, col = empty
            
            for num in range(1, 10):
                if self.is_valid(current, row, col, num):
                    new_board = deepcopy(current)
                    new_board[row][col] = num
                    heapq.heappush(pq, (self.heuristic(new_board), new_board))
        return None,steps

class SudokuGUI:
    def __init__(self, root, board):
        self.root = root
        self.board = board
        self.entries = []
        self.create_widgets()

    def create_widgets(self):
        for i in range(9):
            row_entries = []
            for j in range(9):
                entry = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)
                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                row_entries.append(entry)
            self.entries.append(row_entries)
        
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=9, column=4, pady=10)

    def solve(self):
        board = self.get_board()
        solver = SudokuSolver(board)
        solution = solver.a_star()
        if solution:
            self.display_solution(solution)
            self.steps_label.config(text=f"Cost (steps taken): {steps}")
        else:
            messagebox.showerror("Error", "No solution exists")

    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.entries[i][j].get()
                row.append(int(value) if value else 0)
            board.append(row)
        return board

    def display_solution(self, solution):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, str(solution[i][j]))

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

root = tk.Tk()
root.title("Interactive Sudoku Solver")
app = SudokuGUI(root, board)
root.mainloop()
