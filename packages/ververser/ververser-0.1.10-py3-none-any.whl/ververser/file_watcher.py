import os.path
from pathlib import Path


class FileWatcher:

    def __init__( self, file_path: Path, record_now = True ):
        self.file_path = file_path
        if record_now:
            self.last_seen_time_modified = self.get_last_time_modified()
        else:
            self.last_seen_time_modified = 0

    def get_last_time_modified( self ) -> float:
        return os.path.getmtime( self.file_path )

    def is_file_updated( self ) -> bool:
        last_time_modified = self.get_last_time_modified()
        is_updated = False
        if last_time_modified != self.last_seen_time_modified:
            is_updated = True
            self.last_seen_time_modified = last_time_modified
            print(f'File was updated! - {self.file_path} - Timestamp: {self.last_seen_time_modified}')
        return is_updated
