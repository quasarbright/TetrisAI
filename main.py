import sys
import random
from game import Game
from textView import TextView
from visualView import VisualView
from playableController import PlayableController
from aiController import AIController
import montecarlo
from vector import Vector
from aiGame import AIGame
import torch
import train

# controller = PlayableController(Game, VisualView)
# controller.go()


# fuel = 10
# if len(sys.argv) > 1:
#     fuel = int(sys.argv[1])

# def choose(game):
#     return montecarlo.chooseAction(game, fuel)

actor = train.trainActor(num_epochs=100)
actions = train.actions

def choose(game):
    state = game.toTensor()
    action_logprob, action_index = actor.choose_action(state)
    print(action_logprob, action_index)
    action = actions[action_index]
    return action

controller = AIController(Game, VisualView, choose)
controller.go()

# game = AIGame(Game())
# print(game.toTensor())
# print(game.toTensor().size())

    