class GameState():
    def __init__(self):
        self.board = [["--","rs","--","rs","--","rs","--","rs"],
                 ["rs","--","rs","--","rs","--","rs","--"],
                 ["--","rs","--","rs","--","rs","--","rs"],
                 ["--","--","--","--","--","--","--","--"],
                 ["--","--","--","--","--","--","--","--"],
                 ["bs","--","bs","--","bs","--","bs","--"],
                 ["--","bs","--","bs","--","bs","--","bs"],
                 ["bs","--","bs","--","bs","--","bs","--"]]
        self.redTurn = True
        self.moveLog = []
        self.redsCaptured = 0
        self.blacksCaptured = 0

    def changeTurn(self):
        self.redTurn = not self.redTurn

    def makeMove(self, move):
        moves, killMoves = self.getAllValidMoves()

        for i in range(len(killMoves)):
            killMove = killMoves[i]
            if (killMove.startRow, killMove.startCol) == (move.startRow, move.startCol):
                if (killMove.endRow, killMove.endCol) == (move.endRow, move.endCol):
                    self.board[move.startRow][move.startCol] = "--"
                    self.board[killMove.capturedRow][killMove.capturedCol] = "--"
                    self.board[move.endRow][move.endCol] = move.startPiece
                    if killMove.capturedPiece[0] == "r":
                        self.redsCaptured += 1
                    elif killMove.capturedPiece[0] == "b":
                        self.blacksCaptured += 1
                    self.moveLog.append(move)
                    self.changeTurn()


        for i in range(len(moves)):
            m = moves[i]
            if (m.startRow, m.startCol) == (move.startRow, move.startCol):
                if (m.endRow, m.endCol) == (move.endRow, move.endCol):
                    self.board[move.startRow][move.startCol] = "--"
                    self.board[move.endRow][move.endCol] = move.startPiece
                    self.moveLog.append(move)
                    self.changeTurn()


    def undoMove(self):
        if len(self.moveLog) != 0:
            lastMove = self.moveLog.pop()
            self.board[lastMove.startRow][lastMove.startCol] = lastMove.startPiece
            self.board[lastMove.endRow][lastMove.endCol] = lastMove.endPiece
            self.changeTurn()

    def getAllValidMoves(self):
        moves = []
        kills = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                cell = self.board[r][c]
                turn = cell[0]
                piece = cell[1]

                # generate moves for single checkers piece
                if piece == "s":
                    if (turn == "r" and self.redTurn):  # red moves downward
                        # Normal moves
                        if r < (len(self.board) - 1):
                            if c > 0:
                                if self.board[r+1][c-1] == "--": # Bottom Left Cell Empty ?
                                    moves.append(Move((r, c), (r+1, c-1), (-1, -1), (-1, -1), self.board))
                            if c < (len(self.board[r]) - 1):
                                if self.board[r+1][c+1] == "--": # Bottom Right Cell Empty ?
                                    moves.append(Move((r, c), (r+1, c+1), (-1, -1), (-1, -1), self.board))
                        # Kills
                        if r < (len(self.board) - 2):
                            if c > 1:
                                if self.board[r+1][c-1][0] == "b" and self.board[r+2][c-2] == "--":
                                    # if other piece below and to the left, and empty space behind it
                                    kills.append(Move((r, c), (r+2, c-2), (r+1, c-1), (-1, -1), self.board))
                                    # Check for double kill
                            if c < (len(self.board[r]) - 2):
                                if self.board[r+1][c+1][0] == "b" and self.board[r+2][c+2] == "--":
                                    # if other piece below and to the right, and empty space behind it
                                    kills.append(Move((r, c), (r+2, c+2), (r+1, c+1), (-1, -1), self.board))
                                    # Check for double kill
                    elif (turn == "b" and not self.redTurn):  # black moves upward
                        # Normal moves
                        if r > 0:
                            if c > 0:
                                if self.board[r-1][c-1] == "--": # Top Left Cell Empty ?
                                    moves.append(Move((r, c), (r-1, c-1), (-1, -1), (-1, -1), self.board))
                            if c < (len(self.board[r]) - 1):
                                if self.board[r-1][c+1] == "--": # Top Right Cell Empty ?
                                    moves.append(Move((r, c), (r-1, c+1), (-1, -1), (-1, -1), self.board))
                        # Kills
                        if r > 1:
                            if c > 1:
                                if self.board[r-1][c-1][0] == "r" and self.board[r-2][c-2] == "--":
                                    # if other piece up and to the left, and empty space behind it
                                    kills.append(Move((r, c), (r-2, c-2), (r-1, c-1), (-1, -1), self.board))
                                    # Check for double kill
                            if c < (len(self.board[r]) - 2):
                                if self.board[r-1][c+1][0] == "r" and self.board[r-2][c+2] == "--":
                                    # if other piece up and to the right, and empty space behind it
                                    kills.append(Move((r, c), (r-2, c+2), (r-1, c+1), (-1, -1), self.board))
                                    # Check for double kill

        return moves, kills


class Move():
    def __init__(self, startCell, endCell, capturedCell, doubleCapturedCell, board):
        self.startRow, self.startCol = startCell
        self.startPiece = board[self.startRow][self.startCol]

        self.endRow, self.endCol = endCell
        self.endPiece = board[self.endRow][self.endCol]

        self.capturedRow, self.capturedCol = capturedCell
        self.capturedPiece = board[self.capturedRow][self.capturedCol]

        if not len(doubleCapturedCell) == 0:
            self.doubleCapturedRow, self.doubleCapturedCol = doubleCapturedCell
            self.doubleCapturedPiece = board[self.doubleCapturedRow][self.doubleCapturedCol]
