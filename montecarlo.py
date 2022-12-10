import random
import math

from aiGame import AIGame
from collections import defaultdict

# monte carlo tree search


class MCTS:
    """Monte-Carlo Tree Search agent"""
    # I am using a class just to keep track of global state, hyper parameters, etc. as fields
    def __init__(self, rolloutPolicy, explorationRate: float = math.sqrt(2), maxRolloutLength: int = math.inf):
        """
        :param rolloutPolicy: function from state to action. used during rollouts
        :param explorationRate: UCT rate of exploration for selection
        :param maxRolloutLength: Maximum number of actions to take in a rollout before termination
        """
        self.rolloutPolicy = rolloutPolicy
        self.explorationRate = explorationRate
        self.maxRolloutLength = maxRolloutLength
        self.reset()

    def reset(self):
        """Reset internal state, like dicts and sets
        """
        # map of state to map of action to how many times the pair has been selected
        self.counts = defaultdict(lambda: defaultdict(int))
        # map of state to map of action to the sum of returns from that pair
        self.totals = defaultdict(lambda: defaultdict(int))
        # set of visited states

    def chooseAction(self, state: AIGame, numIterations: int):
        """Choose the next action to perform.

        :param state: current state
        :param numIterations: how many iterations of MCTS to perform, where 1 iteration involves a selection, expansion,
        simulation, and backup.
        :return: an action, which is a possible member of the result of state.getLegalActions()
        """
        self.reset()
        for _ in range(numIterations):
            pairs, rolloutStartState = self.selectAndExpand(state)
            G = self.rollout(rolloutStartState)
            self.backup(pairs, G)

        actions = state.getLegalActions()
        return max(actions, key=lambda action: self.Q(state, action))

    def selectAndExpand(self, state: AIGame):
        """Search the tree for an unexplored state, starting at the given state.
        """
        pairs = []
        # this is necessary for the first selection since the root state starts out as unvisited
        action = self.selectionPolicy(state)
        pairs.append((state, action))
        state = state.move(action)
        while self.stateVisited(state) and not state.isDead():
            action = self.selectionPolicy(state)
            pairs.append((state, action))
            state = state.move(action)
        return pairs, state

    def stateVisited(self, state: AIGame):
        """Has the state been visited during selection?"""
        return self.countStateVisits(state) > 0

    def selectionPolicy(self, state: AIGame):
        """Select an action using UCT. Use during node selection.

        :return: the action to take during selection
        """
        actions = state.getLegalActions()
        untried = [action for action in actions if not self.stateActionVisited(state, action)]
        if untried:
            return random.choice(untried)
        else:
            actions = list(actions)
            # for random tie breaker
            random.shuffle(actions)
            return max(actions, key=lambda action: self.uct(state, action))

    def stateActionVisited(self, state: AIGame, action) -> bool:
        """Has the state-action pair been visited during selection?"""
        return self.countStateActionVisits(state, action) > 0

    def uct(self, state: AIGame, action) -> float:
        """UCT (Upper Confidence bounds applied to Trees) score for the given state-action pair. Encourages exploration
        """
        N_s = self.countStateVisits(state)
        N_a = self.countStateActionVisits(state, action)
        # TODO this should be + and c needs to be WAY bigger!!!!!
        # i'm leaving it for now for experimental consistency but geez this isn't even uct
        # c needs to be comparable to the returns, so different for score and heuristic
        # TODO you can get rid of the sqrt by returning the square of uct since it'll have the same comparisons
        # looks like it'll save 25%.
        # the repeated N_s is probably worse. That should go too
        return self.Q(state, action) / self.explorationRate * math.sqrt(math.log(N_s) / N_a)

    def countStateVisits(self, state: AIGame) -> int:
        """Computes the number of times a state has been visited in selection"""
        actions = state.getLegalActions()
        return sum([self.countStateActionVisits(state, action) for action in actions])

    def countStateActionVisits(self, state: AIGame, action) -> int:
        """Computes the number of times a state-action pair has been visited in selection"""
        return self.counts[state][action]

    def Q(self, state: AIGame, action) -> float:
        """Value of state-action pair"""
        return self.totalReturnsFromStateAction(state, action) / self.countStateActionVisits(state, action)

    def totalReturnsFromStateAction(self, state: AIGame, action) -> float:
        """Sum of returns from the state-action pair"""
        return self.totals[state][action]

    def rollout(self, state: AIGame) -> float:
        """Finish an episode using the rollout policy and return the return"""
        # The return is just the final score, no discounting
        for _ in range(self.maxRolloutLength):
            if state.isDead():
                break
            action = self.rolloutPolicy(state)
            state = state.move(action)
        return state.score()

    def backup(self, pairs, G):
        """Back-propagate returns to the state-action pairs along the selection path."""
        # no discounting for now
        for state, action in pairs:
            self.totals[state][action] += G
            self.counts[state][action] += 1


