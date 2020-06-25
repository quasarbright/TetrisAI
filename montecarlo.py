import math
import random
from aiGame import AIGame
# mean + c * sqrt(ln(t) / n) ??

_debug = False
def debug(*args, **kwargs):
    if _debug:
        print(*args, **kwargs)

class Node:
    c = .001

    def __init__(self, state: AIGame, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action # what action was used to get here
        self.children = []
        self.untriedActions = state.getLegalActions()[:]
        random.shuffle(self.untriedActions)
        self.numSimulations = 0
        self.totalScore = 0
        self.maxValue = self.state.score()
        self.visited = False
    
    def isExpanded(self):
        # return len(self.children) > 0 and all(child.visited for child in self.children)
        return len(self.untriedActions) == 0

    def mean(self):
        return self.totalScore / max(1,self.numSimulations)

    def uct(self, child):
        # print(child.maxValue, Node.c * math.sqrt(math.log(self.numSimulations) / child.numSimulations))
        return child.maxValue + Node.c * math.sqrt(math.log(self.numSimulations) / child.numSimulations)
    
    def traverse(self):
        node = self
        while node.isExpanded() and not node.state.isDead():
            node = max(node.children, key=self.uct)
        if node.state.isDead():
            # print('term')
            return node
        else:
            # unvisited = tuple(filter(lambda child: not child.visited, node.children))
            # return random.choice(unvisited)
            return node.expand()
    
    def maxDepth(self):
        if len(self.children) == 0:
            return 1
        else:
            return 1 + max(child.maxDepth() for child in self.children)
    
    def size(self):
        if len(self.children) == 0:
            return 1
        else:
            return 1 + sum(child.size() for child in self.children)

    def expand(self):
        # if len(self.children) == 0:
        #     state = self.state
        #     actions = state.getAllMoves()
        #     self.children = [Node(state.move(action), self, action) for action in actions]
        # else:
        #     pass
        if len(self.untriedActions) > 0:
            action = self.untriedActions.pop()
            child = Node(self.state.move(action), self, action)
            self.children.append(child)
            return child
        else:
            print("tried to expand expanded node")
            pass

    def rolloutPolicy(self, state):
        actions = state.getLegalActions()
        state = state.move(random.choice(actions))
        return state
        # action = minimax.chooseAction(state, 0)
        # return state.move(action)

    
    def rollout(self):
        # maybe make all, not just legal
        self.visited = True
        state = self.state
        return state.score()
        while not state.isDead():
            state = self.rolloutPolicy(state)
        return state.score()
    
    def backProp(self, result):
        node = self
        while True:
            node.numSimulations += 1
            node.totalScore += result
            if node.parent is None:
                break
            else:
                node.parent.maxValue = max(node.parent.maxValue, self.maxValue)
                node = node.parent

    def chooseChild(self):
        return max(self.children, key=lambda child: child.numSimulations)

    def chooseAction(self):
        bestChild = self.chooseChild()
        return bestChild.action
    
    def iterate(self, n=1):
        for _ in range(n):
            debug(f"size = {self.size()} before")
            debug(f"depth = {self.maxDepth()} before")
            leaf = self.traverse()
            score = leaf.rollout()
            leaf.backProp(score)
            debug(f"size = {self.size()} after")
            debug(f"depth = {self.maxDepth()} after")
    
    def __str__(self):
        def indent(s: str):
            lines = s.splitlines()
            return '\n'.join('    '+line for line in lines)
        if len(self.children) > 0:
            return f"({self.totalScore:.4f}, {self.numSimulations})\n" + indent('\n'.join(str(child) for child in self.children))
        else:
            return f"({self.totalScore:.4f}, {self.numSimulations})"
    
    def __repr__(self):
        return f"({self.totalScore:.4f}, {self.numSimulations})"

lastGame, lastNode = None, None
def getRoot(game):
    if game == lastGame:
        debug('s')
        root = lastNode
        root.parent = None
        root.action = None
        return root
    else:
        return Node(game)

def monteCarloTreeSearch(game, numIterations):
    global lastGame, lastNode
    root = getRoot(game)
    root.iterate(numIterations)
    print(root.maxDepth(), root.size(), root.size() / 4**root.maxDepth())
    for child in root.children[:1]:
        print(child.maxValue, Node.c * math.sqrt(math.log(root.numSimulations) / child.numSimulations))
    bestChild = root.chooseChild()
    lastGame, lastNode = bestChild.state, bestChild
    return bestChild.action

def chooseAction(game, maxDepth):
    return monteCarloTreeSearch(game, maxDepth)
