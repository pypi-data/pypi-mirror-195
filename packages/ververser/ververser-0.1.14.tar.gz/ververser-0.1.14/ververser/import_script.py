from ververser.global_game_window import get_global_game_window
from ververser.script import Script


def import_script( script_path : str ) -> Script:
    return get_global_game_window().asset_manager.load( script_path )