class HeuristicEvalMCTS(MCTS):
    """Like ordinary MCTS, but instead of playing rollouts, just evaluate the state using the heuristic score.
    Essentially a more sophisticated heuristic minimax."""
    def __init__(self):
        super().__init__(False)

    # override
    def rollout(self, state: AIGame) -> float:
        """Instead of using a rollout policy, evaluate with the heuristic"""
        return state.heuristicScore()


class ScoreEvalMCTS(MCTS):
    """Like ordinary MCTS, but instead of playing rollouts, just evaluate the state using the in-game score.
    Essentially a more sophisticated naive minimax."""
    def __init__(self):
        super().__init__(False)

    # override
    def rollout(self, state: AIGame) -> float:
        """Instead of using a rollout policy, evaluate with the heuristic"""
        return state.score()


def uniformPolicy(state: AIGame):
    """Randomly select a legal action with uniform probability"""
    return random.choice(state.getLegalActions())


def greedyHeuristicPolicy(state: AIGame):
    """Select the action which leads to the highest immediate heuristic score"""
    # env is technically stochastic, but it's deterministic as far as the heuristic is concerned.
    # the only stochasticity is in the future pieces
    actions = list(state.getLegalActions())
    # random tie breakers
    random.shuffle(actions)
    return max(actions, key=lambda action: state.move(action).heuristicScore())


if __name__ == '__main__':
    from aiGame import HighLevelAIGame
    from game import Game
    from tqdm.auto import trange
    # numTimesteps = 100
    # numIterations = 100
    # state = HighLevelAIGame(Game())
    # mcts = HeuristicEvalMCTS()#MCTS(uniformPolicy, maxRolloutLength=numTimesteps)
    # states = [state.copy()]
    # for t in trange(numTimesteps):
    #     action = mcts.chooseAction(state, numIterations=numIterations)
    #     state = state.move(action)
    #     states.append(state)
    def runLowLevelExperiment(initialState: 'AIGame', chooseAction, numPieces=100, maxNumTimesteps=1000,numGames=10):
        """Run a game with the given policy,
        cut off after numTimesteps time steps.
        Run numGames games.
        Return list of list of states (each game's history)"""
        statess = []
        for game in trange(numGames, desc="games loop"):
            state = initialState.copy()
            states = [state.copy()]
            pieceCount = 0
            bag = state.game.bag[:]
            for t in trange(maxNumTimesteps, desc=f'game {game}'):
                if state.isDead() or pieceCount >= numPieces:
                    break
                action = chooseAction(state)
                state = state.move(action)
                if bag != state.game.bag:
                    # bag change => piece was placed
                    pieceCount += 1
                    bag = state.game.bag[:]
                    states.append(state)
            statess.append(states)
        return statess
    state = AIGame(Game())
    mcts = ScoreEvalMCTS()
    numIterations = 10
    def chooseAction(state):
        return mcts.chooseAction(state, numIterations=numIterations)
    scoreEvalMCTSLowLevelResults = runLowLevelExperiment(state, chooseAction, numGames=1)

