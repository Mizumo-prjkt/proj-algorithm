import pygame, sys
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WIDTH, HEIGHT = 300, 350
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (21, 179, 158)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER_COLOR = (70, 70, 70)
BUTTON_TEXT_COLOR = (200, 200, 200)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Board setup
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# AI difficulty (global variable)
ai_difficulty = None

# Drawing functions
def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - 50), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - 50), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                  (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def draw_button():
    button_rect = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    font = pygame.font.Font(None, 36)
    text_surface = font.render('Retry', True, BUTTON_TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

def check_win(player):
    # Vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            print(f"{'Player' if player == 1 else 'AI'} wins with vertical line at column {col}")
            return True
    
    # Horizontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            print(f"{'Player' if player == 1 else 'AI'} wins with horizontal line at row {row}")
            return True
    
    # Ascending diagonal win check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        print(f"{'Player' if player == 1 else 'AI'} wins with ascending diagonal from (2, 0) to (0, 2)")
        return True
    
    # Descending diagonal win check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        print(f"{'Player' if player == 1 else 'AI'} wins with descending diagonal from (0, 0) to (2, 2)")
        return True

    return False

def ai_move():
    if ai_difficulty == 'hard':
        # Check if AI can win
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    board[row][col] = 2
                    if check_win(2):
                        print(f"AI wins by placing at ({row}, {col})")
                        return True
                    board[row][col] = 0
        
        # Check if AI needs to block player
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if available_square(row, col):
                    board[row][col] = 1
                    if check_win(1):
                        board[row][col] = 2
                        print(f"AI blocks player at ({row}, {col})")
                        return False # Block but don't declare win
                    board[row][col] = 0
        
    # Otherwise, make a random move (easy mode or fallback)
    empty_squares = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if available_square(row, col)]
    if empty_squares:
        row, col = random.choice(empty_squares)
        mark_square(row, col, 2)
        print(f"AI ({ai_difficulty}) places at ({row}, {col})")
        if check_win(2):
            print(f"AI wins with random move from ({row}, {col})")
            return True
    return False

def restart_game():
    global board, game_over, player, ai_difficulty
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    game_over = False
    player = 1
    ai_difficulty = random.choice(['easy', 'hard']) # Set AI difficulty on restart
    screen.fill(BG_COLOR)
    draw_lines()
    draw_button()
    print(f"Game restarted with AI difficulty: {ai_difficulty}")

# Game Loop
player = 1
game_over = False

# Set initial AI difficulty
ai_difficulty = random.choice(['easy', 'hard'])
print(f"Initial AI difficulty: {ai_difficulty}")

draw_lines()
draw_button()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            if mouseY < HEIGHT - 50:
                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if available_square(clicked_row, clicked_col) and not game_over and player == 1:
                    mark_square(clicked_row, clicked_col, player)
                    print(f"Player places at ({clicked_row}, {clicked_col})")
                    if check_win(player):
                        print(f"Player wins by connecting at ({clicked_row}, {clicked_col})")
                        game_over = True
                    elif is_board_full():
                        print("Game ended in a draw")
                        game_over = True
                    player = 2
                    draw_figures()

                if player == 2 and not game_over:
                    if ai_move():
                        game_over = True
                    elif is_board_full():
                        print("Game ended in a draw")
                        game_over = True
                    player = 1
                    draw_figures()
            else:
                restart_game()

    draw_button()
    pygame.display.update()
