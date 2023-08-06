import logging
from pathlib import Path
from runpy import run_path


logger = logging.getLogger(__name__)


def invoke_if_not_none( f, *args, **kwargs ) -> None:
    if f:
        f( *args, **kwargs )


class MainScript:

    def __init__( self, file_path : Path, game_window ):
        self.file_path = file_path
        self.data_module = run_path( str( file_path ) )

        self.f_init = self.data_module.get( 'vvs_init' )
        self.f_update = self.data_module.get( 'vvs_update' )
        self.f_draw = self.data_module.get( 'vvs_draw' )
        self.f_exit = self.data_module.get( 'vvs_exit' )

        self.vvs_init( game_window )

    def vvs_init( self, game_window ):
        invoke_if_not_none( self.f_init, game_window )

    def vvs_update( self, dt ):
        invoke_if_not_none( self.f_update, dt )

    def vvs_draw( self ):
        invoke_if_not_none( self.f_draw )

    def vvs_exit( self ):
        invoke_if_not_none( self.f_exit )


def load_main_script( script_path : Path, game_window ) -> MainScript:
    return MainScript( script_path, game_window )
