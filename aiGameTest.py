import unittest
from game import *
from aiGame import HighLevelAIGame
from tetrimino import *


class TestHighLevelGame(unittest.TestCase):
    def testGenerateInputs(self):
        game = HighLevelAIGame(Game())
        # empties are necessary bc of DAS
        # there are some extraneous ones though
        self.assertEqual([[RCW], [HARD], []], game.generateInputs((0, 1)))
        self.assertEqual([[LEFT], [], [HARD], []], game.generateInputs((-1, 0)))
        self.assertEqual([[RCW], [LEFT], [], [HARD], []], game.generateInputs((-1, 1)))
        self.assertEqual([[RCW], [], [RCW], [RIGHT], [], [RIGHT], [], [RIGHT], [], [HARD], []],
                         game.generateInputs((3, 2)))
        self.assertEqual([[RCCW], [LEFT], [], [LEFT], [], [HARD], []], game.generateInputs((-2, 3)))
        self.assertEqual([[HARD], []], game.generateInputs((0, 0)))

    def testHardAfterMove(self):
        """Whole game is just O pieces.
        Put one all the way to the left and another in the middle.
        Since (0,0) is just a hard drop, this won't shift or rotate.
        Regression test since there was a bug where if you hard drop, release
        and wait for spawn, and then hard drop right when it spawns, it thought you
        never released it.
        """
        game = HighLevelAIGame(Game())
        game.game.bag = [Tetrimino(O) for _ in range(500)]
        game.game.currentTetrimino = Tetrimino(O)
        game = game.move((-4, 0))
        self.assertEqual([O, O, None, None, None, None, None, None, None, None],
                         game.game.grid[0])
        game = game.move((0, 0))
        self.assertEqual([O, O, None, None, O, O, None, None, None, None],
                         game.game.grid[0])
        print(game.game.grid)

    def testTetrisOfLines(self):
        """
        the bag is a bunch of I (line) pieces.
        put them all down vertically going from left to right.
        The 10th one will trigger a tetris.
        """
        game = HighLevelAIGame(Game())
        game.game.bag = [Tetrimino(I) for _ in range(500)]
        game.game.currentTetrimino = Tetrimino(I)
        self.assertEqual(0, game.game.totalLinesCleared)
        for x in range(-4, 6):
            game = game.move((x, 3))
        self.assertEqual(4, game.game.totalLinesCleared)


