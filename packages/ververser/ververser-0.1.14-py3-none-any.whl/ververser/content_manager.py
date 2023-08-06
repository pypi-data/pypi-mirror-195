from pathlib import Path
from typing import Any, Callable

from ververser.reloading_asset import ReloadingAsset, LoadStatus
from ververser.main_script import load_main_script, MainScript
from ververser.multi_file_watcher import MultiFileWatcher
from ververser.script import load_script, Script


ScriptType = MainScript | Script
ContentType = ScriptType | ReloadingAsset

AssetLoaderType = Callable[ [ Path ], Any ]

EXPECTED_SCRIPT_EXTENSION = '.py'
EXPECTED_MAIN_SCRIPT_NAME = Path( 'main.py' )


def is_script_path( path : Path ) -> bool:
    return path.suffix == EXPECTED_SCRIPT_EXTENSION


class ContentManager:

    """
    The asset manager works mainly on two categories of content:
    1) scripts
        When a single script is updated we will not try to do anything clever.
        We basically reinitialize the entire game to make sure all scripts are reloaded.
        In future versions of ververser we can always make this more intelligent.
        The game window is responsible for checking if it needs to reinitialize.
    2) non-scripts
        Non scripts can be anything, i.e. Meshes, Shader or Textures
        Reloading these, does not require reloading the entire game,
        We will just replace them while we keep running.

    Because scripts are dealt with separately,
    we will make a hard distinction between these two categories,
    and refer to non-script content as "assets".
    """

    def __init__( self, content_folder_path : Path ):
        self.content_folder_path = content_folder_path
        self.script_watcher = MultiFileWatcher( 'Script Watcher' )

        self.asset_loaders : list[ tuple[ str, AssetLoaderType ] ] = []
        self.reloading_assets : list[ ReloadingAsset ] = []

        self.register_asset_loader( '.py', load_script )
        self.script_watcher.add_file_watch( self.make_content_path_complete( EXPECTED_MAIN_SCRIPT_NAME ) )

    # ======== Generic functions ========

    def make_content_path_complete( self, asset_path : Path ) -> Path:
        return self.content_folder_path / asset_path

    def exists( self, asset_path ) -> bool:
        complete_asset_path = self.make_content_path_complete( asset_path )
        return complete_asset_path.is_file()

    def load( self, content_path ) -> ContentType:
        absolute_content_path = self.make_content_path_complete( content_path.strip() )
        if not self.exists( absolute_content_path ):
            raise ValueError( f'Content file does not exist. File path: "{absolute_content_path}"' )
        if is_script_path( absolute_content_path ):
            return self._load_script( absolute_content_path )
        else:
            return self._load_asset( absolute_content_path )

    # ======== Script related functions ========

    def is_any_script_updated( self ) -> bool:
        return self.script_watcher.is_any_file_modified()

    def load_main_script( self, game_window ) -> MainScript:
        absolute_script_path = self.make_content_path_complete( EXPECTED_MAIN_SCRIPT_NAME )
        assert self.exists( absolute_script_path ), f'Could not load asset. File path: "{EXPECTED_MAIN_SCRIPT_NAME}"'
        main_script = load_main_script( absolute_script_path, game_window )
        self.script_watcher.add_file_watch( absolute_script_path )
        return main_script

    def _load_script( self, absolute_script_path : Path ) -> Script:
        self.script_watcher.add_file_watch( absolute_script_path )
        return load_script( absolute_script_path )

    # ======== Asset related functions ========

    def _load_asset( self, absolute_asset_path ) -> ReloadingAsset :
        asset_loader = self.get_asset_loader_for_file( absolute_asset_path )
        reloading_asset = ReloadingAsset(
            f_load_asset = asset_loader,
            file_path = absolute_asset_path
        )
        self.reloading_assets.append( reloading_asset )
        return reloading_asset

    def is_any_asset_updated( self ) -> bool:
        for reloading_asset in self.reloading_assets:
            if reloading_asset.is_modified():
                return True
        return False

    def try_reload_assets( self ) -> LoadStatus:
        overall_load_status = LoadStatus.NOT_CHANGED
        for reloading_asset in self.reloading_assets:
            if not reloading_asset.is_modified():
                continue
            reload_status = reloading_asset.reload()
            if reload_status == LoadStatus.RELOADED:
                overall_load_status = LoadStatus.RELOADED
            if reload_status == LoadStatus.FAILED:
                return LoadStatus.FAILED
        return overall_load_status

    def register_asset_loader( self, postfix : str, f_load_asset : AssetLoaderType ) -> None:
        self.asset_loaders.append( ( postfix, f_load_asset ) )

    def get_asset_loader_for_file( self, file_path : Path ) -> AssetLoaderType:
        # reverse search through all registered loaders
        # this way. newest registered loaders overrule older ones
        for postfix, asset_loader in reversed( self.asset_loaders ):
            if str( file_path ).endswith( postfix ):
                return asset_loader
        raise KeyError( f'No asset loader found for file_path: "{file_path}". Known loaders: {self.asset_loaders}' )




