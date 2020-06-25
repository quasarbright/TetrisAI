import sys
import random
from game import Game
from textView import TextView
from visualView import VisualView
from playableController import PlayableController
from aiController import AIController
import montecarlo
from vector import Vector

# controller = PlayableController(Game, VisualView)
# controller.go()


fuel = 10
if len(sys.argv) > 1:
    fuel = int(sys.argv[1])

def choose(game):
    return montecarlo.chooseAction(game, fuel)


controller = AIController(Game, VisualView, choose)
controller.go()