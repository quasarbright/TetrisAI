import random
from game import HOLD
def chooseAction(game, maxDepth=10):
    # memo shouldn't be global because there can only possibly be a duplicate state 
    # within a single call of chooseAction since the keys are (game, depth) pairs
    memo = {}
    def value(game, depth):
        if (game, depth) in memo:
            # print("sssdfsdf")
            return memo[(game, depth)]
        actions = game.getLegalActions()
        if depth <= 0 or len(actions) == 0 or game.isDead():
            ans = game.heuristicScore()
            memo[(game, depth)] = ans
            return ans
        else:
            newGames = [game.move(action) for action in actions]
            ans = max([value(game, depth-1) for game in newGames])
            memo[(game, depth)] = ans
            return ans
    def valueOfAction(action):
        newGame = game.move(action)
        return value(newGame, maxDepth)
    actions = game.getLegalActions()
    random.shuffle(actions)
    return max(actions, key=valueOfAction)


if __name__ == '__main__':
    from aiGame import HighLevelAIGame
    from game import Game
    from aiController import ReplayController
    numTimesteps = 10
    numIterations = 100
    state = HighLevelAIGame(Game())
    states = [state.copy()]
    for t in range(numTimesteps):
        print(t)
        action = chooseAction(state, maxDepth=0)
        print(action)
        state = state.move(action)
        states.append(state)
    print(len(states), "states")
    ReplayController(states, frameRate=1).go()
