import pygame
#                                           constants

WIDTH, HEIGHT = 600, 600  #dimensions of the window
ROWS, COLUMNS = 8, 8    #number of squares in each row and column
SQUARE_SIZE = WIDTH//COLUMNS  #size of each square

# colors in RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('CROWN.png'), (44, 25))
###########################################################################################################
#                                              piece
# creating the actual pieces
class Piece:
    pad = 15 
    outline = 2

    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self): # calculating the middle of the square for placing the piece
        self.x = SQUARE_SIZE * self.column + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):  # change king variable if the piece becomes a king
        self.king = True

    def draw(self, win):
        # drawing the piece
        radius = SQUARE_SIZE // 2 - self.pad  # calculating radius
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.outline)  # drawing outer piece
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)  # drawing inner piece
        if self.king: #drawing the crown
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, column):
        self.row = row
        self.column = column
        self.calculate_position()


########################################################################################################################
#                                              board
class Board:
    def __init__(self):
        self.board = []  #creating empty list
        self.red_left = self.white_left = 12  #number of pieces for each player
        self.red_kings = self.white_kings = 0 #number of kings for each player
        self.create_board()
    
    def create_board(self): # creates the board
        for row in range(ROWS):
            self.board.append([]) # creating empty list for each row
            for column in range(COLUMNS):
                if column % 2 == ((row + 1) % 2): #if true then the square will contain a piece initially
                    if row < 3:
                        self.board[row].append(Piece(row, column, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, column, RED))
                    else:
                        self.board[row].append(0)
                else:  #the square will initially be without any piece
                    self.board[row].append(0)
                    
    def get_piece(self, row, column): #returns the piece in the given row and column
        return self.board[row][column]
    
    def draw_squares(self, win): #to draw the squares of the board
        #fill the window with black color
        win.fill(BLACK)
        for row in range(ROWS):
            for column in range(row % 2, COLUMNS, 2): #to draw the red squares
                pygame.draw.rect(win, GREY, (row * SQUARE_SIZE, column * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
    def draw(self, win):
        # drawing board and pieces
        self.draw_squares(win)
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board[row][column]
                if piece != 0: #if the square value is not zero, then draw the piece
                    piece.draw(win)
                    
    def remove(self, pieces):  #to remove pieces when a player jumps
        for piece in pieces:
            self.board[piece.row][piece.column] = 0  #to replace the piece place with zero to indicate there is no piece
            if piece != 0:
                #decreasing the number of pieces of the player with the removed piece
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
                    
    def winner(self): #to determine if there is a winner
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        
        return None
    
    def move(self, piece, row, column):
        self.board[piece.row][piece.column], self.board[row][column] = self.board[row][column], self.board[piece.row][piece.column]
        piece.move(row, column)
        # check to see if current position is the last or first row to make a king
        if row == ROWS-1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1
                
    def get_valid_moves(self, piece):
        moves = {} #a dictionary
        left = piece.column - 1
        right = piece.column + 1
        row = piece.row
        
        if piece.color == RED or piece.king:
            moves.update(self.go_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self.go_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self.go_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self.go_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves
    
    def go_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0: #to prevent going outside the board
                break
            
            current = self.board[r][left]
            if current == 0: #if the wanted cell is clear
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self.go_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self.go_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color: #if the same player on the wanted cell
                break
            else: #if the enemy is on the wanted cell
                last = [current]

            left -= 1
        
        return moves

    def go_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLUMNS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self.go_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self.go_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
    
    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5) 
    
    def get_all_pieces(self, color):
        checkers = []
        for row in self.board:
            for checker in row:
                if checker != 0 and checker.color == color:
                    checkers.append(checker)
        return checkers

###################################################################################################################
#                                              game
class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, column):
        if self.selected:
            result = self._move(row, column)
            if not result:
                self.selected = None
                self.select(row, column)

        piece = self.board.get_piece(row, column)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, column):
        piece = self.board.get_piece(row, column)
        if self.selected and piece == 0 and (row, column) in self.valid_moves:
            self.board.move(self.selected, row, column)
            skipped = self.valid_moves[(row, column)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()


######################################################################################################################
#                                             algorithms

from copy import deepcopy

def alphabeta(board, tree_depth, alpha, beta, cpu_turn):
    if tree_depth == 0 or board.winner() != None:
        return board.evaluate(), board

    if cpu_turn:
        max_score = float('-inf')
        best_move = None
        for move in get_all_moves(board, WHITE):
            score = alphabeta(move, tree_depth - 1, alpha, beta, False)[0] 
            max_score = max(max_score, score)
            if max_score == score:
                best_move = move
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return max_score, best_move
    else:
        min_score = float('inf')
        best_move = None
        for move in get_all_moves(board, RED):
            score = alphabeta(move, tree_depth - 1, alpha, beta, True)[0]
            min_score = max(min_score, score)
            if min_score == score:
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break
        return min_score, best_move


def minimax(board, tree_depth, cpu_turn):
    if tree_depth == 0 or board.winner() != None:
        return board.evaluate(), board

    if cpu_turn:
        max_score = float('-inf')
        best_move = None
        for move in get_all_moves(board, WHITE):
            score = minimax(move, tree_depth - 1, False)[0]
            max_score = max(max_score, score)
            if max_score == score:
                best_move = move
        return max_score, best_move
    else:
        min_score = float('inf')
        best_move = None
        for move in get_all_moves(board, RED):
            score = minimax(move, tree_depth - 1, True)[0]
            min_score = min(min_score, score)
            if min_score == score:
                best_move = move
        return min_score, best_move
    
import random

def random_agent(board, color):
    moves = get_all_moves(board, color)
    return random.choice(moves)

def get_all_moves(board, color):
    moves = []
    for checker in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(checker)
        for move, skip in valid_moves.items():
            board_copy = deepcopy(board)
            checker_copy = board_copy.get_piece(checker.row, checker.column)
            new_board = simulate_move(checker_copy, move, board_copy, skip)
            moves.append(new_board)

    return moves

def simulate_move(checker, move, board, skip):
    board.move(checker, move[0], move[1])
    if skip:
        board.remove(skip)
    
    return board


###########################################################################################################################
#                                             main
# Frames per Second
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
global difficulty_level 
difficulty_level = 1

def draw_winner(winner): 
        run = True
        pygame.display.set_caption('GAME OVER')
        while run:
            WIN.fill(GREY)
            pygame.font.init()
            font = pygame.font.SysFont('arial', 60)
            font2 = pygame.font.SysFont('arial',40)
            WIN.blit(font.render("GAME OVER", True, YELLOW), (150,150))
            if winner == WHITE:
                line2 = font2.render("WHITE (AGENT) WON", True, YELLOW)
            else:
                line2 = font2.render("RED (RANDOM) WON", True, YELLOW)       
            text_rect = line2.get_rect()
            text_rect.center = (WIDTH/2, HEIGHT/2-20)
            WIN.blit(line2,text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()
        pygame.quit()
import pygame_gui
def selections():
    pygame.init()

    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((600, 600))

    algorithm_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((250, 75), (100, 50)),
                                             text='Algorithm',
                                             manager=manager)

    algorithm_options = ['Alpha-beta', 'Minimax']
    algorithm_select = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((250, 125), (100, 75)),
                                                       item_list=algorithm_options,
                                                       manager=manager)

    difficulty_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((250, 225), (100, 50)),
                                               text='Difficulty',
                                               manager=manager)

    difficulty_options = ['Easy', 'Hard']
    difficulty_select = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((250, 275), (100, 75)),
                                                        item_list=difficulty_options,
                                                        manager=manager)

    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 375), (100, 50)),
                                            text='Start',
                                            manager=manager)

    run = True
    while run:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        algorithm = algorithm_select.get_single_selection()
                        difficulty = difficulty_select.get_single_selection()
                        return algorithm, difficulty
                        # Pass the selected algorithm and difficulty to your main function here

            manager.process_events(event)

        manager.update(time_delta)
        screen.fill((255, 255, 255))
        manager.draw_ui(screen)
        pygame.display.update()
        
def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    pygame.display.set_caption('Checkers')
    algorithm, difficulty =selections()
    if difficulty =='Easy':
        difficulty_level=1
    else:
        difficulty_level=3

    while run:
        clock.tick(FPS)

        
        if game.turn == WHITE:
            pygame.time.delay(100)
            if algorithm == 'Alpha-beta':
                value, new_board = alphabeta(game.get_board(), difficulty_level, -10000, 10000, WHITE)
            else:
                value, new_board = minimax(game.get_board(), difficulty_level, WHITE)
            game.ai_move(new_board) 
            
        else:
            # Random agent's turn
            pygame.time.delay(100) 
            move = random_agent(game.get_board(), RED)
            game.ai_move(move)
            
        if game.winner() != None:
            winner = game.winner()
            pygame.time.delay(1000)
            draw_winner(winner)
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                

        game.update()

   

main()
