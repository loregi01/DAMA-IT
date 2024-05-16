from typing import List, Tuple
import random

class Move:
    from gameEngine.piece import Piece, Checker, King
    def __init__(self, moved: Piece, x0: int, y0: int, x1: int, y1: int, eaten: Piece, multiple_eat: bool):
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1
        self._moved = moved
        self._eaten = eaten
        self._multiple_eat = multiple_eat


class Game:
    def __init__(self, difficulty: int, first_player: bool, up: bool, turn: bool):
        self._n = 8
        self._pieceBoard = [[None for _ in range(self._n)] for _ in range(self._n)]
        self._myTurn = first_player
        self._isThinking = False
        #self._difficulty = difficulty
        self._moves = []
        self._forced_moves = []
        self._black_pieces_left = []
        self._white_pieces_left = []
        from gameEngine.piece import Piece, Checker, King
        i = 0
        j = 0
        for i in range(self._n):
            for j in range(self._n):
                if j % 2 == 0 and (i == 0 or i == 2):
                    self._pieceBoard[i][j] = Checker(j, i, False, self._pieceBoard)
                    self._black_pieces_left.append(i * self._n + j)
                elif j % 2 != 0 and i == 1:
                    self._pieceBoard[i][j] = Checker(j, i, False, self._pieceBoard)
                    self._black_pieces_left.append(i * self._n + j)
                elif j % 2 != 0 and (i == 5 or i == 7):
                    self._pieceBoard[i][j] = Checker(j, i, True, self._pieceBoard)
                    self._white_pieces_left.append(i * self._n + j)
                elif j % 2 == 0 and i == 6:
                    self._pieceBoard[i][j] = Checker(j, i, True, self._pieceBoard)
                    self._white_pieces_left.append(i * self._n + j)
        
        #if not first_player and difficulty != 0:
        #    self.start()

    #def run(self):
    #    pass

    def transform(self, x: int, y: int) -> bool:
        x = int(x)
        y = int(y)
        if self._pieceBoard[y][x].white() and y == 0:
            return True
        if not self._pieceBoard[y][x].white() and y == 7:
            return True
        return False

    def myTurn(self) -> bool:
        return self._myTurn

    def isThinking(self) -> bool:
        return self._isThinking

    def move_size(self) -> int:
        return len(self._moves)

    def setMyTurn(self, mt: bool):
        self._myTurn = mt

    from gameEngine.piece import Piece, Checker, King
    def pieceBoard(self) -> List[List[Piece]]:
        return self._pieceBoard

    def black_pieces_left(self) -> List[int]:
        return self._black_pieces_left

    def white_pieces_left(self) -> List[int]:
        return self._white_pieces_left

    def move(self, x0, y0, x1, y1, multiple_eat) -> Tuple[bool, bool]:
        x0 = int(x0)
        y0 = int(y0)
        x1 = int(x1)
        y1 = int(y1)

        if not self._pieceBoard[y0][x0]:
            return False, multiple_eat

        white = self._pieceBoard[y0][x0].white()
        ate = False

        rightMove = False
        app = 0
        if self._forced_moves:
            for vp in self._forced_moves:
                if vp[0] % self._n == x0 and vp[0] // self._n == y0:
                    if vp[1] % self._n == x1 and vp[1] // self._n == y1:
                        rightMove = True
                        app = len(vp)
            
            if not rightMove:
                return False, multiple_eat
            
            if app > 2:
                multiple_eat = True
                m = self._forced_moves[:]
                for vp in m:
                    if vp[0] % self._n != x0 or vp[0] // self._n != y0:
                        if vp[1] % self._n != x1 or vp[1] // self._n != y1:
                            self._forced_moves.remove(vp)
            
            for vp in self._forced_moves:
                vp.pop(0)

        boolMove, ate = self._pieceBoard[y0][x0].moveTo(x1, y1, ate)
        #print("BOOL MOVE", boolMove)

        if not boolMove:
            return False, multiple_eat

        if ate:
            eat_king = False
            eat_king = self.eat(x0, y0, x1, y1, multiple_eat, eat_king)

            if white:
                self._black_pieces_left.remove(self._moves[-1]._eaten._y * self._n + self._moves[-1]._eaten._x)
            else:
                self._white_pieces_left.remove(self._moves[-1]._eaten._y * self._n + self._moves[-1]._eaten._x)
        else:
            self._moves.append(Move(self._pieceBoard[y1][x1], x0, y0, x1, y1, 0, multiple_eat))

        if self.transform(x1, y1):
            c = True
            if not self._pieceBoard[y1][x1].white():
                c = False
            self._pieceBoard[y1][x1] = None
            from gameEngine.piece import King
            self._pieceBoard[y1][x1] = King(x1, y1, c, self._pieceBoard)
            self._pieceBoard[y1][x1].setKing(True)

        if not white:
            self._black_pieces_left.append(y1 * self._n + x1)
            self._black_pieces_left.remove(y0 * self._n + x0)
        else:
            self._white_pieces_left.append(y1 * self._n + x1)
            self._white_pieces_left.remove(y0 * self._n + x0)

        #change turn, solo se non è in corso una mangiata multipla
        if not multiple_eat:
            self._myTurn = not self._myTurn

        return True, multiple_eat
    def eat(self, x0, y0, x1, y1, multiple_eat, eat_king) -> bool:
        x0 = int(x0)
        y0 = int(y0)
        x1 = int(x1)
        y1 = int(y1)        
        #coordinates of eat piece
        xy0 = y0 * 8 + x0
        xy1 = y1 * 8 + x1
        a = abs(xy1 - xy0) // 2
        m = max(xy0, xy1) - a
        xe = m % 8
        ye = m // 8

        self._moves.append(Move(self._pieceBoard[y0][x0], x0, y0, x1, y1, self._pieceBoard[ye][xe], multiple_eat))

        self._pieceBoard[y1][x1] = self._moves[-1]._moved
        self._pieceBoard[y1][x1]._x = self._moves[-1]._x1
        self._pieceBoard[y1][x1]._y = self._moves[-1]._y1

        self._pieceBoard[y0][x0] = None

        if self._pieceBoard[ye][xe].king():
            eat_king = True
        else:
            eat_king = False

        self._pieceBoard[ye][xe] = None
        return eat_king
    
    
    def undoForEat(self):
        if not self._moves:
            return

        last_move = self._moves.pop()

        self._pieceBoard[last_move._y0][last_move._x0] = last_move._moved
        self._pieceBoard[last_move._y0][last_move._x0]._x = last_move._x0
        self._pieceBoard[last_move._y0][last_move._x0]._y = last_move._y0

        if last_move._eaten:
            xy0 = last_move._y0 * 8 + last_move._x0
            xy1 = last_move._y1 * 8 + last_move._x1
            a = abs(xy1 - xy0) // 2
            m = max(xy0, xy1) - a
            xe = m % 8
            ye = m // 8
            xe = int(xe)
            ye = int(ye)
            self._pieceBoard[ye][xe] = last_move._eaten
            self._pieceBoard[ye][xe]._x = xe
            self._pieceBoard[ye][xe]._y = ye

        self._pieceBoard[last_move._y1][last_move._x1] = None

    def best_eat(self, x_start, y_start, l, n_king, paths) -> Tuple[bool, int, int, List[List[int]]]:
        x_start = int(x_start)
        y_start = int(y_start)

        if not self._pieceBoard[y_start][x_start].can_eat():
            #print("not eat")
            return False, l, n_king, paths
        #print("eat")
        i = 0
        n = 0
        app = 0
        size = 0
        king = 0
        eat_king = False

        path_king = []
        app_path = []
        multiple_eat_piece = []

        app_path.append(y_start * self._n + x_start)
        while True:
            while self._pieceBoard[y_start][x_start].can_eat():
                size = len(self._pieceBoard[y_start][x_start].end_up_point)
                if size > 1:
                    if multiple_eat_piece:
                        if multiple_eat_piece[-1][0] == y_start * self._n + x_start:
                            if multiple_eat_piece[-1][1] < size:
                                for _ in range(size - multiple_eat_piece[-1][1]):
                                    self._pieceBoard[y_start][x_start].end_up_point.pop()
                        else:
                            multiple_eat_piece.append([y_start * self._n + x_start, size])
                    else:
                        multiple_eat_piece.append([y_start * self._n + x_start, size])

                eat_king = self.eat(x_start, y_start, self._pieceBoard[y_start][x_start].end_up_point[-1][0], self._pieceBoard[y_start][x_start].end_up_point[-1][1], False, eat_king)

                if eat_king:
                    king += 1

                x_start = self._moves[-1]._x1
                y_start = self._moves[-1]._y1

                app_path.append(y_start * self._n + x_start)

                i += 1

            path_king.append(king)

            app = i

            if multiple_eat_piece:
                while ((x_start != multiple_eat_piece[-1][0] % self._n or y_start != multiple_eat_piece[-1][0] // self._n) and app != 0) or ((x_start == multiple_eat_piece[-1][0] % self._n and y_start == multiple_eat_piece[-1][0] // self._n and multiple_eat_piece[-1][1] >= 1) and app != 0):
                    if x_start == multiple_eat_piece[-1][0] % self._n and y_start == multiple_eat_piece[-1][0] // self._n and multiple_eat_piece[-1][1] == 1:
                        multiple_eat_piece.pop()

                    if self._moves[-1]._eaten.king():
                        king -= 1
                    x_start = self._moves[-1]._x0
                    y_start = self._moves[-1]._y0
                    self.undoForEat()
                    app -= 1

                    if multiple_eat_piece:
                        if x_start == multiple_eat_piece[-1][0] % self._n and y_start == multiple_eat_piece[-1][0] // self._n and multiple_eat_piece[-1][1] == 1:
                            multiple_eat_piece.pop()
                            if app != 0:
                                if self._moves[-1]._eaten.king():
                                    king -= 1
                                x_start = self._moves[-1]._x0
                                y_start = self._moves[-1]._y0
                                self.undoForEat()
                                app -= 1

                    if not multiple_eat_piece:
                        break

                    if x_start == multiple_eat_piece[-1][0] % self._n and y_start == multiple_eat_piece[-1][0] // self._n and multiple_eat_piece[-1][1] > 1:
                        break

            if not multiple_eat_piece or (len(multiple_eat_piece) == 1 and multiple_eat_piece[-1][1] == 1):
                while app > 0:
                    if self._moves[-1]._eaten.king():
                        king -= 1
                    x_start = self._moves[-1]._x0
                    y_start = self._moves[-1]._y0
                    self.undoForEat()
                    app -= 1

            if multiple_eat_piece:
                if app == 0 and len(multiple_eat_piece) == 1 and multiple_eat_piece[-1][1] == 1:
                    multiple_eat_piece.pop()

            if multiple_eat_piece:
                if x_start == multiple_eat_piece[-1][0] % self._n and y_start == multiple_eat_piece[-1][0] // self._n and multiple_eat_piece[-1][1] != 1:
                    multiple_eat_piece[-1][1] -= 1
            #print("app_path", app_path)
            paths.append(app_path[:])

            n += 1

            if i != 0:
                for _ in range(i - app):
                    app_path.pop()
            else:
                app_path.clear()
                app_path.append(y_start * self._n + x_start)

            i = app

            if not multiple_eat_piece:
                break

        l = 0
        for q in paths:
            if len(q) >= l:
                l = len(q)

        n_king = 0
        i = 0
        for q in paths:
            if len(q) == l:
                if path_king[i] > n_king:
                    n_king = path_king[i]
            i += 1

        i = 0
        copy_paths = paths[:]
        #print("copy path", copy_paths)
        #print("paths", paths)
        for q in copy_paths:
            if len(q) != l:
                paths.remove(q)
            if len(q) == l and path_king[i] != n_king:
                paths.remove(q)
            i += 1

        return True, l, n_king, paths
    
    def eat_rules(self):
        self._forced_moves.clear()
        #print("turn", self._myTurn)
        if self._myTurn:
            ctr = self._white_pieces_left
        else:
            ctr =  self._black_pieces_left
        
        app_best = []
        lung_eat = 0
        app_lung_eat = 0
        n_king = 0
        app_n_king = 0
        
        for p in ctr:
            app_best.clear()

            boolBestEat, lung_eat, n_king, app_best = self.best_eat(p % self._n, p // self._n, lung_eat, n_king, app_best)
            #print("p", p)
            #print("lung_eat", lung_eat)
            #print("n_king", n_king)
            #print("app_best", app_best)
            if boolBestEat:
                if lung_eat > app_lung_eat:
                    app_lung_eat = lung_eat
                    app_n_king = n_king
                    self._forced_moves = app_best[:]
                elif lung_eat == app_lung_eat:
                    if not self._pieceBoard[p // self._n][p % self._n].king() and not self._pieceBoard[self._forced_moves[0][0] // self._n][self._forced_moves[0][0] % self._n].king():
                        for q in app_best:
                            self._forced_moves.append(q[:])
                    elif self._pieceBoard[p // self._n][p % self._n].king() and not self._pieceBoard[self._forced_moves[0][0] // self._n][self._forced_moves[0][0] % self._n].king():
                        self._forced_moves = app_best[:]
                    elif self._pieceBoard[p // self._n][p % self._n].king() and self._pieceBoard[self._forced_moves[0][0] // self._n][self._forced_moves[0][0] % self._n].king() and n_king >= app_n_king:
                        if app_n_king == n_king:
                            for q in app_best:
                                self._forced_moves.append(q[:])
                        else:
                            app_n_king = n_king
                            self._forced_moves = app_best[:]

        if not self._forced_moves:
            return False

        return True
    
    def draw(self):
        c = False
        if len(self._black_pieces_left) < 6 and len(self._white_pieces_left) < 6:
            for i in range(len(self._moves) - 1, len(self._moves) - 11, -1):
                if self._moves[i]._x0 == self._moves[i - 4]._x0:
                    if self._moves[i]._y0 == self._moves[i - 4]._y0:
                        c = True
                    else:
                        c = False
        return c

    def wins(self):
        if not self._black_pieces_left:
            return 1
        if not self._white_pieces_left:
            return 2
        no_moves_b = 1
        no_moves_w = 2

        for b in self._black_pieces_left:
            if self._pieceBoard[b // self._n][b % self._n]._possibleMove():
                no_moves_b = 0

        for b in self._white_pieces_left:
            if self._pieceBoard[b // self._n][b % self._n]._possibleMove():
                no_moves_w = 0

        if no_moves_b == 1:
            return 1
        if no_moves_w == 2:
            return 2
        return 0

    def ended(self):
        return self.wins() != 0


