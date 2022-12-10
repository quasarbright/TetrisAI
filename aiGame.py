from game import *
import tetrimino

'''
heuristics are from https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
'''
# no hold
actions = [HOLD, RCW, RCCW, LEFT, RIGHT, SOFT, HARD]

class AIGame:
    def __init__(self, game: Game = None):
        if game is not None:
            self.game = game
        else:
            self.game = Game()
        self.lines = self.game.totalLinesCleared
        self.prevLines = self.lines

    def copy(self):
        ans = AIGame(self.game.copy())
        ans.lines = self.lines
        ans.prevLines = self.prevLines
        return ans

    def getLegalActions(self):
        return actions + [None]

    def move(self, action):
        ans = self.copy()
        oldLines = self.lines
        ans.game.aiUpdate([action])
        ans.prevLines = ans.lines
        ans.lines = ans.game.totalLinesCleared
        return ans

    def isDead(self):
        return self.game.dead

    def score(self):
        return self.game.score
    
    def heuristicScore(self):
        gridT = [[None for y in range(self.game.lastVisibleRow+1)] for x in range(self.game.width)]
        for x in range(self.game.width):
            for y in range(self.game.lastVisibleRow+1):
                gridT[x][y] = self.game.grid[y][x]
        
        # aggregate height
        def height(col):
            indices = (i for i in range(self.game.lastVisibleRow+1))
            activeIndices = filter(lambda row: gridT[col][row] is not None, indices)
            return max(activeIndices,default=0)
        heights = tuple(height(col) for col in range(self.game.width))
        aggregateHeight = sum(heights)

        # porosity
        def isHole(x, y):
            if y <= self.game.lastVisibleRow-1:
                return gridT[x][y] is None and gridT[x][y+1] is not None
            else:
                return False
        
        holes = 0
        for x in range(self.game.width):
            for y in range(self.game.lastVisibleRow+1):
                if isHole(x,y):
                    holes += 1
        
        # bumpiness
        bumpiness = 0
        for h1, h2 in zip(heights,heights[1:]):
            bumpiness += abs(h1-h2)
        
        # lines just cleared
        clears = self.lines - self.prevLines
        
        a = -0.510066
        b = 0.760666
        c = -0.35663
        d = -0.184483
        return a * aggregateHeight + b * clears + c * holes + d * bumpiness

    def __eq__(self, other):
        return isinstance(other, AIGame) and self.game == other.game

    def __hash__(self):
        return hash(self.game)


class HighLevelAIGame(AIGame):
    '''Instead of doing individual inputs, a move is a (position, rotation) pair
    where doing the move hard drops a piece at that x position with that rotation
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def copy(self):
        ans = HighLevelAIGame(self.game.copy())
        ans.lines = self.lines
        ans.prevLines = self.prevLines
        return ans
    
    def getLegalActions(self):
        positions = tuple(range(-5, 6))
        rotations = tuple(range(4))
        ans = [(p, r) for p in positions for r in rotations]
        # for heuristic agents, putting a piece down is almost always worse than holding,
        # so they'll just stall
        # if self.game.canHold and self.game.canMove():
        #     ans.append(HOLD)
        return ans
    
    def move(self, action):
        assert action in self.getLegalActions()
        ans = self.copy()
        game = ans.game
        for inputsHeld in self.generateInputs(action):
            game.update(inputsHeld)
        while game.spawnRequired:
            # wait for new tetrimino to spawn
            # TODO if you move this before the updates, it breaks main minimax for some reason. Why?
            # I think it has something to do with the fact that the AI controller does its own version of this method.
            game.update([])
        ans.prevLines = ans.lines
        ans.lines = game.totalLinesCleared
        return ans
    
    def generateInputs(self, action):
        """Generate the low-level inputs for the high level action.
        Returns a list of input combination lists, where each sublist is the list of inputs for a single frame
        """
        assert action in self.getLegalActions()
        if action == HOLD:
            return [[HOLD]]
        ans = self.copy()
        game = ans.game
        inputs = []
        shifts = []
        rotations = []
        while not ans.game.canMove():
            game.update()
            inputs.append([])
        position, rotation = action
        if rotation == 1:
            rotations.append([RCW])
        elif rotation == 2:
            rotations.append([RCW])
            rotations.append([])
            rotations.append([RCW])
        elif rotation == 3:
            rotations.append([RCCW])

        if position < 0:
            for _ in range(-position):
                shifts.append([LEFT])
                shifts.append([])
        elif position > 0:
            for _ in range(position):
                shifts.append([RIGHT])
                shifts.append([])

        # for some reason, it seems like this caused there to be no RCW rotations. Couldn't figure out why
        # this is only important in extremely high gravity anyway though
        # rotShifts = []        
        # for (rotation, shift) in zip(rotations, shifts):
        #     rotations.pop(0)
        #     shifts.pop(0)
        #     rotShifts.append(rotation + shift)
        
        # inputs += rotShifts
        
        inputs += rotations
        inputs += shifts

        inputs.append([HARD])
        # this is necessary because we can't do anything right after a hard drop?
        # also, if we're doing consecutive (0,0), we'd end up holding hard and it'd only do 1
        inputs.append([])
        return inputs
