from game import *
from tetrimino import *

class TextView:
    def __init__(self, game):
        self.game = game
    
    def show(self):
        game = self.game
        lines = []
        boardStrs = [["  " for x in range(game.width)] for y in range(game.lastVisibleRow)]

        for x in range(game.width):
            for y in range(game.lastVisibleRow):
                if game.getPieceAt(x, y) is not None:
                    boardStrs[y][x] = "██"
        for p in game.getTetriminoActivePositions(p=game.getGhostPosition()):
            boardStrs[p.y][p.x] = "▒▒"
        for p in game.getTetriminoActivePositions():
            boardStrs[p.y][p.x] = "▓▓"
            
        boardStrs = boardStrs[::-1]
        boardStrs = ["".join(line) for line in boardStrs]
        lines += boardStrs
        
        hold = game.holdTetrimino
        if hold is None:
            lines.append("no hold")
        else:
            lines.append(f"hold: {hold.pieceType}")
        lines.append("next pieces: " + ", ".join(t.pieceType for t in game.getUpcomingTetriminos()))
        # TODO score
        return '\n'.join(lines)
    
    def print(self):
        print(self.show())
                
