import tkinter as tk
from tkinter import messagebox
import random

# Function to get maximum gold and path
def get_max_gold(gold):
    n = len(gold)
    m = len(gold[0])

    dp = [[0 for _ in range(m)] for _ in range(n)]
    path = [[[] for _ in range(m)] for _ in range(n)]

    for col in range(m-1, -1, -1):
        for row in range(n):
            if col == m - 1:
                dp[row][col] = gold[row][col]
                path[row][col] = [(row, col)]
            else:
                right = dp[row][col+1]
                right_up = dp[row-1][col+1] if row > 0 else 0
                right_down = dp[row+1][col+1] if row < n-1 else 0

                max_gold = max(right, right_up, right_down)

                if max_gold == right:
                    path[row][col] = [(row, col)] + path[row][col+1]
                elif max_gold == right_up:
                    path[row][col] = [(row, col)] + path[row-1][col+1]
                else:
                    path[row][col] = [(row, col)] + path[row+1][col+1]

                dp[row][col] = gold[row][col] + max_gold

    max_gold = 0
    best_path = []
    for i in range(n):
        if dp[i][0] > max_gold:
            max_gold = dp[i][0]
            best_path = path[i][0]

    return max_gold, best_path

# Class for the Gold Mine GUI
class GoldMineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gold Mine Game - AI Solver")

        # Container frame for the UI elements
        self.main_frame = tk.Frame(root, padx=10, pady=10)
        self.main_frame.pack(padx=20, pady=20)

        # Title label (smaller font)
        self.title_label = tk.Label(self.main_frame, text="Gold Mine Game", font=("Arial", 15, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=4, pady=5)

        # Grid dimension input section (manual entry)
        self.grid_frame = tk.Frame(self.main_frame)
        self.grid_frame.grid(row=1, column=0, columnspan=4, pady=10)

        self.grid_label = tk.Label(self.grid_frame, text="Enter Grid Dimensions (Rows x Columns)", font=("Arial", 12))
        self.grid_label.grid(row=0, column=0, columnspan=4, pady=5)

        self.row_label = tk.Label(self.grid_frame, text="Rows:", font=("Arial", 10))
        self.row_label.grid(row=1, column=0, padx=5, pady=5)
        self.row_entry = tk.Entry(self.grid_frame, width=5, font=("Arial", 10), justify="center")
        self.row_entry.grid(row=1, column=1, padx=5)
        self.row_entry.insert(0, "4")  # Default value

        self.col_label = tk.Label(self.grid_frame, text="Columns:", font=("Arial", 10))
        self.col_label.grid(row=1, column=2, padx=5, pady=5)
        self.col_entry = tk.Entry(self.grid_frame, width=5, font=("Arial", 10), justify="center")
        self.col_entry.grid(row=1, column=3, padx=5)
        self.col_entry.insert(0, "4")  # Default value

        # Buttons for solving and randomizing
        self.solve_button = tk.Button(self.main_frame, text="Solve", command=self.solve, bg="#4CAF50", fg="black", font=("Arial", 10), width=12)
        self.solve_button.grid(row=2, column=0, pady=5)

        self.randomize_button = tk.Button(self.main_frame, text="Randomize Grid", command=self.randomize_grid, bg="#FF9800", fg="black", font=("Arial", 10), width=12)
        self.randomize_button.grid(row=2, column=1, pady=5)

        # Label to display result
        self.result_label = tk.Label(self.main_frame, text="", font=("Arial", 10), justify=tk.LEFT)
        self.result_label.grid(row=3, column=0, columnspan=4, pady=5)

        # Frame to contain the canvas (animation panel)
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.grid(row=4, column=0, columnspan=4, pady=5)

        # Canvas for the animation (smaller size)
        self.canvas = tk.Canvas(self.canvas_frame, width=300, height=200, bg="white")
        self.canvas.pack()

        # Default grid setup
        self.rows = 4
        self.cols = 4
        self.grid_entries = []

    def create_grid(self):
        # Create the grid entries as Entry widgets
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.grid_entries = []

        for i in range(self.rows):
            row_entries = []
            for j in range(self.cols):
                e = tk.Entry(self.grid_frame, width=4, font=("Arial", 8), justify="center", bg="lightyellow", bd=2)
                e.grid(row=i+2, column=j, padx=3, pady=3)
                row_entries.append(e)
            self.grid_entries.append(row_entries)

    def randomize_grid(self):
        # Read the grid dimensions from the input fields
        try:
            self.rows = int(self.row_entry.get())
            self.cols = int(self.col_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for rows and columns.")
            return

        # Create new grid dynamically based on user-defined size
        self.create_grid()

        # Generate a random grid of values
        grid = [[random.randint(1, 10) for _ in range(self.cols)] for _ in range(self.rows)]

        # Update grid entries with random values
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid_entries[i][j].delete(0, tk.END)
                self.grid_entries[i][j].insert(0, str(grid[i][j]))

    def solve(self):
        # Read the grid values
        try:
            gold = [[int(self.grid_entries[i][j].get()) for j in range(self.cols)] for i in range(self.rows)]
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers in all cells.")
            return

        max_gold, path = get_max_gold(gold)

        self.result_label.config(text=f"Maximum Gold: {max_gold}\nPath: {path}")
        self.animate_grid(gold, path)

    def animate_grid(self, gold, path):
        self.canvas.delete("all")
        rows, cols = len(gold), len(gold[0])
        cell_width = 50
        cell_height = 40
        path_index = 0

        # Draw the initial grid with numbers
        for i in range(rows):
            for j in range(cols):
                x1 = j * cell_width
                y1 = i * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(gold[i][j]))

        # Animate the path
        def step():
            nonlocal path_index
            if path_index < len(path):
                row, col = path[path_index]
                x1 = col * cell_width
                y1 = row * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height

                # Create a yellow rectangle and display the number in yellow
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="pink", outline="black")
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(gold[row][col]), fill="black")

                path_index += 1
                self.root.after(500, step)  # 500ms delay between each step

        step()  # Start the animation

if __name__ == "__main__":
    root = tk.Tk()
    app = GoldMineGUI(root)
    root.mainloop()
