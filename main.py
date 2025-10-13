class board_maker():
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]


    def print_board(self, board):
        print("\n\n---------------------")
        for i in range(9):
            temp_str = ''
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    temp_str += '| '
                temp_str += str(board[i][j]) + ' '
            print(temp_str)
            if (i + 1) % 3 == 0:
                print("---------------------")


    def change_board(self, board):
        def check_errors(msg):
            while True:
                user_input = input(msg)
                if user_input in "123456789":
                    return int(user_input)
                print("\nInvalid input, please type a number from 1 to 9 (Inclusive).")
        
        while True:
            self.print_board(board)
            print()
            row = check_errors("Row to change (1 to 9): ")
            column = check_errors("Column to change (1 to 9): ")
            amount = check_errors("Change to amount (1 to 9): ")

            board[row-1][column-1] = amount
            print("\n" * 3)
            self.print_board(board)
            if input("Type 'q' to quit, or Enter/type anything else to change another cell: ").lower().startswith("q"):
                return board


class sudoko_solver():
    def __init__(self, board_to_solve):
        self.BoardTS = board_to_solve
    

    def print_board(self, board):
        temp = board_maker()
        temp.print_board(board)

    
    def solve(self, board):
        current = 0
        available_board_pos = [[i, j] for i in range(9) for j in range(9) if board[i][j] == 0]
        curr_sq_pos = available_board_pos[current]
        curr_value = 1
        iteration = 1
        
        while True:
            print("\n\nvvv Start vvv")
            print(f"Current: {current}, Curr_sq: {curr_sq_pos}, Curr_value: {curr_value}, Iteration: {iteration}.")
            self.print_board(board)
            
            flag = True #Checks the board is filled or not.
            for i in range(9):
                if 0 in board[i]:
                    flag = False
            if flag:
                break

            #board[curr_sq_pos[0]][curr_sq_pos[1]] is the value of the current square.
            if self.check_sq(board, curr_sq_pos, curr_value):
                board[curr_sq_pos[0]][curr_sq_pos[1]] = curr_value
                current += 1
                curr_value = 1
            else:
                curr_value += 1
                if curr_value > 9:
                    #Goes to the square before (and adds 1) and sets the current square to 0.
                    while True:
                        board[curr_sq_pos[0]][curr_sq_pos[1]] = 0
                
                        if current > 0:
                            current -= 1

                        curr_sq_pos = available_board_pos[current]
                
                        if board[curr_sq_pos[0]][curr_sq_pos[1]] >= 9:
                            board[curr_sq_pos[0]][curr_sq_pos[1]] = 0
                            continue
                
                        curr_value = board[curr_sq_pos[0]][curr_sq_pos[1]] + 1
                        break
            #Fixes current from going negetive and/or an IndexError occuring.
            try:
                curr_sq_pos = available_board_pos[current]
            except IndexError:
                current += 1
            iteration += 1
            
        print(f"\n\nDone! Iteration: {iteration}.")
        return board


    #Checks if the given square follows the rules of Sudoku. Returns either True or False.
    def check_sq(self, board, curr_sq, curr_value): #Order of type: list of lists, list with 2 int's, int.
        for cell in board: #Check the columns.
            if cell[curr_sq[1]] == curr_value:
                return False
           
        for row in board[curr_sq[0]]: #Check the rows.
            if row == curr_value:
                return False
        
        #Checks the 3x3 box that the square is in.
        box_columns = ((curr_sq[0] // 3) + 1) * 3
        box_rows = ((curr_sq[1] // 3) + 1) * 3
        
        for i in range(box_columns - 3, box_columns):
            for j in range(box_rows - 3, box_rows):
                if board[i][j] == curr_value:
                    return False
        return True


if __name__ == "__main__":
    b = board_maker()
    
    #You can replace this line with a 2D list instead.
    b.board = b.change_board(b.board)

    b.print_board(b.board)

    input("Press enter to start solving!")

    s = sudoko_solver(b.board)
    b.board = s.solve(s.BoardTS)

    b.print_board(b.board)