import pygame
from pygame.time import Clock
from visualView import VisualView
from game import Game, LEFT, RIGHT, HARD, SOFT, RCCW, RCW, HOLD
clock = Clock()
keymap = {
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_SPACE: HARD,
    pygame.K_DOWN: SOFT,
    pygame.K_z: RCCW,
    pygame.K_x: RCW,
    pygame.K_LSHIFT: HOLD,
}
class PlayableController:
    def __init__(self, gameFactory, viewFactory):
        self.gameFactory = gameFactory
        self.viewFactory = viewFactory
    
    def go(self):
        game : Game = self.gameFactory()
        view : VisualView = self.viewFactory(game)
        view.show()
        def shouldLoop():
            ans = not game.dead
            ans = ans and not any(event.type == pygame.QUIT for event in pygame.event.get())
            return ans
        while shouldLoop():
            inputsHeld = set() # dups are ok
            keys = pygame.key.get_pressed()
            for key in keymap:
                if keys[key]:
                    inputsHeld.add(keymap[key])
            game.update(inputsHeld)
            view.show()
            clock.tick_busy_loop(game.frameRate)

if __name__ == "__main__":
    controller = PlayableController(Game, VisualView)
    controller.go()