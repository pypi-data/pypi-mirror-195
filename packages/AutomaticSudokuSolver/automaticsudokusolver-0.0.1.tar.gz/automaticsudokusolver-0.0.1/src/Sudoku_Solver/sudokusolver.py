#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

class Solver():
    """
    The Solver class contains the basic solving code
    """
    def __init__(self):
        self.count = 0
    def find_next_empty(self, puzzle):
        """
        This function finds the next empty space on the board
        """
        for row in range(9):
            for column in range(9):
                if puzzle[row][column] == -1:
                    return row, column
        return None, None
    def find_next_full(self, puzzle):
        """
        This function finds the next space that is not empty
        """
        for row in range(9):
            for column in range(9):
                if puzzle[row][column] != -1:
                    return row, column
        return None, None

    def is_valid(self, puzzle, guess, row, col):
        """
        This function checks if a guess can go in the specified place
        """
        row_vals = puzzle[row]
        if guess in row_vals:
            return False
        col_vals = [puzzle[i][col] for i in range(9)]
        if guess in col_vals:
            return False
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if puzzle[r][c] == guess:
                    return False
        return True
        
    def solve(self, puzzle):
        """
        This function solves the sudoku
        """
        row, col = self.find_next_empty(puzzle)
        if row is None and col is None:
            return True
        for guess in range(1,10):
            self.count += 1
            if self.is_valid(puzzle, guess, row, col):
                puzzle[row][col] = guess
                
                if self.solve(puzzle):
                    return (True, puzzle, self.count)
            puzzle[row][col] = -1
        return False

class GUI():
    """
    The GUI class represents a GUI which solves sudokus
    """
    def __init__(self):
        """
        Build the window
        """
        self.solver = Solver()
        self.window = tk.Tk()
        self.title = tk.Label(text="WELCOME TO THE SUDOKU SOLVER")
        self.title.grid(row=1, column=1)
        self.board = [[],[],[],[],[],[],[],[],[]]
        for row in range(9):
            for item in range(9):
                myentry = tk.Entry(width=1)
                myentry.grid(row=row+3, column=item+3)
                self.board[row].append(myentry)
        self.pb = ttk.Progressbar(
            self.window,
            orient='horizontal',
            mode='determinate',
            length=280
        )
        self.pb.grid(row=5, column=1)
        self.progress = tk.Label(text="0.0%")
        self.progress.grid(row=6, column=1)
        self.solve_btn = tk.Button(text="Solve!")
        self.solve_btn.bind("<Button-1>", self.handle_solve_click)
        self.solve_btn.grid(row=13,column=2)
        self.clear_btn = tk.Button(text="Clear")
        self.clear_btn.bind("<Button-1>", self.handle_clear_click)
        self.clear_btn.grid(row=13, column=1)
    
    def handle_solve_click(self, event):
        """
        This function handles the press of the solve button
        """
        entryboard = [[],[],[],[],[],[],[],[],[]]
        for row in range(9):
            for item in range(9):
                if self.board[row][item].get() != "":
                    entryboard[row].append(int(self.board[row][item].get()))
                else:
                    entryboard[row].append(-1)
        
        row, col = self.solver.find_next_empty(entryboard)
        if row == None:
            showinfo(message="This sudoku is already solved.")
            return False
        row, col = self.solver.find_next_full(entryboard)
        print(type(row))
        while row != None:
            now = entryboard[row][col]
            entryboard[row][col] = -1
            if self.solver.is_valid(entryboard, now, row, col):
                pass
            else:
                showinfo(message="This is an impossible sudoku.")
                # row = None
                return False
            #window.after(100, lambda:entryboard[row][col] = now)
            previousrow, previouscol = row,col
            row, col = self.solver.find_next_full(entryboard)
            entryboard[previousrow][previouscol] = now
        solved, self.solution, count = self.solver.solve(entryboard)
        print(round(count/150))
        self.pb.start(round(count/150))
        print(self.solution)
        print(count/1.5)
        self.window.after(round(count/1.5), self.show_solution, entryboard)
        self.window.after(10, self.update_progress_bar)
    def show_solution(self, entryboard):
        """
        This function shows the solution
        """
        self.pb.stop()
        self.pb['value'] = 100
        count = 0
        for row in range(9):
            for item in range(9):
                self.board[row][item].delete(0, tk.END)
                self.board[row][item].insert(0, self.solution[row][item])
    def handle_clear_click(self, event):
        """
        This function handles when the clear button is pressed
        """
        for row in range(9):
            for item in range(9):
                self.board[row][item].delete(0, tk.END)
        self.pb['value'] = 0
        self.progress['text'] = "0.0%"
    def update_progress_bar(self):
        """
        This function updates the progress bar
        """
        if self.pb['value'] < 100:
            self.progress['text'] =  f"{self.pb['value']}%"
            self.window.after(10, self.update_progress_bar)
        else:
            self.pb['value'] = 100
            self.progress['text'] = "Complete"
    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    solver = Solver()
    print(solver.solve([[-1,7,2,-1,3,6,4,-1,-1],
              [-1,9,-1,7,-1,-1,-1,3,5],
              [-1,-1,-1,1,8,-1,-1,-1,2],
              [2,-1,6,-1,-1,-1,-1,9,-1],
              [3,-1,5,-1,9,-1,6,-1,8],
              [-1,4,-1,-1,-1,-1,5,-1,1],
              [7,-1,-1,-1,2,3,-1,-1,-1],
              [1,5,-1,-1,-1,4,-1,8,-1],
              [-1,-1,8,6,1,-1,9,7,-1]]))
    interface = GUI()
    interface.start()
    