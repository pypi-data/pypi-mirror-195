import logging
from pathlib import Path
from runpy import run_path


logger = logging.getLogger(__name__)


class MainScript:

    def __init__( self, file_path : Path, game_window ):
        self.file_path = file_path
        self.data_module = run_path( str( file_path ) )

        self.vvs_init( game_window )

    def vvs_init( self, game_window ):
        f_init = self.data_module.get( 'vvs_init' )
        if f_init :
            f_init( game_window )

    def vvs_update( self, dt ):
        f_update = self.data_module.get( 'vvs_update' )
        if f_update :
            f_update( dt )

    def vvs_draw( self ):
        f_draw = self.data_module.get( 'vvs_draw' )
        if f_draw:
            f_draw()


def load_main_script( script_path : Path, game_window ) -> MainScript:
    main_script = None
    try :
        main_script = MainScript( script_path, game_window )
    except Exception as e :
        logger.exception( f'Encountered an error during loading of main script "{script_path}". Exception: {e}' )
    return main_script
