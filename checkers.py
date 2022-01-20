import pygame
import checkersEngine

#CONSTANTS
WIDTH = 960
HEIGHT = 720
DIMENSION = 8
BOARD_WIDTH = 600
X_START = (WIDTH-BOARD_WIDTH)/2
Y_START = (HEIGHT-BOARD_WIDTH)/2
CELL_WIDTH = BOARD_WIDTH/DIMENSION
PIECE_SIZE = 64
IMAGES = {}

# PYGAME SETUP
window = pygame.display.set_mode((WIDTH, HEIGHT),pygame.DOUBLEBUF, 32)
pygame.display.set_caption("Checkers")

def loadImages():
    pieces = ['rs', 'bs']
    for piece in pieces:
        IMAGES[piece] = pygame.image.load("res/"+piece+".png")

def draw_checkerboard(window):
    #pygame.draw.rect(window, (255,255,255), pygame.Rect(X_START-3, Y_START-3, BOARD_WIDTH+6, BOARD_WIDTH+6))
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if i % 2 == 0:
                if j % 2 == 0:
                    color = (255, 0, 0)
                else:
                    color = (0, 0, 0)
            else:
                if j%2 == 0:
                    color = (0, 0, 0)
                else:
                    color = (255,0,0)
            pygame.draw.rect(window, color, pygame.Rect(X_START + i*CELL_WIDTH, Y_START + j*CELL_WIDTH, CELL_WIDTH, CELL_WIDTH))

def draw_pieces(window, board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if not board[i][j] == "--":
                piece_x = X_START + j*CELL_WIDTH + CELL_WIDTH/2 - PIECE_SIZE/2
                piece_y = Y_START + i*CELL_WIDTH + CELL_WIDTH/2 - PIECE_SIZE/2
                window.blit(IMAGES[board[i][j]], (piece_x, piece_y))
                #pygame.draw.ellipse(window, color, (piece_x, piece_y, PIECE_SIZE, PIECE_SIZE))

def highlight_selected(window, selectedSquare):
    if not selectedSquare == ():
        i = selectedSquare[1]
        j = selectedSquare[0]
        pygame.draw.rect(window, (200,200,200), pygame.Rect(X_START + i*CELL_WIDTH, Y_START + j*CELL_WIDTH, CELL_WIDTH, CELL_WIDTH))

def highlight_moves_captures(window, moves, kills, selectedSquare):
    blue_cells = []  # valid moves
    red_cells = []  # valid captures
    if not selectedSquare == ():
        for move in moves:
            if (move.startRow, move.startCol) == selectedSquare:
                blue_cells.append((move.endRow, move.endCol))
        for kill in kills:
            if (kill.startRow, kill.startCol) == selectedSquare:
                red_cells.append((kill.capturedRow, kill.capturedCol))
                blue_cells.append((kill.endRow, kill.endCol))
        for cell in blue_cells:
            i = cell[1]
            j = cell[0]
            pygame.draw.rect(window, (100,100,200), pygame.Rect(X_START + i*CELL_WIDTH, Y_START + j*CELL_WIDTH, CELL_WIDTH, CELL_WIDTH))
        for cell in red_cells:
            i = cell[1]
            j = cell[0]
            pygame.draw.rect(window, (200,100,100), pygame.Rect(X_START + i*CELL_WIDTH, Y_START + j*CELL_WIDTH, CELL_WIDTH, CELL_WIDTH))

def draw_captured(window, redsCaptured, blacksCaptured):
    for i in range(redsCaptured):
        img = pygame.transform.scale(IMAGES["rs"], (40, 40))
        window.blit(img, (X_START + BOARD_WIDTH + 5, Y_START + BOARD_WIDTH - 40 -i*(PIECE_SIZE-20)))
    for i in range(blacksCaptured):
        img = pygame.transform.scale(IMAGES["bs"], (40, 40))
        window.blit(img, (X_START - 40, Y_START + i*(PIECE_SIZE-20)))


def draw_turn(window, redTurn):
    img = 0;
    if(redTurn):
        img = IMAGES["rs"]
    else:
        img = IMAGES["bs"]
    window.blit(img, (20, 20))



def drawGameBoard(window, board, selectedSquare, moves, kills, redsCaptured, blacksCaptured, redTurn):
    draw_checkerboard(window)
    highlight_selected(window, selectedSquare)
    highlight_moves_captures(window, moves, kills, selectedSquare)
    draw_pieces(window, board)  # Draw all the pices on the board
    draw_captured(window, redsCaptured, blacksCaptured)  # Draw captured piceces along side of the board
    draw_turn(window, redTurn)  # Draw who's turn it is in top left corner


def main():
    FPS = 60  # max fps
    running = True  # running or not
    gs = checkersEngine.GameState()  # Initialize gamestate
    clock = pygame.time.Clock()  # Initialize clock

    loadImages()  # Function that loads all resources

    selectedSquare = () # tuple keeping track of current selected square
    lastClicked = [] # list of tuples containing up to 2 points

    # Game Loop
    while running:
        clock.tick(FPS)  # Keep steady framerate
        pygame.display.update()  # Update pygame display
        pygame.draw.rect(window, (60,60,60), pygame.Rect(0, 0, WIDTH, HEIGHT)) # Background

        moves, kills = gs.getAllValidMoves()  # Get valid moves and kills

        # Draw Game Board
        drawGameBoard(window, gs.board, selectedSquare, moves, kills, gs.redsCaptured, gs.blacksCaptured, gs.redTurn)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # EXIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos  # Get mouse position
                # If click within board
                if mouse_x > X_START and mouse_y > Y_START and mouse_x < X_START+BOARD_WIDTH and mouse_y < Y_START+BOARD_WIDTH:
                    col = int((mouse_x - X_START) // CELL_WIDTH)
                    row = int((mouse_y - Y_START) // CELL_WIDTH)
                    if len(lastClicked) == 0 and not gs.board[row][col] == "--" or len(lastClicked) > 0:  # MAKE SURE YOU DONT START ON EMPTY CELL
                        if selectedSquare == (row, col):
                            selectedSquare = () # deselect
                            lastClicked = []
                        else:
                            selectedSquare = (row, col)
                            lastClicked.append(selectedSquare)
                            if len(lastClicked) == 2:
                                # MOVE
                                move = checkersEngine.Move(lastClicked[0], lastClicked[1], (-1, -1), (-1, -1), gs.board)
                                gs.makeMove(move)
                                # CLEAR VARIABLES, SWITCH TURNS
                                selectedSquare = ()
                                lastClicked = []
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gs.undoMove()



if __name__ == "__main__":
    main()
