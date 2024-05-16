from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem
from PySide6.QtGui import QPainter, QColor, QPixmap, QPen, QBrush
from PySide6.QtCore import Qt, QPointF, QLineF

from typing import List

class Cell(QGraphicsRectItem):
    EMPTY = 0
    PIECE_W = 1
    PIECE_B = 2
    P_DAMA_W = 3
    P_DAMA_B = 4

    cellsize = 100
    color_dark = QColor(139, 69, 19)
    color_bright = QColor(205, 133, 63)
    color_over = QColor(255, 228, 181)
    color_selected = QColor(255, 255, 0)

    #graphics
    pieces = []  # Assuming this will be initialized somewhere in the code
    
    from views.board import Board
    def __init__(self, board: Board, bx: int, by: int):
        super().__init__()
        self._x = bx
        self._y = by
        self._content = Cell.EMPTY
        self._board = board
        self._selected = False
        self._mouseover = False
        self._suggested = False
        self._draggable = False
        self.setZValue(0)

        if self._y % 2 == 0:
            self._color = self.color_dark if self._x % 2 == 0 else self.color_bright
        else:
            self._color = self.color_bright if self._x % 2 == 0 else self.color_dark

        if not Cell.pieces:
            Cell.pieces.append(QPixmap("views/graphics/pawnW.png").scaled(1.2 * Cell.cellsize, 1.2 * Cell.cellsize, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            Cell.pieces.append(QPixmap("views/graphics/pawnB.png").scaled(1.2 * Cell.cellsize, 1.2 * Cell.cellsize, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            Cell.pieces.append(QPixmap("views/graphics/damaW.png").scaled(1.2 * Cell.cellsize, 1.2 * Cell.cellsize, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            Cell.pieces.append(QPixmap("views/graphics/damaB.png").scaled(1.2 * Cell.cellsize, 1.2 * Cell.cellsize, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)
        self.setRect(Cell.cellsize * self._x, Cell.cellsize * self._y, Cell.cellsize, Cell.cellsize)

    def setContent(self, newContent):
        self._content = newContent
        self.update()

    def setSelected(self, selected):
        self._selected = selected
        self.update()

    def setSuggested(self, suggested):
        self._suggested = suggested
        self.setZValue(suggested)
        self.update()

    def clear_selected_cells(self):
        for i in range(8):
            for j in range(8):
                self._board._cells[i][j].setSelected(False)
                self._board._cells[i][j].setSuggested(False)

    def mouseMoveEvent(self, event):
        #if self._board._game.isThinking():
        #    return
        
        if self._board._cells[self._y][self._x]._content == Cell.EMPTY:
            return

        '''if self._board.forced_cells():
            continuare = False
            for c in self._board._game._forced_moves:
                if self._x == c.front() % 8 and self._y == c.front() / 8:
                    continuare = True
            if not continuare:
                return
'''
        self._selected = True

        '''if self._board._game.pieceBoard()[self._y][self._x]:
            pMove = self._board._game.pieceBoard()[self._y][self._x]._possibleMove()
            for move in pMove:
                self._board._cells[move.second][move.first].setSelected(True)
                '''
        
        self._draggable = True
        self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if not self._selected:
            return

        if self._board._cells[self._y][self._x]._content == Cell.EMPTY:
            return

        prev_x = self._x
        prev_y = self._y
        doMove = False
        if self._draggable:
            pMove = self._board._game.pieceBoard()[self._y][self._x]._possibleMove()
            print("pMove", pMove)
            colItems = self.collidingItems()
            #print("WE")
            #print(colItems)
            #if colItems.isEmpty():
            if not colItems:
                self._x = QPointF(self.scenePos()).x()
                self._y = QPointF(self.scenePos()).y()
            else:
                closestItem = None
                shortestDist = 100
                for item in colItems:
                    line = QLineF(item.sceneBoundingRect().center(), self.sceneBoundingRect().center())
                    for p in pMove:
                        if item.pos().x() == p[0] and item.pos().y() == p[1]:
                            if line.length() < shortestDist:
                                shortestDist = line.length()
                                closestItem = item
                             
                if closestItem is not None:
                    self._x = QPointF(closestItem.scenePos()).x()
                    self._y = QPointF(closestItem.scenePos()).y()
                    doMove = True
            self._draggable = False
            

        self.clear_selected_cells()
        
        if doMove:
            self._board.move(prev_x, prev_y, self._x, self._y)

        self._board._cells[prev_y][prev_x].setPos(QPointF(prev_x, prev_y))
        self._board._cells[prev_y][prev_x]._x = prev_x
        self._board._cells[prev_y][prev_x]._y = prev_y

        self._selected = False
        self.update()
        super().mouseReleaseEvent(event)

    def hoverEnterEvent(self, e):
        self._mouseover = True
        self.update()

    def hoverLeaveEvent(self, e):
        self._mouseover = False
        self.update()

    def paint(self, painter: QPainter, option, widget):
        painter.setRenderHint(QPainter.TextAntialiasing)

        if self._suggested and not self._draggable:
            painter.setRenderHint(QPainter.HighQualityAntialiasing)
            pen = QPen(QBrush(Qt.yellow if self._suggested else Qt.red), 4, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin)
            painter.setPen(pen)
        else:
            painter.setPen(Qt.NoPen)

        if self._draggable:
            self.setZValue(2)
            painter.setBrush(Qt.transparent)
        else:
            painter.setBrush(QBrush(self._color))
            if not self._suggested:
                pen = QPen(QColor(0, 0, 0), 2, Qt.SolidLine)
                painter.setPen(pen)

        painter.drawRect(self.rect())

        if (self._mouseover or self._selected) and not self._draggable:
            painter.setOpacity(0.3)
            if self._selected:
                painter.setBrush(QBrush(self.color_selected))
            else:
                painter.setBrush(QBrush(self.color_over))
            painter.drawRect(self.rect())
            painter.setOpacity(1.0)

        if self._content:
            painter.drawPixmap(self.rect().topLeft() - QPointF(0.1 * Cell.cellsize, 0.1 * Cell.cellsize), Cell.pieces[self._content - 1])
