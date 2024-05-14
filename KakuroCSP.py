import random
import math
import copy

class KakuroConfig:  
    """Utility class for the configuration of the Kakaro Board"""

    def get_indices(difficulty):
        """Returns the range of indices rows can span for different 
        difficulty levels of the Kakaro board"""
        if difficulty == "easy":
            return ((0, 1), (0, 2), (1, 3), (2, 3))
        elif difficulty == "intermediate":
            return ((1, 2), (0, 3), (0, 3), (1, 2))
        elif difficulty == "hard":
            return ((0, 2), (0, 2), (1, 3), (1, 3))
        elif difficulty == "expert":
            return ((1, 2), (0, 3), (0, 3), (1, 2))
        elif difficulty == "impossible":
            return ((1, 2), (0, 3), (0, 3), (1, 2))
        

    def get_constraints(difficulty):
        """ Returns column and row constraints of kakaro boards for differing difficulty levels.
        First row constraints, then column"""
        if difficulty == "easy":
            return ((3, 6, 8, 12), (4, 6, 6, 13))
        elif difficulty == "intermediate":
            return ((14, 14, 28, 16), (17, 18, 26, 11))
        elif difficulty == "hard":
            return ((14, 9, 20, 17), (4, 30, 22, 4))
        elif difficulty == "expert":
            return ((4, 19, 30, 8), (9, 19, 26, 7))
        elif difficulty == "impossible":
           return ((14, 14, 29, 16), (17, 18, 26, 11))

    def _initialize_board(indices, size): 
        """ Initializes board with empty cells (empty meaning values of None) """
        board = [[] for _ in range(size)] 
        for i in range(size):
                for j in range(indices[i][0], indices[i][1] + 1): 
                    board[i].append({'index': j, 'value': None, 'domain': list(range(1,10))})
        return board


class KakuroBoard:
    """ Creates a Kakuro Board, which is represented as a 2-D list. Each list element 
    has length 2. The first entry of the list element is the value, the second is the index
    (since indices can be blank and shapes of board are rarely consistent). Kakuro boards 
    have dimension, or size, difficulties and row and column constraints"""

    def __init__(self, difficulty = "intermediate"):
        self.__size = 4
        self.__difficulty = difficulty
        indices = KakuroConfig.get_indices(self.__difficulty)
        self.board = KakuroConfig._initialize_board(indices, self.__size)
        self.__row_constraints = KakuroConfig.get_constraints(self.__difficulty)[0]
        self.__col_constraints = KakuroConfig.get_constraints(self.__difficulty)[1]


    def set_board(self, new_board_state):
        """Set the board to a new state provided by the solver's timeline."""
        # Replace the entire board with the new state
        self.board = new_board_state

    def deep_copy(self):
        """Create a deep copy of the board."""
        return copy.deepcopy(self)

    def get_size(self):
        """ Get the size of the puzzle """
        return self.__size
    
    def get_difficulty(self):
        """ Get the difficulty of the puzzle """
        return self.__difficulty
    
    def get_board(self):
        """ Get the board containing rows and cells """
        return self.board
    
    def display_board(self):
        """ Print the board in a list format"""
        for row in self.board:
            print(row)

    def pretty_print(self):
        """ Print the board in a graphical format """
        # print column constraints
        row_constraints = self.get_row_constraints()
        col_constraints = self.get_col_constraints()
        print('    ', end = '')
        for elem in col_constraints:
            print(elem, end = '  ')
        print()

        for index, row in enumerate(self.board):
            # print row constraints
            if (len(str(row_constraints[index])) == 1):
                print(row_constraints[index], end = '  ')
            else:
                print(row_constraints[index], end = ' ')

            # print row
            i = 0
            for j in range(self.__size):
                if i < len(row) and row[i]['index'] == j:
                    print('[', end = '')
                    if row[i]['value'] is not None:
                        print(row[i]['value'], end = '')
                    else:
                        print(' ', end = '')
                    print(']', end = '')
                    i += 1
                else:
                    print('[X]', end = '')

            print()

    def pretty_print_domains(self):
        """ Print the cell domains in a graphical format"""
        # print column constraints
        row_constraints = self.get_row_constraints()
        col_constraints = self.get_col_constraints()
        print('    ', end = '')
        for elem in col_constraints:
            print(elem, end = '  ')
        print()

        for index, row in enumerate(self.board):
            # print row constraints
            if (len(str(row_constraints[index])) == 1):
                print(row_constraints[index], end = '  ')
            else:
                print(row_constraints[index], end = ' ')

            # print row
            i = 0
            for j in range(self.__size):
                if i < len(row) and row[i]['index'] == j:
                    print('[', end = '')

                    for value in row[i]['domain']:
                        print(value, end = '')

                    print(']', end = '')

                    i += 1
                else:
                    print('[X]', end = '')

            print()

    def get_row_constraints(self): 
        """ Get the row constraints of the board """
        return self.__row_constraints
    
    def get_col_constraints(self):
        """ Get the column constraints of the board """
        return self.__col_constraints
                
    def sum_rows(self):
        """ Returns the sum of the row values of the board """
        sum_row = [0] * self.__size
        i = 0
        for row in self.board: 
            sum_row[i] = sum([item['value'] for item in row if isinstance(item['value'], int)])
            i += 1
        return sum_row
    
    def sum_cols(self):
        """ Returns the sum of each column of the board """
        sum_col = [0] * self.__size
        i = 0
        for row in self.board:
            for elem in row:
                if isinstance(elem['value'], int):
                    sum_col[elem['index']] += elem['value']
        return sum_col
    
    def get_num_rem_rows(self): 
        """ Get the number of remaining cells in each row """
        num_rem_rows = [0] * 4
        for row in enumerate(self.board): 
            for cell in row[1]:
                if cell['value'] is None:
                    num_rem_rows[row[0]] += 1
        return num_rem_rows
    
    def get_num_rem_cols(self): 
        """ Get the number of remaining cells in each column """
        num_rem_cols = [0] * 4
        for row in enumerate(self.board): 
            for cell in row[1]:
                if cell['value'] is None:
                    num_rem_cols[cell['index']] += 1
        return num_rem_cols
     
    
    def is_valid_assignment(self, row, col, value):
        """ Determine if a value assignment is valid """
        # Check if value violates row sum constraint
        row_sum = sum(cell['value'] for cell in self.board[row] if isinstance(cell['value'], int)) + value
        if row_sum > self.get_row_constraints()[row]:
            return False

        # Check if value violates column sum constraint
        col_sum = 0
        for i in range(self.get_size()):
            cell = next((x for x in self.board[i] if x['index'] == col), None)
            if cell and isinstance(cell['value'], int):
                col_sum += cell['value']
        col_sum += value
        if col_sum > self.get_col_constraints()[col]:
            return False

        # Check if value violates all-different constraint in row and column
        for cell in self.board[row]:
            if cell['value'] == value:
                return False
        for i in range(self.get_size()):
            cell = next((x for x in self.board[i] if x['index'] == col), None)
            if cell and cell['value'] == value:
                return False

        return True
    
    def is_complete(self):
        """ Determine if the board is complete """
        for row in self.board:
            for cell in row:
                if cell['value'] is None:
                    return False  # Found an unassigned cell
        return self.meets_constraints()  # Check if the board meets all constraints
        
    def meets_constraints(self): 
        """ Checks if the current cell entries meets the board constraints"""
        return self.sum_rows() == list(self.__row_constraints) and self.sum_cols() == list(self.__col_constraints)
    
