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
actions = [HOLD, RCW, RCCW, LEFT, RIGHT, SOFT, HARD, HOLD]

class Game:
    def __init__(self):
        self.width = 10
        self.height = 40
        self.previewSize = 3 # how many pieces you see in the future
        self.spawnPosition = Vector(3,19)
        self.lastVisibleRow = 19
        self.frameRate = 60
        
        ## timing
        self.frameCount = 0

        self.lockDelay = 0.5 * self.frameRate
        self.lockTime = 0 # time spent on ground
        
        self.autoShiftDelay = 16
        self.autoRepeatRate = 6
        self.shiftTime = 0 # how long left or right has been held

        self.autoEntryRate = 10
        self.spawnWaitTime = 0 # how long to wait until spawning the next piece (after locking)

        self.timeSinceDrop = 0

        ## flags and counts
        self.canHold = True
        self.isSoftDropping = False
        self.rotateReleased = True
        self.hardReleased = True
        self.spawnRequired = False
        self.dead = False
        self.score = 0
        self.level = 6
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
        if self.currentTetrimino is None:
            return self.currentPosition
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
        if tetrimino is not None:
            h = len(tetrimino.getState()) - 1
            ans = []
            for p_ in tetrimino.getActivePositions():
                p_ = p_.copy()
                p_.y = h - p_.y
                ans.append(p+p_)
            return ans
        else:
            return []

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
    
    def getGravity(self):
        '''gets the number of frames per drop
        '''
        level = self.level
        seconds = (0.8 - (level-1)*0.0007)**(level-1)
        if self.isSoftDropping:
            vel = 1 / seconds
            vel += 20
            seconds = 1 / vel
        frames = seconds * self.frameRate
        return frames
    
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
    
    def isOnGround(self):
        p = self.currentPosition + Vector(0, -1)
        return self.isTetriminoObstructedAt(p=p)

    
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
        self.canHold = True
    
    def clearRows(self):
        clearCount = 0
        for y in range(self.height-1,-1,-1):
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
                    if isCw:
                        self.onSuccessfulRotateCW()
                    else:
                        self.onSuccessfulRotateCCW()
                    break

    def moveLeft(self):
        p = self.currentPosition + Vector(-1,0)
        if not self.isTetriminoObstructedAt(self.currentTetrimino, p):
            self.currentPosition = p
            self.onSuccessfulMoveLeft()

    def moveRight(self):
        p = self.currentPosition + Vector(1, 0)
        if not self.isTetriminoObstructedAt(self.currentTetrimino, p):
            self.currentPosition = p
            self.onSuccessfulMoveRight()

    def drop(self):
        '''drop according to gravity. only call once per frame since it handles a counter
        '''
        g = self.getGravity()
        if g < 1:
            g = int(1 / g)
            self.dropByN(g)
        else:
            if self.timeSinceDrop > g:
                self.dropBy1()
    
    def dropByN(self, n):
        for _ in range(n):
            self.dropBy1()


    def dropBy1(self):
        p = self.currentPosition + Vector(0, -1)
        if not self.isTetriminoObstructedAt(self.currentTetrimino, p):
            self.currentPosition = p
            self.timeSinceDrop = 0

    def hardDrop(self):
        self.currentPosition = self.getGhostPosition()
        self.timeSinceDrop = 0
    
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
        clears = self.clearRows()
        self.onClears(clears)
        self.currentTetrimino = None
        self.spawnRequired = True
        self.spawnWaitTime = self.autoEntryRate
    
    def lock(self):
        '''alias for self.assimilateIntoStack
        '''
        self.assimilateIntoStack()
        
    
    def update(self,inputsHeld=[]):
        '''advances the game 1 frame
        inputsHeld should contain values like LEFT, RIGHT, SOFT, RCW etc.
        '''
        left = LEFT in inputsHeld
        right = RIGHT in inputsHeld
        soft = SOFT in inputsHeld
        hard = HARD in inputsHeld
        rcw = RCW in inputsHeld
        rccw = RCCW in inputsHeld
        hold = HOLD in inputsHeld

        if self.spawnRequired:
            if self.spawnWaitTime == 0:
                self.spawnTetrimino()
                self.spawnRequired = False
            else:
                self.spawnWaitTime -= 1
        else:
            # need else bc there is no tetrimino otherwise
            if left == right: # no shift
                self.shiftTime = 0
            
            if not (left and right):
                if self.shiftTime == 0:
                    if left:
                        self.moveLeft()
                        self.shiftTime += 1
                    elif right:
                        self.moveRight()
                        self.shiftTime += 1
                elif self.shiftTime > self.autoShiftDelay:
                    # TODO handle ARR < 1 like gravity
                    timeSinceDelay = self.shiftTime - self.autoShiftDelay
                    if timeSinceDelay % self.autoRepeatRate == 0:
                        if left:
                            self.moveLeft()
                            self.shiftTime += 1
                        elif right:
                            self.moveRight()
                            self.shiftTime += 1

            if rcw and rccw:
                pass
            elif not (rccw or rcw):
                self.rotateReleased = True
            elif rcw and self.rotateReleased:
                self.rotateCW()
                self.rotateReleased = False
            elif rccw and self.rotateReleased:
                self.rotateCCW()
                self.rotateReleased = False

            
            if self.canHold and hold:
                # dw about no piece, we're in the else branch
                self.hold()
            
            if not hard:
                self.hardReleased = True
            elif hard and self.hardReleased:
                self.hardDrop()
                self.hardReleased = False

            self.isSoftDropping = soft
            
            self.timeSinceDrop += 1
            self.drop()

            # maybe do this first
            if self.isOnGround():
                self.lockTime += 1
            if self.lockTime >= self.lockDelay:
                self.lock()
                self.lockTime = 0
        
        self.groundPushRegisteredThisFrame = False
        self.frameCount += 1

    
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
            dlines = 3
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
    

    def onSuccessfulRotateCW(self):
        self.onSuccessfulAnything()

    def onSuccessfulRotateCCW(self):
        self.onSuccessfulAnything()
    
    def onSuccessfulMoveLeft(self):
        self.onSuccessfulAnything()

    def onSuccessfulMoveRight(self):
        self.onSuccessfulAnything()

    def onSuccessfulAnything(self):
        '''successful left, right, cw, or ccw
        '''
        self.lockTime = 0