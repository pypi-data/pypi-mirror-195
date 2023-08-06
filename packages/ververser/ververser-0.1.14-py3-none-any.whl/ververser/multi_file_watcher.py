from pathlib import Path
from typing import Optional
from ververser.file_watcher import FileWatcher


class MultiFileWatcher:

    def __init__( self, name : str = "<not set>" ):
        self.name = name
        self.file_watchers : list[ FileWatcher ] = []
        self.last_seen_time_modified : float = 0

    def clear( self ) -> None:
        self.file_watchers = []

    def add_file_watch( self, file_path : Path ) -> None:
        new_file_watcher = FileWatcher( file_path )
        self.file_watchers.append( new_file_watcher )
        self.last_seen_time_modified = max( self.last_seen_time_modified, new_file_watcher.get_last_time_modified() )

    def get_last_time_modified( self ) -> float:
        if not self.file_watchers:
            return 0
        all_modification_times = [ file_watcher.get_last_time_modified() for file_watcher in self.file_watchers ]
        modification_time = max( all_modification_times )
        return modification_time

    def is_any_file_modified( self ) -> bool:
        last_time_modified = self.get_last_time_modified()
        is_updated = False
        if last_time_modified != self.last_seen_time_modified:
            is_updated = True
            self.last_seen_time_modified = last_time_modified
            print( f'MultiFileWatcher with name "{self.name}" was updated - Timestamp: {self.last_seen_time_modified}' )
        return is_updated
