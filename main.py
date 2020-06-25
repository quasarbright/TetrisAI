import sys
import random
from game import Game
from textView import TextView
from visualView import VisualView
from playableController import PlayableController
from aiController import *
import montecarlo
import minimax
from vector import Vector
from aiGame import *
import torch
import train

# controller = PlayableController(Game, VisualView)
# controller.go()


fuel = 1
if len(sys.argv) > 1:
    fuel = int(sys.argv[1])

# def choose(game):
#     return montecarlo.chooseAction(game, fuel)

# actor = train.trainActor(num_epochs=100)
# actions = train.actions

# def choose(game):
#     state = game.toTensor()
#     action_logprob, action_index = actor.choose_action(state)
#     print(action_logprob, action_index)
#     action = actions[action_index]
#     return action

# controller = AIController(Game, VisualView, choose)
# controller.go()

# game = AIGame(Game())
# print(game.toTensor())
# print(game.toTensor().size())

def choose(game):
    # position = int(input("position:"))
    # rotation = int(input("rotation:"))
    # return (position, rotation)

    return minimax.chooseAction(game, fuel)

controller = HighLevelController(Game, VisualView, choose)
controller.go()
