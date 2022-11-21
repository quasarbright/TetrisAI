import pygame
from pygame.time import Clock
from visualView import VisualView, drawGame, size, playMusic
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
                while game.spawnRequired:
                    # skip waiting for piece to spawn, makes it look faster
                    game.update([])
                # for inputsHeld in HighLevelAIGame(game).generateInputs(self.actionChooser(HighLevelAIGame(game))):
                #     # 1 frame = 1 move
                #     game.update(inputsHeld)
                inputsHeld = []
                if len(inputQueue) == 0:
                    action = self.actionChooser(HighLevelAIGame(game))
                    inputQueue = HighLevelAIGame(game).generateInputs(action)
                if len(inputQueue) > 0:
                    inputsHeld = inputQueue.pop(0)
                game.update(inputsHeld)
            view.show()
            clock.tick_busy_loop(game.frameRate)


class ReplayController:
    """Display a replay of a game. No sound effects, just music."""
    def __init__(self, states, frameRate=60):
        """
        :param states: states to replay
        """
        self.states = states
        self.frameRate = frameRate

    def go(self):
        screen = pygame.display.set_mode(size)
        playMusic()
        for state in self.states:
            if any(event.type == pygame.QUIT for event in pygame.event.get()):
                break
            drawGame(state.game, screen)
            clock.tick_busy_loop(self.frameRate)
        # after completing, just show the last state
        while not any(event.type == pygame.QUIT for event in pygame.event.get()):
            drawGame(state.game, screen)
            clock.tick_busy_loop(self.frameRate)


# if __name__ == "__main__":
#     controller = AIController(Game, VisualView)
#     controller.go()
