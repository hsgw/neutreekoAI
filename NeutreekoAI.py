# -*- coding: utf-8 -*-
import Neutreeko as Neu
import random, time

class NeutreekoAI:
    VALUE_MAX = 1000
    VALUE_MIN = -1000
    VALUE_WON = +10
    VALUE_LOSE = -10
    VALUE_CONTINUE = 0
    DEPTH = 5

    def __init__(self, playerColor):
        self._playerColor = playerColor
        self._enemyColor = Neu.PlayerColor.getEnemyColor(playerColor)
        self._isFirstSearch = True

    def doTurn(self, pieces):
        print("AI's turn!")
        print("Search next winning hands...")
        legalMoves = Neu.Board.getLegalMoveDirections(pieces, self._playerColor)
        # 次の手の中で勝つ手を探す
        for move in legalMoves:
            temp = Neu.Board.applyMove(pieces, self._playerColor, move[0], move[1])
            if Neu.Board.isWon(temp, self._playerColor):
                print("Winning Hand is Found!")
                return move[0], move[1]

        print("Not found")
        print("Search next losing hands...")
        moves = []
        # 次の手の中で負ける手を除外
        for move in legalMoves:
            loseFlag = False
            temp = Neu.Board.applyMove(pieces, self._playerColor, move[0], move[1])
            enemyMoves = Neu.Board.getLegalMoveDirections(temp, self._enemyColor)
            for enemyMove in enemyMoves:
                temp2 = Neu.Board.applyMove(pieces, self._enemyColor, enemyMove[0], enemyMove[1])
                if Neu.Board.isWon(temp2, self._enemyColor):
                    loseFlag = True
                    print("losing hand found! {0}".format(move))
                    continue
            if not loseFlag:
                moves.append(move)

        if len(moves) <= 0:
            print("Not found next hands...")
            return random.choice(legalMoves)
        elif len(moves) == 1:
            print("Only 1 moves found")
            return moves[0]

        print("Next Hands: {}".format(moves))
        print("Thinking...")
        start = time.time()
        value, selectedMoves, count = self._myTurn(pieces, moves, self.DEPTH)
        elapse = time.time() - start
        print("done! {}sec".format(elapse))

        print("{0}, {1} / count:{2}".format(value, selectedMoves, count))
        if len(selectedMoves) == 0:
            return random.choice(moves)

        return random.choice(selectedMoves)

    def _myTurn(self, pieces, moves, depth):
        if depth == 0:
            return self._evaluteValue(pieces)*depth, [], 1

        initialValue = self._evaluteValue(pieces)
        if initialValue != self.VALUE_CONTINUE:
            return initialValue*depth, [], 1

        totalValue = 0
        goodValue = self.VALUE_MIN
        goodMoves = []
        count = 0
        for move in moves:
            tempPieces = Neu.Board.applyMove(pieces, self._playerColor, move[0], move[1])
            tempMoves = Neu.Board.getLegalMoveDirections(tempPieces, self._enemyColor)
            v, m, c = self._enemyTurn(tempPieces, tempMoves, depth - 1)
            # print("my: {0},{1}".format(v,m))
            if v > goodValue:
                goodValue = v
                goodMoves = [move]
            elif v == goodValue:
                goodMoves.append(move)
            totalValue = totalValue + v
            count = count + c
        return totalValue, goodMoves, count

    def _enemyTurn(self, pieces, moves, depth):
        if depth == 0:
            return self._evaluteValue(pieces)*depth, [], 1

        initialValue = self._evaluteValue(pieces)
        if initialValue != self.VALUE_CONTINUE:
            return initialValue*depth, [], 1

        totalValue = 0
        goodValue = self.VALUE_MAX
        goodMoves = []
        count = 0
        for move in moves:
            tempPieces = Neu.Board.applyMove(pieces, self._enemyColor, move[0], move[1])
            tempMoves = Neu.Board.getLegalMoveDirections(tempPieces, self._playerColor)
            v, m, c = self._myTurn(tempPieces, tempMoves, depth - 1)
            # print("enemy: {0},{1}".format(v, m))
            if v < goodValue:
                goodValue = v
                goodMoves = [move]
            elif v == goodValue:
                goodMoves.append(move)
            totalValue = totalValue + v
            count = count + c
        return totalValue, goodMoves, count

    def _evaluteValue(self, pieces):
        if Neu.Board.isWon(pieces, self._playerColor):
            return self.VALUE_WON
        if Neu.Board.isWon(pieces, self._enemyColor):
            return self.VALUE_LOSE
        return self.VALUE_CONTINUE
