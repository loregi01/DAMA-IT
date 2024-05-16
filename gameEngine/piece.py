from typing import List, Tuple

class Piece:
    def __init__(self, x: int, y: int, white: bool, board: List[List['Piece']]) -> None:
        self._n = 8
        self._x = x
        self._y = y
        self._white = white
        self._king = False
        self._pieceBoard = board
        self.end_up_point = []

    def white(self) -> bool:
        return self._white

    def x(self) -> int:
        return self._x

    def y(self) -> int:
        return self._y

    def king(self) -> bool:
        return self._king

    def setWhite(self, white: bool) -> None:
        self._white = white

    def setX(self, x: int) -> None:
        self._x = x

    def setY(self, y: int) -> None:
        self._y = y

    def setKing(self, king: bool) -> None:
        self._king = king

    #def _possibleMove(self) -> List[Tuple[int, int]]:
    #    return 0

    def validMove(self, x: int, y: int, eat: bool) -> bool:
        x = int(x)
        y = int(y)
        
        #Power for the distance 
        x2 = (self._x - x) ** 2
        y2 = (self._y - y) ** 2

        #Point in board
        if x >= self._n or y >= self._n:
            return False

        if x < 0 or y < 0:
            return False
        
        #Point is free
        if self._pieceBoard[y][x] != None:
            return False

        #Point is at distance , Point is diagonal
        if eat:
            if x2 + y2 != 8:
                return False
        else:
            if x2 + y2 != 2:
                return False
        
        return True

    
    #def can_eat(self) -> bool:
    #    return True

class Checker(Piece):

    def moveTo(self, x: int, y: int, ate: bool) -> Tuple[bool, bool]:
        ate = self.can_eat()
        x = int(x)
        y = int(y)
        if not self.validMove(x, y, ate):
            return False, ate

        if not ate:
            self._pieceBoard[y][x] = self
            self._pieceBoard[self._y][self._x] = None
            self._x = x
            self._y = y

        return True, ate
    
    def _possibleMove(self) -> List[Tuple[int, int]]:
        possibleMove = []

        if self._pieceBoard[self._y][self._x]:
            if self.can_eat():
                #print("we")
                #print(self.end_up_point)
                possibleMove = self.end_up_point
                #possibleMove.append(self.end_up_point[0][0])
                #possibleMove.append(self.end_up_point[0][1])
                #possibleMove.extend([self.end_up_point[0], self.end_up_point[1]])
            else:
                if self.validMove(self._x - 1, self._y - 1, False):
                    possibleMove.append((self._x - 1, self._y - 1))
                if self.validMove(self._x + 1, self._y - 1, False):
                    possibleMove.append((self._x + 1, self._y - 1))
                if self.validMove(self._x - 1, self._y + 1, False):
                    possibleMove.append((self._x - 1, self._y + 1))
                if self.validMove(self._x + 1, self._y + 1, False):
                    possibleMove.append((self._x + 1, self._y + 1))
        
        #print("Possible Move", possibleMove)

        return possibleMove

    def validMove(self, x: int, y: int, eat: bool) -> bool:
        x = int(x)
        y = int(y)
        if not super().validMove(x, y, eat):
            return False
        
        if not self._white:  # black up
            if self._y > y:
                return False
        
        if self._white:  # white down
            if self._y < y:
                return False

        return True

    def can_eat(self) -> bool:
        #global end_up_point
        self.end_up_point.clear()

        canEat = False
        
        if self.validMove(self._x + 2, self._y + 2, True):
            if self._pieceBoard[self._y + 1][self._x + 1] and self._pieceBoard[self._y + 1][self._x + 1].white() != self._white and not self._pieceBoard[self._y + 1][self._x + 1].king():
                canEat = True
                self.end_up_point.append((self._x + 2, self._y + 2))
        if self.validMove(self._x - 2, self._y + 2, True):
            if self._pieceBoard[self._y + 1][self._x - 1] and self._pieceBoard[self._y + 1][self._x - 1].white() != self._white and not self._pieceBoard[self._y + 1][self._x - 1].king():
                canEat = True
                self.end_up_point.append((self._x - 2, self._y + 2))
        if self.validMove(self._x - 2, self._y - 2, True):
            if self._pieceBoard[self._y - 1][self._x - 1] and self._pieceBoard[self._y - 1][self._x - 1].white() != self._white and not self._pieceBoard[self._y - 1][self._x - 1].king():
                canEat = True
                self.end_up_point.append((self._x - 2, self._y - 2))
        if self.validMove(self._x + 2, self._y - 2, True):
            if self._pieceBoard[self._y - 1][self._x + 1] and self._pieceBoard[self._y - 1][self._x + 1].white() != self._white and not self._pieceBoard[self._y - 1][self._x + 1].king():
                canEat = True
                self.end_up_point.append((self._x + 2, self._y - 2))
        #print("end up point", self.end_up_point)
        return canEat

class King(Piece):

    def moveTo(self, x: int, y: int, ate: bool) -> Tuple[bool, bool]:
        ate = self.can_eat()

        x = int(x)
        y = int(y)

        if not self.validMove(x, y, ate):
            return False, ate

        if not ate:
            self._pieceBoard[y][x] = self
            self._pieceBoard[self._y][self._x] = None
            self._x = x
            self._y = y

        return True, ate

    def _possibleMove(self) -> List[Tuple[int, int]]:
        possibleMove = []

        if self._pieceBoard[self._y][self._x]:
            if self.can_eat():
                possibleMove.extend(self.end_up_point)
            else:
                if self.validMove(self._x - 1, self._y - 1, False):
                    possibleMove.append((self._x - 1, self._y - 1))
                if self.validMove(self._x + 1, self._y - 1, False):
                    possibleMove.append((self._x + 1, self._y - 1))
                if self.validMove(self._x - 1, self._y + 1, False):
                    possibleMove.append((self._x - 1, self._y + 1))
                if self.validMove(self._x + 1, self._y + 1, False):
                    possibleMove.append((self._x + 1, self._y + 1))
        
        return possibleMove

    def validMove(self, x: int, y: int, eat: bool) -> bool:
        x = int(x)
        y = int(y)
        if not super().validMove(x, y, eat):
            return False
        return True

    def can_eat(self) -> bool:
        #global end_up_point
        self.end_up_point.clear()

        canEat = False

        if self.validMove(self._x + 2, self._y + 2, True):
            if self._pieceBoard[self._y + 1][self._x + 1] and self._pieceBoard[self._y + 1][self._x + 1].white() != self._white:
                canEat = True
                self.end_up_point.append((self._x + 2, self._y + 2))
        if self.validMove(self._x - 2, self._y + 2, True):
            if self._pieceBoard[self._y + 1][self._x - 1] and self._pieceBoard[self._y + 1][self._x - 1].white() != self._white:
                canEat = True
                self.end_up_point.append((self._x - 2, self._y + 2))
        if self.validMove(self._x - 2, self._y - 2, True):
            if self._pieceBoard[self._y - 1][self._x - 1] and self._pieceBoard[self._y - 1][self._x - 1].white() != self._white:
                canEat = True
                self.end_up_point.append((self._x - 2, self._y - 2))
        if self.validMove(self._x + 2, self._y - 2, True):
            if self._pieceBoard[self._y - 1][self._x + 1] and self._pieceBoard[self._y - 1][self._x + 1].white() != self._white:
                canEat = True
                self.end_up_point.append((self._x + 2, self._y - 2))

        return canEat
