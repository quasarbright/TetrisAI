import pygame
from game import *
from tetrimino import *


pygame.init()

size = width, height = 1000,800
pad = 80
font = pygame.font.SysFont(pygame.font.get_default_font(), 40)

k = (height - 2*pad)
playRect = pygame.Rect(width/2 - k/4, pad, k/2, k)

pieceSize = playRect.width / 10

holdRect = pygame.Rect(pad, pad, playRect.x - 2 * pad, playRect.x - 2 * pad)

nextRect = pygame.Rect(playRect.right + pad, pad, holdRect.width, holdRect.height * 3)


# screen = pygame.display.set_mode(size)


def gridToPx(x, y):
    x = playRect.x + pieceSize * x
    # y = 0 means bottom side is at bottom
    y = playRect.bottom - (y+1) * pieceSize
    return x, y

def drawTetriminoInRect(rect, tetrimino, screen):
    '''assumes tetrimino in default position
    '''
    state = tetrimino.getState()
    state = state[:-1]
    w = len(state[0])
    h = len(state)
    surface = pygame.Surface((pieceSize*w,pieceSize*(h)))
    surface.fill(panelColor)
    color = pygame.Color(*typeToColor[tetrimino.pieceType])
    for row in range(h):
        for col in range(w):
            if state[row, col] == 1:
                x, y = [n*pieceSize for n in (col,row)]
                r = pygame.Rect(x, y, pieceSize, pieceSize)
                drawRect(r, color, surface)
    x = rect.centerx - surface.get_rect().width/2
    y = rect.centery - surface.get_rect().height/2
    screen.blit(surface, (x, y))



def drawRect(rect, color, screen):
    surface = pygame.Surface((rect.width, rect.height))
    surface.fill(color)
    surface.set_alpha(color.a)
    screen.blit(surface, (rect.x, rect.y))

def drawPieceOnGrid(pieceType, x, y, screen, ghost=False):
    '''x, y in grid coords
    '''
    x,y = gridToPx(x,y)
    r,g,b = typeToColor[pieceType]
    color = pygame.Color(r,g,b)
    if ghost:
        color.a = 100
    rect = pygame.Rect(x,y,pieceSize,pieceSize)
    drawRect(rect, color, screen)
    # pygame.draw.rect(screen, color, rect)
    


bgColor = (30, 30, 30)
panelColor = (12, 12, 12)

def drawGame(game, screen):
    screen.fill(bgColor)
    pygame.draw.rect(screen, panelColor, playRect)
    pygame.draw.rect(screen, panelColor, holdRect)
    pygame.draw.rect(screen, panelColor, nextRect)

    for y in range(game.lastVisibleRow):
        for x in range(game.width):
            piece = game.getPieceAt(x, y)
            if piece is not None:
                drawPieceOnGrid(piece, x, y, screen)

    for p in game.getTetriminoActivePositions(p=game.getGhostPosition()):
        piece = game.currentTetrimino.pieceType
        if p.y <= game.lastVisibleRow:
            drawPieceOnGrid(piece, p.x, p.y, screen, ghost=True)

    for p in game.getTetriminoActivePositions():
        piece = game.currentTetrimino.pieceType
        if p.y <= game.lastVisibleRow:
            drawPieceOnGrid(piece, p.x, p.y, screen)

    if game.holdTetrimino is not None:
        drawTetriminoInRect(holdRect, game.holdTetrimino, screen)

    for (i, tetrimino) in enumerate(game.getUpcomingTetriminos()):
        y = nextRect.y + i * nextRect.width
        rect = pygame.Rect(nextRect.x, y, nextRect.width, nextRect.width)
        drawTetriminoInRect(rect, tetrimino, screen)

    score = font.render(f"score: {game.score}", True, (255, 255, 255))
    score_rect = score.get_rect()
    score_rect.centerx = holdRect.centerx
    score_rect.y = holdRect.bottom + pad
    screen.blit(score, score_rect)

    level = font.render(f"level: {game.level}", True, (255, 255, 255))
    level_rect = level.get_rect()
    level_rect.centerx = score_rect.centerx
    level_rect.y = score_rect.bottom + pad
    screen.blit(level, level_rect)

    pygame.display.flip()

class VisualView:
    def __init__(self, game):
        self.game = game
        self.screen = None

    def show(self):
        if self.screen is None:
            self.screen = pygame.display.set_mode(size)
        drawGame(self.game, self.screen)
    
    def hide(self):
        self.screen = None
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.hardDrop()
    game.assimilateIntoStack()
    game.hardDrop()
    game.assimilateIntoStack()
    game.hardDrop()
    game.assimilateIntoStack()
    game.hold()
    game.dropBy1()
    game.dropBy1()
    game.dropBy1()
    game.moveRight()

    view = VisualView(game)
    while True:
        if any(event.type == pygame.QUIT for event in pygame.event.get()):
            pygame.quit()
            break

        view.show()
