import pygame
from pygame.time import Clock
from visualView import VisualView
from game import Game
from aiGame import AIGame, HighLevelAIGame
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

class HighLevelController(AIController):
    '''controller specially designed for a high level ai game
    which has actions represented as (positin, rotation) pairs, rather than low-level inputs for each frame
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def go(self):
        game: Game = self.gameFactory()
        view: VisualView = self.viewFactory(game)
        view.show()
        inputQueue = []
        while not any(event.type == pygame.QUIT for event in pygame.event.get()):
            if not game.dead:
                inputsHeld = []
                if len(inputQueue) == 0:
                    action = self.actionChooser(HighLevelAIGame(game))
                    # print(action)
                    inputQueue = HighLevelAIGame(game).generateInputs(action)
                if len(inputQueue) > 0:
                    inputsHeld = inputQueue.pop(0)
                game.update(inputsHeld)
            view.show()
            clock.tick_busy_loop(game.frameRate)

# if __name__ == "__main__":
#     controller = AIController(Game, VisualView)
#     controller.go()
