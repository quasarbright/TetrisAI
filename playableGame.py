import pygame
from game import *
from tetrimino import *

pygame.init()

game = Game()
game.hardDrop()
game.assimilateIntoStack()
game.hardDrop()
game.assimilateIntoStack()
game.hardDrop()
game.assimilateIntoStack()
game.dropBy1()
game.dropBy1()
game.dropBy1()
game.moveRight()

size = width, height = 800,800
pad = 40

k = (height - 2*pad)
playRect = pygame.Rect(width/2 - k/4, pad, k/2, k)

pieceSize = playRect.width / 10

holdRect = pygame.Rect(pad, pad, playRect.x - 2 * pad, playRect.x - 2 * pad)

nextRect = pygame.Rect(playRect.right + pad, pad, holdRect.width, holdRect.height * 3)


screen = pygame.display.set_mode(size)

def gridToPx(x, y):
    x = playRect.x + pieceSize * x
    # y = 0 means bottom side is at bottom
    y = playRect.bottom - (y+1) * pieceSize
    return x, y

def drawPieceAt(pieceType, x, y, ghost=False):
    '''x, y in grid coords
    '''
    x,y = gridToPx(x,y)
    r,g,b = typeToColor[pieceType]
    color = pygame.Color(r,g,b)
    if ghost:
        color.a = 100
    rect = pygame.Rect(x,y,pieceSize,pieceSize)
    surface = pygame.Surface((rect.width, rect.height))
    surface.fill(color)
    surface.set_alpha(color.a)
    screen.blit(surface, (rect.x, rect.y))
    # pygame.draw.rect(screen, color, rect)
    


bgColor = (30, 30, 30)
panelColor = (12, 12, 12)

while True:
    if any(event.type == pygame.QUIT for event in pygame.event.get()):
        pygame.quit()
        break
    
    screen.fill(bgColor)
    pygame.draw.rect(screen, panelColor, playRect)
    pygame.draw.rect(screen, panelColor, holdRect)
    pygame.draw.rect(screen, panelColor, nextRect)

    for y in range(game.lastVisibleRow):
        for x in range(game.width):
            piece = game.getPieceAt(x, y)
            if piece is not None:
                drawPieceAt(piece, x, y)
    
    for p in game.getTetriminoActivePositions(p=game.getGhostPosition()):
        piece = game.currentTetrimino.pieceType
        if p.y <= game.lastVisibleRow:
            drawPieceAt(piece, p.x, p.y, ghost=True)

    for p in game.getTetriminoActivePositions():
        piece = game.currentTetrimino.pieceType
        if p.y <= game.lastVisibleRow:
            drawPieceAt(piece, p.x, p.y)

    pygame.display.flip()
