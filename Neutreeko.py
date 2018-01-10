# -*- coding: utf-8 -*-
import NeutreekoAI

from enum import IntEnum
from copy import deepcopy

class PlayerColor(IntEnum):
    BLACK = 0
    WHITE = 1

    @staticmethod
    def getEnemyColor(playerColor):
        if playerColor == PlayerColor.BLACK:
            return PlayerColor.WHITE
        else:
            return PlayerColor.BLACK

class Pieces:
    @staticmethod
    def startPos():
        return [(4, 1), (1, 2), (4, 3), (0, 1), (3, 2), (0, 3)]

    @staticmethod
    def getPlayerPieces(pieces, playerColor):
        if playerColor == PlayerColor.BLACK:
            return pieces[:3]
        else:
            return pieces[3:]

    @staticmethod
    def sortY(pieces):
        return sorted(pieces, key=lambda n:n[0])

    @staticmethod
    def sortX(pieces):
        return sorted(pieces, key=lambda n: n[1])


class Board:

    @staticmethod
    def getLegalMoveDirections(pieces, playerColor):
        ret = []
        myPieces = Pieces.getPlayerPieces(pieces, playerColor)
        for i, (y,x) in enumerate(myPieces):
            # up = 0
            if not y == 0 and (y-1, x) not in pieces:
                ret.append((i, 0))
            # up-right = 1
            if not y == 0 and not x == 4 and (y-1, x+1) not in pieces:
                ret.append((i, 1))
            # right = 2
            if not x == 4 and (y, x+1) not in pieces:
                ret.append((i, 2))
            # right-down = 3
            if not y == 4 and not x == 4 and (y+1, x+1) not in pieces:
                ret.append((i, 3))
            # down = 4
            if not y == 4 and (y+1, x) not in pieces:
                ret.append((i, 4))
            # down-left = 5
            if not x == 0 and not y == 4 and (y+1,x-1) not in pieces:
                ret.append((i, 5))
            # left = 6
            if not x == 0 and (y,x-1) not in pieces:
                ret.append((i, 6))
            # up-left = 7
            if not x == 0 and not y == 0 and (y-1,x-1) not in pieces:
                ret.append((i, 7))
        return ret

    @staticmethod
    def applyMove(pieces, playerColor, movePieceNo, direction):
        srcPos = Pieces.getPlayerPieces(pieces, playerColor)[movePieceNo]
        distPos = srcPos

        # up
        if direction == 0:
            calcNext = lambda pos : (pos[0] - 1, pos[1])
            while True:
                if distPos[0] == 0 or calcNext(distPos) in pieces:
                    break
                distPos = calcNext(distPos)

        # up-right
        elif direction == 1:
            calcNext = lambda pos: (pos[0] - 1, pos[1] + 1)
            while True:
                if distPos[0] == 0 or distPos[1] == 4 or calcNext(distPos) in pieces:
                    break
                distPos = calcNext(distPos)

        # right
        elif direction == 2:
            calcNext = lambda pos: (pos[0], pos[1] + 1)
            while True:
                if distPos[1] == 4 or calcNext(distPos) in pieces:
                    break
                distPos = calcNext(distPos)

        # down-right
        elif direction == 3:
            calcNext = lambda pos: (pos[0] + 1, pos[1] + 1)
            while True:
                if distPos[0] == 4 or distPos[1] == 4 or calcNext(distPos) in pieces:
                    break
                distPos = calcNext(distPos)

        # down
        elif direction == 4:
            calcNext = lambda pos: (pos[0] + 1, pos[1])
            while True:
                if distPos[0] == 4 or calcNext(distPos) in pieces:
                    break
                distPos = calcNext(distPos)

        # down-left
        elif direction == 5:
            calcNext = lambda pos: (pos[0] + 1, pos[1] - 1)
            while True:
                if distPos[0] == 4 or distPos[1] == 0 or calcNext(distPos) in pieces:
                    break
                distPos = calcNext(distPos)

        # left
        elif direction == 6:
            calcNext = lambda pos: (pos[0], pos[1] - 1)
            while True:
                if distPos[1] == 0 or calcNext(distPos) in pieces:
                    break
                distPos = calcNext(distPos)

        # up-left
        elif direction == 7:
            calcNext = lambda pos: (pos[0] - 1, pos[1] - 1)
            while True:
                if distPos[0] == 0 or distPos[1] == 0 or calcNext(distPos) in pieces:
                    break
                distPos = calcNext(distPos)

        else:
            pass

        ret = deepcopy(pieces)
        ret[playerColor.value*3+movePieceNo] = distPos
        return ret

    @staticmethod
    def isWon(pieces, playerColor):
        myPieces = Pieces.sortX(Pieces.getPlayerPieces(pieces, playerColor))
        # horizontal
        if myPieces[0][0] == myPieces[1][0] == myPieces[2][0]:
            if myPieces[0][1] + 2 == myPieces[1][1] + 1 == myPieces[2][1]:
                return True
            else:
                return False

        # vertical
        myPieces = Pieces.sortY(myPieces)
        if myPieces[0][1] == myPieces[1][1] == myPieces[2][1]:
            if myPieces[0][0] + 2 == myPieces[1][0] + 1 == myPieces[2][0]:
                return True
            else:
                return False

        # diagonal
        if myPieces[0][0] + 2 == myPieces[1][0] + 1 == myPieces[2][0]:
            if (myPieces[0][1] + 2 == myPieces[1][1] + 1 == myPieces[2][1])\
            or (myPieces[0][1] == myPieces[1][1] + 1 == myPieces[2][1] + 2):
                return True
            else:
                return False
        return False



    @staticmethod
    def print(pieces):
        BLACK = ['⓿	','❶','❷']
        WHITE = ['⓪','①','②']
        out = ""
        grid = [['□' for i in range(5)] for j in range(5)]
        for i in range(3):
            grid[pieces[i][0]][pieces[i][1]] = BLACK[i]
            grid[pieces[i+3][0]][pieces[i+3][1]] = WHITE[i]
        for row in grid:
            out += "".join([str(p) for p in row]) + "\n"
        print(out)

