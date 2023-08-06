import logging
from pathlib import Path
from ververser import make_global_game_window


if __name__ == '__main__':
    logging.basicConfig( level = logging.INFO )
    game = make_global_game_window( Path( __file__ ).parent / 'content' )
    game.run()
