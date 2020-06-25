from game import *

class AIGame:
    def __init__(self, game : Game):
        self.game = game

    def copy(self):
        return AIGame(self.game.copy())

    def getLegalActions(self):
        return actions + [None]

    def move(self, action):
        if action is None:
            return self.copy()
        else:
            ans = self.copy()
            ans.game.update([action])
            return ans

    def isDead(self):
        return self.game.dead

    def score(self):
        return self.game.score * self.game.frameRate / (self.game.frameCount+1) / 50000

    def __eq__(self, other):
        return isinstance(other, AIGame) and self.game == other.game

    def __hash__(self):
        return hash(self.game)