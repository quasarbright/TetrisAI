from game import Game
from textView import TextView
from vector import Vector

game = Game()
view = TextView(game)

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

view.print()


view.print()