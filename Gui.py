import pygame
import sys

from Backtracking import KakuroBoardSolver
from KakuroCSP import KakuroBoard  # Make sure to import your KakuroBoard class

# Initialize Pygame
pygame.init()

# Constants for the grid size
BOARD_SIZE = 4  # Assuming the board is 4x4
GRID_SIZE = BOARD_SIZE + 1  # Add one for the constraints
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
FONT_SIZE = 36

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
PURPLE = (150, 0, 150)
LIGHT_GRAY = (220, 220, 220)


# Colors for domain values
DOMAIN_SOLVED = (0, 255, 0)  # Green for solved value
DOMAIN_POSSIBLE = (0, 0, 255)  # Blue for possible values
DOMAIN_IMPOSSIBLE = (255, 0, 0)  # Red for values not in the domain


# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kakuro Game")

# Load font
font = pygame.font.SysFont(None, FONT_SIZE)

# Initialize Kakuro board
kakuro = KakuroBoard()
kakuro.pretty_print()

solver = KakuroBoardSolver()
# solver.ac3(kakuro)
# solver.backtrack(kakuro)
print(solver.timeline)
# Helper function definitions
def draw_blocked_cell(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))

def draw_input_cell(x, y):
    pygame.draw.rect(screen, PURPLE, (x, y, CELL_SIZE, CELL_SIZE))

def draw_constraint_cell(x, y, constraint):
    pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
    if constraint:  # Only draw constraint if it's not None
        text_surface = font.render(str(constraint), True, BLACK)
        screen.blit(text_surface, (x + (CELL_SIZE - text_surface.get_width()) // 2,
                                   y + (CELL_SIZE - text_surface.get_height()) // 2))

def draw_grid_lines():
    # Draw vertical lines
    for i in range(GRID_SIZE + 1):  # +1 for the edge line
        pygame.draw.line(screen, LIGHT_GRAY, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT))
    # Draw horizontal lines
    for i in range(GRID_SIZE + 1):  # +1 for the edge line
        pygame.draw.line(screen, LIGHT_GRAY, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE))

