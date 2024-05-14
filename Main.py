from KakuroCSP import KakuroBoard, KakuroConfig
from Backtracking import KakuroBoardSolver

# ---------------------- Testing ----------------------

board = KakuroBoard("expert")

print("\nEmpty board")
board.pretty_print()

print("\nDomains")
board.pretty_print_domains()


print("\nDomains after first iteration of AC3 pre-processing")
solver = KakuroBoardSolver()
solver.ac3(board)
board.pretty_print_domains()

print('\nBacktracking algo in process:')
solver.backtrack(board)


print('\nSolved! Board after backtracking algo executed:')
board.pretty_print()

print('T/F: The board meets constraints?', board.meets_constraints())



