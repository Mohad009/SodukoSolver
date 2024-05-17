import heapq #This is used to implement priority queue for A* algorithm
from copy import deepcopy #deepcopy function used to create deep copies of objects without modifying the original
import tkinter as tk # GUI library
from tkinter import messagebox #this is to show the message
class SudokuSolver:
    def __init__(self, board):
        self.board = board # Initializes the solver with the given Sudoku board

    # Checks if placing a number in a specific cell is valid according to Sudoku rules.
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
   
   # Finds the next empty cell in the Sudoku board
    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def heuristic(self, board): #Estimates the cost to reach the goal state by counting the number of empty cells.
        return sum(row.count(0) for row in board)

    #Solves the Sudoku puzzle using the A* algorithm.
    def a_star(self):
        start = deepcopy(self.board)
        pq = [(self.heuristic(start), start)]
        heapq.heapify(pq)
        steps = 0  # Initialize step counter
        
        while pq:
            _, current = heapq.heappop(pq)
            steps += 1  # Increment step counter for each state expansion
            empty = self.find_empty(current)
            if not empty:
                return current, steps  # Return both solution and step count
            row, col = empty
            
            for num in range(1, 10):
                if self.is_valid(current, row, col, num):
                    new_board = deepcopy(current)
                    new_board[row][col] = num
                    heapq.heappush(pq, (self.heuristic(new_board), new_board))
        return None, steps


class SudokuGUI: # A class to create a graphical user interface for solving Sudoku puzzles.
    def __init__(self, root, board): #Initializes the GUI with the given root window and Sudoku board.
        self.root = root
        self.board = board
        self.entries = []
        self.create_widgets()

    def create_widgets(self):
        #Creates the widgets for the GUI, including the grid of Entry widgets for the Sudoku cells and the Solve button.
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
        
        self.steps_label = tk.Label(self.root, text="")  # Label to display steps
        self.steps_label.grid(row=10, column=0, columnspan=9)

    def solve(self):
        """
        Solves the Sudoku puzzle and updates the GUI with the solution.
        If no solution exists, shows an error message.
        """
        board = self.get_board()
        solver = SudokuSolver(board)
        solution, steps = solver.a_star()
        if solution:
            self.display_solution(solution)
            self.steps_label.config(text=f"Cost (steps taken): {steps}")  # Update steps label
        else:
            messagebox.showerror("Error", "No solution exists")

    #Retrieves the current state of the board from the Entry widgets
    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.entries[i][j].get()
                row.append(int(value) if value else 0)
            board.append(row)
        return board

    #  Updates the Entry widgets with the solution values.
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
# Set up the Tkinter root window
root = tk.Tk()
root.title("Interactive Sudoku Solver") 
app = SudokuGUI(root, board) # Initialize the GUI application
root.mainloop() # Start the main event loop