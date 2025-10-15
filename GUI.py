import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from main import sudoko_solver


class SudokuGUI():
    def __init__(self, root):
         self.selected_num = 0
         self.grid_items = [[0 for j in range(9)] for i in range(9)]
         
         self.root = root
         root.title("Sudoku Solver (With GUI!)")
         root.geometry("1500x1000")

         self.create_widgets()
    

    def set_button(self, num):
        self.f1_buttons[num].config(text=self.selected_num, style="Font.TButton")
        self.grid_items[num // 9][num % 9] = self.selected_num

    
    def set_num(self, var):
        self.selected_num = var
    
    
    def reset_board(self):
        self.grid_items = [[0 for j in range(9)] for i in range(9)]
        
        for num in self.f1_buttons:
            num.config(text=0, style="Font.TButton")
    

    def test_name(self):
        for num in range(81):
            self.f1_buttons[num].config(text=self.grid_items[num // 9][num % 9], style="Font.TButton")
    

    def stop_solve(self):
        self.stop = 1


    def create_widgets(self):
        self.root.grid_rowconfigure(1, weight=10)
        self.root.grid_rowconfigure((0, 2, 3), weight=0)

        self.root.grid_columnconfigure(0, weight=1)

        
        label1 = ttk.Label(self.root, text="Sudoku board", font="Calibri 24 bold")
        label1.grid(row=0, column=0)

        
        #Font for buttons.
        self.btn_font = tkfont.Font(family="Google Sans", size=24, weight="bold")
        style = ttk.Style(self.root)
        style.configure('Normal.TButton', font=self.btn_font)

        blue_style = ttk.Style(self.root)
        blue_style.configure("Blue.TButton", font=self.btn_font, background="#87CEEB", foreground="Black")

        red_style = ttk.Style(self.root)
        red_style.configure("Red.TButton", font=self.btn_font, background="#EB8787", foreground="Black")

        
        #9x9 Grid.
        frame1 = ttk.Frame(self.root)
        frame1.grid(row=1, column=0, sticky="nesw", padx=10, pady=10)
        
        for i in range(9):
            frame1.rowconfigure(i, weight=1)
        for j in range(9):
            frame1.columnconfigure(j, weight=1)
        
        
        #Add buttons to the 9x9 grid.
        self.f1_buttons = []
        for i in range(81):
            sq_button = ttk.Button(frame1, text=' ', style="Normal.TButton", command=lambda var=i: self.set_button(var))
            self.f1_buttons.append(sq_button)

            row_num = i // 9
            column_num = i % 9

            sq_button.grid(row=row_num, column=column_num, sticky="nesw")
    

       
        #Select number to change
        button_frame = ttk.Frame(self.root)
        num_buttons = []
        for i in range(10):
            button = ttk.Button(button_frame, text=(i), command=lambda var=i: self.set_num(var))
            num_buttons.append(button)     
        
        #Solve, reset, stop frame.
        self.srs_frame = ttk.Frame(self.root)

        #Solve, reset and stop buttons.
        self.solve_b = ttk.Button(self.srs_frame, text="Solve", command=self.solve_sudoku)
        self.stop_b = ttk.Button(self.srs_frame, text="Stop", command=self.stop_solve)
        self.reset_b = ttk.Button(self.srs_frame, text="Reset", command=self.reset_board)
        
        self.stop = 0
    
        
        for i in num_buttons:
             i.pack(side="left")
        button_frame.grid(row=2, column=0, pady=60)

        self.solve_b.pack(side="left", padx=50)
        self.stop_b.pack(side="left")
        self.reset_b.pack(side="left", padx=50)
        self.srs_frame.grid(row=3, column=0)

        self.solve_b.state(["!disabled"])
        self.reset_b.state(["!disabled"])
        self.stop_b.state(["disabled"])

        self.reset_board()
    
    
    def solve_sudoku(self):
        self.old_grid = [j for i in self.grid_items for j in i]
        self.grid_2 = tuple(self.grid_items)

        s = sudoko_solver(self.grid_items)

        self.solve_b.state(["disabled"])
        self.reset_b.state(["disabled"])
        self.stop_b.state(["!disabled"])

        self.my_solve = s.solve(self.grid_items)

        self.animate_solve()
                


    def animate_solve(self):
        def stop_animation():
            self.solve_b.state(["!disabled"])
            self.reset_b.state(["!disabled"])
            self.stop_b.state(["disabled"])
            self.stop = 0
        
        
        if self.stop == 1:
            stop_animation()
            self.reset_board()
            for i in range(81):
                self.grid_items[i // 9][i % 9] = self.old_grid[i]
                self.f1_buttons[i].config(text=self.old_grid[i])
            return
        
        try:
            #Checks all the nums to see if it should be blue
            for i in range(81):
                temp_var = self.old_grid[i]
                
                if temp_var != self.grid_items[i // 9][i % 9] and temp_var == 0:
                    self.f1_buttons[i].config(style="Blue.TButton")
                else:
                    self.f1_buttons[i].config(style="Normal.TButton")
            
            next_items, temp = next(self.my_solve)
            
            if temp != None:
                self.f1_buttons[(9 * temp[0]) + temp[1]].config(style="Red.TButton")
                stop_animation()
                return
            
            self.grid_items = next_items

            #Show the actual board
            for i in range(81):
                self.f1_buttons[i].config(text=self.grid_items[i // 9][i % 9])

            self.root.after(1, self.animate_solve)
        except StopIteration:
            stop_animation()
            return


def main():
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()