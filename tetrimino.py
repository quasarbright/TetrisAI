import numpy as np
from vector import Vector
I = "I"
J = "J"
L = "L"
Z = "Z"
S = "S"
T = "T"
O = "O"
types = [I, J, L, Z, S, T, O]
typeToColor = {
    I: (21, 194, 188),  # cyan
    J: (53, 75, 219),  # blue
    L: (217, 156, 33),  # orange
    Z: (217, 33, 33),  # red
    S: (61, 217, 33),  # green
    T: (146, 33, 217),  # purple
    O: (217, 211, 33)  # yellow
}

class Tetrimino:
    def __init__(self, pieceType, index=None, rotations=None, kicks=None):
        self.pieceType = pieceType
        self.color = typeToColor[pieceType]
        # rotation state. either 0, 1, 2, or 3
        # increasing index = CW rotation
        self.index = 0 if index is None else index
        # the boundings box for each rotation state
        if rotations is None:
            if pieceType == I:
                base = np.array([
                    [0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                ])
            elif pieceType == J:
                base = np.array([
                    [1, 0, 0],
                    [1, 1, 1],
                    [0, 0, 0]
                ])
            elif pieceType == L:
                base = np.array([
                    [0, 0, 1],
                    [1, 1, 1],
                    [0, 0, 0]
                ])
            elif pieceType == Z:
                base = np.array([
                    [1,1,0],
                    [0,1,1],
                    [0,0,0]
                ])
            elif pieceType == S:
                base = np.array([
                    [0,1,1],
                    [1,1,0],
                    [0,0,0]
                ])
            elif pieceType == T:
                base = np.array([
                    [0,1,0],
                    [1,1,1],
                    [0,0,0]
                ])
            elif pieceType == O:
                base = np.array([
                    [0,1,1,0],
                    [0,1,1,0],
                    [0,0,0,0],
                ])
            else:
                raise ValueError(f"unknown type: {pieceType}")
            if pieceType == O:
                self.rotations = [base, base, base, base]
            else:
                self.rotations = [
                    base,
                    np.rot90(base, 3),
                    np.rot90(base, 2),
                    np.rot90(base, 1)
                ]
        else:
            self.rotations = rotations
        
        # when a piece rotates, if it is obstructed, the game should try to
        # translate the piece by these kicks and see if it unobstructs them
        # which kicks to try depends on the rotation
        if kicks is None:
            self.kicks = {}
            if pieceType in [J, L, S, T, Z]:
                self.kicks[(1, 0)] = [(0, 0),( 1, 0),( 1,-1),(0, 2),( 1, 2)]
                self.kicks[(1, 2)] = [(0, 0),( 1, 0),( 1,-1),(0, 2),( 1, 2)]
                self.kicks[(2, 1)] = [(0, 0),(-1, 0),(-1, 1),(0,-2),(-1,-2)]
                self.kicks[(2, 3)] = [(0, 0),( 1, 0),( 1, 1),(0,-2),( 1,-2)]
                self.kicks[(3, 2)] = [(0, 0),(-1, 0),(-1,-1),(0, 2),(-1, 2)]
                self.kicks[(3, 0)] = [(0, 0),(-1, 0),(-1,-1),(0, 2),(-1, 2)]
                self.kicks[(0, 3)] = [(0, 0),( 1, 0),( 1, 1),(0,-2),( 1,-2)]
            elif pieceType == I:
                self.kicks[(0, 1)] = [(0, 0),(-2, 0),( 1, 0),(-2,-1),( 1, 2)]
                self.kicks[(1, 0)] = [(0, 0),( 2, 0),(-1, 0),( 2, 1),(-1,-2)]
                self.kicks[(1, 2)] = [(0, 0),(-1, 0),( 2, 0),(-1, 2),( 2,-1)]
                self.kicks[(2, 1)] = [(0, 0),( 1, 0),(-2, 0),( 1,-2),(-2, 1)]
                self.kicks[(2, 3)] = [(0, 0),( 2, 0),(-1, 0),( 2, 1),(-1,-2)]
                self.kicks[(3, 2)] = [(0, 0),(-2, 0),( 1, 0),(-2,-1),( 1, 2)]
                self.kicks[(3, 0)] = [(0, 0),( 1, 0),(-2, 0),( 1,-2),(-2, 1)]
                self.kicks[(0, 3)] = [(0, 0),(-1, 0),( 2, 0),(-1, 2),( 2,-1)]
            for key in self.kicks:
                self.kicks[key] = [Vector(x,y) for (x,y) in self.kicks[key]]
        else:
            self.kicks = kicks
    

    def copy(self):
        return Tetrimino(self.pieceType, self.index, self.rotations, self.kicks)

    def getKicks(self, old, new):
        if (old, new) in self.kicks:
            return self.kicks[(old, new)]
        else:
            return []

    def rotateCW(self):
        oldInd = self.index
        self.index += 1
        self.index %= 4
        return self.getKicks(oldInd, self.index)

    def rotateCCW(self):
        oldInd = self.index
        self.index -= 1
        self.index %= 4
        return self.getKicks(oldInd, self.index)
    
    def getState(self):
        return self.rotations[self.index]
    
    def getActivePositions(self):
        '''should precompute
        '''
        state = self.getState()
        ans = []
        for y in range(len(state)):
            for x in range(len(state[0])):
                if state[y][x] == 1:
                    ans.append(Vector(x,y))
        return ans
    
    def reset(self):
        self.index = 0
    
    def getColor(self):
        return typeToColor[self.pieceType]
    
    def __eq__(self, other):
        if isinstance(other, Tetrimino):
            sameState = self.getState() == other.getState()
            if isinstance(sameState, np.ndarray):
                return sameState.all()
            else:
                return sameState
        else:
            return False
        
    def __hash__(self):
        return hash(tuple(self.getState().flatten()))

prototypes = {t : Tetrimino(t) for t in types}

def makeTetrimino(pieceType):
    return prototypes[pieceType].copy()