# Main function to draw the grid
# Helper function to draw cell values
def draw_cell_value(x, y, value):
    text_surface = font.render(str(value), True, BLACK)
    screen.blit(text_surface, (x + (CELL_SIZE - text_surface.get_width()) // 2,
                               y + (CELL_SIZE - text_surface.get_height()) // 2))

# Helper function to draw domain values with colors
# Helper function to draw domain values with colors and larger solved number
def draw_domain_values(x, y, domain, solved_value=None):
    domain_font_size = CELL_SIZE // 4  # Font size for domain values
    solved_font_size = CELL_SIZE // 3  # Slightly larger font size for the solved value
    domain_font = pygame.font.SysFont(None, domain_font_size)
    solved_font = pygame.font.SysFont(None, solved_font_size)
    padding = CELL_SIZE // 9  # Padding around numbers

    for number in range(1, 10):
        position = ((number - 1) % 3, (number - 1) // 3)  # Grid position
        domain_x = x + position[0] * (CELL_SIZE // 3) + padding
        domain_y = y + position[1] * (CELL_SIZE // 3) + padding

        color = DOMAIN_POSSIBLE if number in domain else DOMAIN_IMPOSSIBLE
        if solved_value and number == solved_value:
            color = DOMAIN_SOLVED
            font = solved_font
        else:
            font = domain_font

        text_surface = font.render(str(number), True, color)
        screen.blit(text_surface, (domain_x, domain_y))


# Main function to draw the grid
def draw_grid():
    # Draw constraints
    for i, constraint in enumerate(kakuro.get_col_constraints()):
        draw_constraint_cell((i+1) * CELL_SIZE, 0, constraint)
    for i, constraint in enumerate(kakuro.get_row_constraints()):
        draw_constraint_cell(0, (i+1) * CELL_SIZE, constraint)

    for row_index, row in enumerate(kakuro.get_board(), 1):  # Start at 1 to offset for constraints
        for col_index in range(1, GRID_SIZE):  # Start at 1 to offset for constraints
            x, y = col_index * CELL_SIZE, row_index * CELL_SIZE
            cell = next((c for c in row if c['index'] == col_index - 1), None)
            if cell is not None:
                draw_input_cell(x, y)
                if cell['value'] is not None:
                    # Pass the solved value to draw_domain_values
                    draw_domain_values(x, y, range(1, 10), solved_value=cell['value'])
                    #draw_cell_value(x, y, cell['value'])
                else:
                    # Pass the cell's domain to draw_domain_values
                    draw_domain_values(x, y, cell['domain'])
            else:
                draw_blocked_cell(x, y)

    # Draw grid lines on top of everything else
    draw_grid_lines()

def handle_mouse_click(pos):
    # Add logic to handle mouse click events
    pass


class Button:
    def __init__(self, x, y, width, height, text=''):
        self.color = (75, 75, 75)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen):
        # Call this method to draw the button on the screen
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(None, 40)
            text = font.render(self.text, True, WHITE)
            screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        else:
            return False

    def change_text(self, new_text):
        """Change the text displayed on the button."""
        self.text = new_text

# Initialize buttons
solve_button = Button(SCREEN_WIDTH - 150, 20, 120, 40, 'Solve')
play_pause_button = Button(SCREEN_WIDTH - 300, 20, 120, 40, 'Play')
speed_up_button = Button(SCREEN_WIDTH - 450, 20, 120, 40, 'Up')
slow_down_button = Button(SCREEN_WIDTH - 600, 20, 120, 40, 'Down')

# Global variables for playback control
is_playing = False
playback_speed = 100  # Milliseconds between steps
last_playback_time = 0

def draw_move_counter(screen, move_number, total_moves):
    font = pygame.font.SysFont(None, FONT_SIZE)
    text = f'Move: {move_number}/{total_moves}'
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (10, 10))  # 10 pixels from the top and left edges


def redraw_game_window(solution_step):
    screen.fill(BLACK)  # Fill the background with black
    draw_grid()
    solve_button.draw(screen)
    play_pause_button.draw(screen)
    speed_up_button.draw(screen)
    slow_down_button.draw(screen)
    if Solved:  # Only draw the counter if the game has started solving
        draw_move_counter(screen, solution_step, len(solver.timeline))
    pygame.display.update()

def main():
    global is_playing, last_playback_time, solution_step, playback_speed, Solved
    running = True
    solution_step = 0
    Solved = False

    while running:
        pos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if solve_button.is_over(pos):
                    if not Solved:
                        solver.ac3(kakuro)
                        solver.backtrack(kakuro)
                        Solved = True
                    # Manually step through the solution
                    if solution_step < len(solver.timeline):
                        kakuro.set_board(solver.timeline[solution_step].board)
                        solution_step += 1
                        redraw_game_window(solution_step)
                elif play_pause_button.is_over(pos):
                    if not Solved:
                        solver.ac3(kakuro)
                        solver.backtrack(kakuro)
                        Solved = True
                    # Toggle automatic playback
                    is_playing = not is_playing
                elif speed_up_button.is_over(pos):
                    # Speed up playback
                    playback_speed = max(10, playback_speed - 10)
                    print(playback_speed)
                elif slow_down_button.is_over(pos):
                    # Slow down playback
                    playback_speed += 10
                    print(playback_speed)

        # Automatic playback logic
        if is_playing and current_time - last_playback_time > playback_speed:
            if solution_step < len(solver.timeline):
                kakuro.set_board(solver.timeline[solution_step].board)
                solution_step += 1
                redraw_game_window(solution_step)
                last_playback_time = current_time

        # Update play/pause button text based on playback state
        if is_playing:
            play_pause_button.change_text('Pause')
        else:
            play_pause_button.change_text('Play')

        redraw_game_window(solution_step)

    pygame.quit()
    sys.exit()



def main_menu():
    # Load the background image
    background_image = pygame.image.load('background.png')
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale it to fit the screen size

    # Button properties
    button_width = 200
    button_height = 50
    button_spacing = 20  # Space between buttons
    total_button_area = (button_height + button_spacing) * 5 - button_spacing  # Adjust based on number of buttons

    # Calculate the starting y position to center the buttons
    start_y = (SCREEN_HEIGHT - total_button_area) // 2

    # Define buttons for each difficulty
    easy_button = Button(SCREEN_WIDTH // 2 - button_width // 2, start_y, button_width, button_height, 'Easy')
    intermediate_button = Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + (button_height + button_spacing), button_width, button_height, 'Intermediate')
    hard_button = Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height, 'Hard')
    expert_button = Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + 3 * (button_height + button_spacing), button_width, button_height, 'Expert')
    impossible_button = Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + 4 * (button_height + button_spacing), button_width, button_height, 'Impossible')

    buttons = [easy_button, intermediate_button, hard_button, expert_button, impossible_button]

    running = True
    while running:
        # Blit the background image onto the screen
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_over(pos):
                        return button.text  # Return the selected difficulty

        # Draw the buttons
        for button in buttons:
            button.draw(screen)

        pygame.display.update()


if __name__ == "__main__":

    diff = main_menu().lower()

    kakuro = KakuroBoard(diff)
    main()