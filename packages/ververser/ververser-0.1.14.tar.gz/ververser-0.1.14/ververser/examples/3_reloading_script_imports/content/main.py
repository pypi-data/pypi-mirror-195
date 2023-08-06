from typing import Optional
from ververser import GameWindow, import_script

game = import_script( 'game.py' )
Game = game.Game


# --------
# This is just some boilerplate that makes it easier to use a custom Game class

_GAME : Optional[ Game ] = None

def vvs_init( game_window : GameWindow ):
    global _GAME
    _GAME = Game( game_window )

def vvs_update( dt ):
    _GAME.update( dt )

def vvs_draw():
    _GAME.draw()