from tetrimino import *
from vector import Vector
import random

'''
time:
- DAS
    - the delay
    - the rate after the delay
- gravity
- stack lock
- max 1 of each input per frame?
'''

HOLD = "HOLD"
RCW = "RCW"
RCCW = "RCCW"
LEFT = "LEFT"
RIGHT = "RIGHT"
SOFT = "SOFT"
HARD = "HARD"
HOLD = "HOLD"

class Game:
    def __init__(self):
        self.width = 10
        self.height = 40
        self.previewSize = 3 # how many pieces you see in the future
        self.spawnPosition = Vector(3,19)
        self.lastVisibleRow = 19
        # you can't hold right after you held
        # gets refreshed when a piece assimilates into the stack
        self.canHold = True
        self.dead = False
        self.score = 0
        self.level = 1
        self.linesThisLevel = 0
        
        # row zero is bottom
        self.grid = [[None for x in range(self.width)] for y in range(self.height)]
        self.bag = [] # last element is next
        self.holdTetrimino = None # piece in the hold place
        self.updateBag()
        self.currentTetrimino = None
        self.currentPosition = None
        self.spawnTetrimino()

    
    def getUpcomingTetriminos(self):
        return self.bag[-1:(-1-self.previewSize):-1]

    def getGhostPosition(self):
        p = self.currentPosition
        prev = p
        tet = self.currentTetrimino
        while not self.isTetriminoObstructedAt(tet, p):
            prev = p
            p += Vector(0,-1) # don't mutate
        return prev
    
    def getPieceAt(self, x, y=None):
        '''either getPieceAt(Vector)
        or     getPieceAt(int, int)
        '''
        if isinstance(x, Vector):
            p = x
            return self.grid[p.y][p.x]
        else:
            return self.grid[y][x]
    
    def getTetriminoActivePositions(self, tetrimino=None, p=None):
        if tetrimino is None:
            tetrimino = self.currentTetrimino
        if p is None:
            p = self.currentPosition
        h = len(tetrimino.getState()) - 1
        ans = []
        for p_ in tetrimino.getActivePositions():
            p_ = p_.copy()
            p_.y = h - p_.y
            ans.append(p+p_)
        return ans

    # def getColorAt(self, x, y=None):
    #     p = Vector(x,y)
    #     if isinstance(x, Vector):
    #         p = x
    #     piece = self.getPieceAt(x, y)
    #     if self.getPieceAt(p) is not None:
    #         return piece.color
    #     elif any(p_ == p for p_ in self.getTetriminoActivePositions(self.currentTetrimino)):
    #         return self.currentTetrimino.color
    #     else:
    #         return None
        
    def getLinesGoal(self):
        '''the number of lines needed to level up
        '''
        return self.level * 5
    
    def isInBounds(self, p):
        return p.x >= 0 and p.x < self.width and p.y >= 0 and p.y < self.height

    def isBadPosition(self, p):
        return not self.isInBounds(p) or self.getPieceAt(p) is not None
    
    def isTetriminoObstructedAt(self, tetrimino=None, p=None):
        if tetrimino is None:
            tetrimino = self.currentTetrimino
        if p is None:
            p = self.currentPosition
        activePositions = self.getTetriminoActivePositions(tetrimino, p)
        return any(self.isBadPosition(p) for p in activePositions)
    
    def setPieceAt(self, piece, p):
        self.grid[p.y][p.x] = piece

    def updateBag(self):
        if len(self.bag) < 7:
            newTetriminos = [makeTetrimino(pt) for pt in types]
            random.shuffle(newTetriminos)
            self.bag = newTetriminos + self.bag

    def popBag(self):
        '''used to get the next tetrimino.
        mutates bag'''
        ans = self.bag.pop()
        self.updateBag()
        return ans

    def spawnTetrimino(self, tetrimino=None):
        if tetrimino is None:
            tetrimino = self.popBag()
        self.currentTetrimino = tetrimino
        self.currentPosition = self.spawnPosition
        if self.isTetriminoObstructedAt(self.currentTetrimino, self.currentPosition):
            self.dead = True
    
    def clearRows(self):
        clearCount = 0
        for y in range(self.height):
            if all(piece is not None for piece in self.grid[y]):
                del self.grid[y]
                self.grid.append([None for x in range(self.width)])
                clearCount += 1
        return clearCount
    
    def rotateCCW(self):
        self._rotateHelp(False)
    
    def rotateCW(self):
        self._rotateHelp(True)
    
    def _rotateHelp(self, isCw):
        rotated = self.currentTetrimino.copy()
        if isCw:
            kicks = rotated.rotateCW()
        else:
            kicks = rotated.rotateCCW()
        if not self.isTetriminoObstructedAt(rotated, self.currentPosition):
            self.currentTetrimino = rotated
        else:
            for kick in kicks:
                p = self.currentPosition + kick
                if not self.isTetriminoObstructedAt(rotated, p):
                    self.currentTetrimino = rotated
                    self.currentPosition = p
                    break

    def moveLeft(self):
        p = self.currentPosition + Vector(-1,0)
        if not self.isTetriminoObstructedAt(self.currentTetrimino, p):
            self.currentPosition = p

    def moveRight(self):
        p = self.currentPosition + Vector(1, 0)
        if not self.isTetriminoObstructedAt(self.currentTetrimino, p):
            self.currentPosition = p

    def softDrop(self):
        '''need time stuff
        '''
        pass

    def dropBy1(self):
        p = self.currentPosition + Vector(0, -1)
        if not self.isTetriminoObstructedAt(self.currentTetrimino, p):
            self.currentPosition = p

    def hardDrop(self):
        self.currentPosition = self.getGhostPosition()
    
    def assimilateIntoStack(self):
        '''puts the current tetrimino into the stack and
        spawns a new one. also potentially clears lines'''
        t = self.currentTetrimino.pieceType

        if t == T:
            # test for t spin
            # if the piece can't move up, down, left, or right
            directions = [Vector(1, 0), Vector(-1, 0), Vector(0, 1), Vector(0, -1)]
            def cantMoveIn(direction):
                p = self.currentPosition + direction
                return self.isTetriminoObstructedAt(self.currentTetrimino, p)
            if all(cantMoveIn(direction) for direction in directions):
                self.onTSpin()

        for p in self.getTetriminoActivePositions():
            self.setPieceAt(t, p)
        self.spawnTetrimino()
        clears = self.clearRows()
        self.onClears(clears)
        self.canHold = True
    
    def onTSpin(self):
        pass
    
    def onClears(self, clears):
        '''NES scoring, guideline levelling
        '''
        # TODO also award for soft dropping?
        fac = self.level + 1
        if clears == 1:
            dlines = 1
            self.score += 40*fac
        elif clears == 2:
            dlines == 3
            self.score += 100*fac
        elif clears == 3:
            dlines = 5
            self.score += 300*fac
        elif clears == 4:
            # BOOM tetris for joseph
            dlines = 8
            self.score += 1200*fac
        else:
            dlines = 0
        self.linesThisLevel += dlines
        if self.linesThisLevel >= self.getLinesGoal():
            self.level += 1
            self.linesThisLevel = 0


    def hold(self):
        '''if they haven't held since the last drop,
        reset current piece, spawn the hold piece, and hold = current
        '''
        if self.canHold:
            self.currentTetrimino.reset()
            temp = self.currentTetrimino
            self.spawnTetrimino(self.holdTetrimino)
            self.holdTetrimino = temp
            self.canHold = False


    
