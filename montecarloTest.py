from montecarlo import *
import unittest
from unittest.mock import Mock


class MCTSTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rolloutPolicy = Mock()
        self.mcts = MCTS(self.rolloutPolicy)
        self.game = AIGame()
