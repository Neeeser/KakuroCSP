from KakuroCSP import KakuroConfig, KakuroBoard
class KakuroBoardSolver:
    """ Class to solve Kakuro puzzles using AC-3 and backtracking algorithms """
    def __init__(self):
        self.timeline = []
        pass


    def ac3(self, kakuro_board):
        """ AC-3 algorithm to reduce domains of neighboring cells """
        for row in enumerate(kakuro_board.board):
            for elem in enumerate(row[1]):
                # AllDiff requirements
                ## Integer values present in element row
                row_vals = [cell['value'] for cell in row[1] if isinstance(cell['value'], int)]
                
                ## Integer values present in element column
                col_val = elem[1]['index']
                col_vals = \
                    [element['value'] for sublist in kakuro_board.board \
                     for element in sublist if element['index'] == col_val and isinstance(element['value'], int)]
                
                ## Invalid alldif values are combination of row and column values
                invalid_vals_alldif = list(set(row_vals + col_vals))
                
                # Update domain for valid values
                ## If the cell is blank:
                if (isinstance(elem[1]['value'], int) is False):

                    ## 1. If there is only one remaining cell in row
                    ## Ensure that cell value sums to row constraint 
                    if kakuro_board.get_num_rem_rows()[row[0]] == 1: 
                        solution = kakuro_board.get_row_constraints()[row[0]]\
                                        - kakuro_board.sum_rows()[row[0]]
                        if solution < 10:
                            elem[1]['domain'] = [solution]
                        else:
                            elem[1]['domain'] = []
                    
                    ## 2. Else if there is only one remaining cell in col
                    ## Ensure that cell value sums to col constraint
                    elif kakuro_board.get_num_rem_cols()[elem[1]['index']] == 1: 
                        solution = kakuro_board.get_col_constraints()[col_val]\
                                        -  kakuro_board.sum_cols()[col_val]
                        if solution < 10:
                            elem[1]['domain'] = [solution]
                        else:
                            elem[1]['domain'] = []
                        
                    ## 3. Otherwise limit domain to numbers that satisfy alldiff 
                    ## and are less than the row/col constraint - current sum row/col
                    else:    
                        elem[1]['domain'] = [integer for integer in list(range(1, 10)) \
                                    if integer not in invalid_vals_alldif \
                                    and integer < kakuro_board.get_row_constraints()[row[0]]\
                                            - kakuro_board.sum_rows()[row[0]]  \
                                    and integer < kakuro_board.get_col_constraints()[col_val]\
                                            -  kakuro_board.sum_cols()[col_val]]
                # 4. If the cell has already been filled in
                else: 
                    ## Limit domain to what it was previously
                    ## but with the selected integer removed
                    domain = elem[1]['domain']
                    domain = [integer for integer in domain if integer != elem[1]['value']]
                    elem[1]['domain'] = domain
                    

    def backtrack(self, kakuro_board):
        """ Backtracking algorithm to solve a Kakuro puzzle: returns timeline of all board states leading to solution """
        self.timeline.append(kakuro_board.deep_copy())
        # Apply AC-3 to reduce domains before starting
        self.ac3(kakuro_board)
        self.timeline.append(kakuro_board.deep_copy())

        # Check if the board is complete
        if kakuro_board.is_complete():
            return True

        # Find the next cell to assign a value
        row, col, cell = self.find_unassigned_cell(kakuro_board)
        if cell is None:
            return False  # No unassigned cell found, backtrack

        # Try each value in the domain of the cell
        for value in cell['domain']: # loop through domain in forward order
        # for value in reversed(cell['domain']): # loop through domain in reverse order
            if kakuro_board.is_valid_assignment(row, col, value):
                cell['value'] = value

                print("\nCurrent Board State:")
                kakuro_board.pretty_print()

                print("\nCurrent Domains:")
                kakuro_board.pretty_print_domains()

                print('\nValue of', value, 'selected for cell at row', row, 'and column', col)
                print('\nBoard state after selection:')
                kakuro_board.pretty_print()

                if self.backtrack(kakuro_board):
                    return True

                # Backtrack: undo the assignment and try the next value
                print('\nBacktracking from value', value, 'at row', row, 'and column', col)
                cell['value'] = None

        # No valid assignment found, need to backtrack
        return False

    def find_unassigned_cell(self, kakuro_board):
        """ Find the next unassigned cell using minimum remaining values heuristic """
        min_domain_size = float('inf')
        selected_cell = None
        selected_row = selected_col = -1

        for row_index, row in enumerate(kakuro_board.board):
            for cell in row:
                if cell['value'] is None and len(cell['domain']) < min_domain_size:
                    min_domain_size = len(cell['domain'])
                    selected_cell = cell
                    selected_row = row_index
                    selected_col = cell['index']

        return selected_row, selected_col, selected_cell
