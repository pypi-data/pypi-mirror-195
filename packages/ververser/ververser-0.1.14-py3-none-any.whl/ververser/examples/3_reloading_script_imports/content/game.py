import math
from pyglet.gl import glClearColor
from ververser import GameWindow


class Game:

    def __init__( self, game_window : GameWindow ):
        self.game_window = game_window
        self.total_time = 0

    def update( self, dt ):
        self.total_time += dt
        g = 0.25 + 0.25 * (math.sin( self.total_time ) + 1)
        glClearColor( 0, g, 0, 1.0 )

    def draw( self ):
        ...
