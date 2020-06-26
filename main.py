import argparse
from game import Game


parser = argparse.ArgumentParser(description="Guideline-compliant marathon Tetris. Play it yourself or watch an AI play.")
group = parser.add_mutually_exclusive_group()
group.add_argument("--minimax", help="watch the minimax game AI play with given search depth (1 recommended)", metavar="depth", type=int)
group.add_argument("--manual", help="play the game yourself. left and right to move, down to soft drop, space to hard drop, z and x to rotate, and shift to hold", action="store_true")

args = parser.parse_args()

if args.minimax:
    from aiController import *
    import minimax
    from aiGame import *

    fuel = args.minimax

    def choose(game):
        return minimax.chooseAction(game, fuel)

    controller = HighLevelController(Game, VisualView, choose)
    controller.go()

elif args.manual:
    from visualView import VisualView
    from playableController import PlayableController
    controller = PlayableController(Game, VisualView)
    controller.go()

else:
    parser.print_help()
