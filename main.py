from game import Game
from textView import TextView
from visualView import VisualView
from playableController import PlayableController
from vector import Vector

controller = PlayableController(Game, VisualView)
controller.go()
