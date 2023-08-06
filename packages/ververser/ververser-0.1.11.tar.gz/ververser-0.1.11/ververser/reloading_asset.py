from enum import Enum, auto
import logging
from typing import Any

from ververser.file_watcher import FileWatcher


logger = logging.getLogger(__name__)


class LoadStatus( Enum ):
    NOT_CHANGED = auto()
    RELOADED = auto()
    FAILED = auto()


class ReloadingAsset:

    def __init__(self, f_load_asset, file_path):
        self.f_load_asset = f_load_asset
        self.file_watcher = FileWatcher( file_path, record_now = False )
        self.asset = None
        self.try_reload()

    def __getattr__( self, name : str ) -> Any:
        return getattr( self.asset, name )

    def try_reload( self ) -> None:
        if not self.file_watcher.is_file_updated():
            self.reload_status = LoadStatus.NOT_CHANGED
            return
        asset_path = self.file_watcher.file_path
        try:
            self.asset = self.f_load_asset( asset_path )
        except Exception as e :
            logger.exception( f'Encountered an error during loading of asset from file "{asset_path}". Exception: {e}' )
            self.reload_status = LoadStatus.FAILED
            self.asset = None
            return
        self.reload_status =  LoadStatus.RELOADED
        return

    def get( self ) -> Any:
        return self.asset


