print( f'Imported {__file__}' )


from pyglet.gl import glClearColor
from ververser import GameWindow, import_script


module_color_for_time = import_script( 'color_for_time.py', reinit_on_mod = False )


class Game:

    def __init__( self, game_window : GameWindow ):
        self.game_window = game_window
        self.total_time = 0

    def update( self, dt ):
        self.total_time += dt
        color = module_color_for_time.get_color_for_time( self.total_time )
        glClearColor( color[0], color[1], color[2], 1.0 )

    def draw( self ):
        ...

    def exit( self ):
        ...