class Game:
    def __init__(self):
        self._currentPieces = [0 for i in range(6)]
        self._myPlayerColor = None
        self._currentPlayerColor = PlayerColor.BLACK
        self._history = []

    def _input_y_n(self, str):
        while True:
            ans = input(str)
            if ans in ['y','Y']:
                return True
            elif ans in ['n', 'N']:
                return False
            print("input y or n")

    def _input_no(self, str, min, max):
        while True:
            try:
                ans = int(input(str))
                if ans >= min and ans <= max:
                    return ans
            except ValueError:
                pass
            print("invalid input")

    def _myTurn(self):
        moves = Board.getLegalMoveDirections(self._currentPieces, self._currentPlayerColor)
        print("Your turn!")
        while True:
            movePieceNo = self._input_no("Select the piece you move. (0-2) > ",0,2)
            print("0:UP, 1:UP-RIGHT, 2:RIGHT. 3:DOWN-RIGHT, 4:DOWN, 5:DOWN-LEFT, 6:LEFT, 7: UP - LEFT")
            direction = self._input_no("Which direction do you move? (0-7) > ",0,7)
            if (movePieceNo, direction) in moves:
                return (movePieceNo, direction)
            else:
                print("Can't move {0} to {1}!".format(movePieceNo, direction))


    def start(self):
        self._history = []
        self.isEnd = False
        self._currentPieces = Pieces.startPos()
        print("================================\n")

        if self._input_y_n("Do you get the first move? y/n > "):
             self._myPlayerColor = PlayerColor.BLACK
             print("You have BLACK")
        else:
            self._myPlayerColor = PlayerColor.WHITE
            print("You have WHITE")

        self.cpu = NeutreekoAI.NeutreekoAI(PlayerColor.getEnemyColor(self._myPlayerColor))

        print("Start Game\n\n")
        while not self.isEnd:
            Board.print(self._currentPieces)
            if self._currentPlayerColor == self._myPlayerColor:
                pieceNo, direction = self._myTurn()
            else:
                pieceNo, direction = self.cpu.doTurn(self._currentPieces)

            self._history.append((self._currentPieces[pieceNo + self._currentPlayerColor.value * 3], direction))
            self._currentPieces = Board.applyMove(self._currentPieces, self._currentPlayerColor, pieceNo, direction)
            print("{}\n".format(self._history[-1]))

            if Board.isWon(self._currentPieces, self._currentPlayerColor):
                self.isEnd = True
                Board.print(self._currentPieces)
                if self._myPlayerColor == self._currentPlayerColor:
                    print("You Win!")
                else:
                    print("You Lose!")
                print("History:\n{}".format(self._history))
            else:
                self._currentPlayerColor = PlayerColor.getEnemyColor(self._currentPlayerColor)

if __name__ == '__main__':
    game = Game()
    game.start()
