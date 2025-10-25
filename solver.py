class sudoko_solver():
    def __init__(self, board_to_solve):
        self.BoardTS = board_to_solve

    
    def solve(self, board):
        current = 0
        available_board_pos = [[i, j] for i in range(9) for j in range(9) if board[i][j] == 0]
        
        #Checks if board given is already completed
        flag = True
        for i in range(9):
            if 0 in board[i]:
                flag = False
        if flag:
            yield board, None
            return
        

        for row in range(9):
            for col in range(9):
                value = board[row][col]
                if value != 0:
                    board[row][col] = 0
                    if not self.check_sq(board, [row, col], value):
                        board[row][col] = value
                        yield board, [row, col]
                        return
                    board[row][col] = value


        curr_sq_pos = available_board_pos[current]
        curr_value = 1
        iteration = 1
        
        while True:
            flag = True #Checks if board is filled or not.
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
                yield board, None

                if current >= len(available_board_pos):
                    break
            else:
                curr_value += 1
                if curr_value > 9:
                    #Goes to the square before (and adds 1) and sets the current square to 0.
                    while True:
                        if current <= 0 and board[curr_sq_pos[0]][curr_sq_pos[1]] >= 9:
                            yield board
                            return
                        
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
    def check_sq(self, brd, curr_sq, curr_value): #Order of type: list of lists, list with 2 int's, int.
        for cell in brd: #Check the columns.
            if cell[curr_sq[1]] == curr_value:
                return False
           
        for row in brd[curr_sq[0]]: #Check the rows.
            if row == curr_value:
                return False
        
        #Checks the 3x3 box that the square is in.
        box_columns = ((curr_sq[0] // 3) + 1) * 3
        box_rows = ((curr_sq[1] // 3) + 1) * 3
        
        for i in range(box_columns - 3, box_columns):
            for j in range(box_rows - 3, box_rows):
                if brd[i][j] == curr_value:
                    return False
        return True
