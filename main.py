from game import Game
from textView import TextView
from visualView import VisualView
from vector import Vector

game = Game()
view = VisualView(game)

game.hardDrop()
game.assimilateIntoStack()
game.hardDrop()
game.assimilateIntoStack()
game.hardDrop()
game.assimilateIntoStack()
game.dropBy1()
game.dropBy1()
game.dropBy1()
game.dropBy1()

while not view.hasQuit():
    view.show()