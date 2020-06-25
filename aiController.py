import pygame
from pygame.time import Clock
from visualView import VisualView
from game import Game
from aiGame import AIGame
clock = Clock()


class AIController:
    def __init__(self, gameFactory, viewFactory, actionChooser):
        self.gameFactory = gameFactory
        self.viewFactory = viewFactory
        self.actionChooser = actionChooser

    def go(self):
        game: Game = self.gameFactory()
        view: VisualView = self.viewFactory(game)
        view.show()
        while not any(event.type == pygame.QUIT for event in pygame.event.get()):
            inputsHeld = []
            if not game.dead:
                action = self.actionChooser(AIGame(game))
                if action is not None:
                    inputsHeld = [action]
                game.update(inputsHeld)
            view.show()
            clock.tick_busy_loop(game.frameRate)


# if __name__ == "__main__":
#     controller = AIController(Game, VisualView)
#     controller.go()
