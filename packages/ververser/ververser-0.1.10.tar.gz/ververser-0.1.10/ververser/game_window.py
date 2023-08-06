import logging
from pathlib import Path
from time import time, sleep
from typing import Optional

import pyglet

from ververser.content_manager import ContentManager, LoadStatus
from ververser.fps_counter import FPSCounter
from ververser.main_script import MainScript


logger = logging.getLogger(__name__)


class GameWindow( pyglet.window.Window ):

    def __init__( self, asset_folder_path : Path, throttle_fps = 30 ):
        super().__init__(vsync = False)

        self.throttle_fps = throttle_fps
        self.frame_count = 0
        self.last_update = time()
        self.fps_counter = FPSCounter()

        self.alive = True
        self.is_paused = False
        self.requires_init = True

        self.has_init_problem = False
        self.has_content_problem = False

        self.asset_manager = ContentManager( asset_folder_path )
        self.main_script : Optional[ MainScript ] = None

    # ================ State affectors ================

    def on_close(self):
        self.alive = False

    def quit( self ):
        self.alive = False

    def restart( self ):
        self.requires_init = True

    # ================ Run game loop ================

    def run(self):
        while self.alive:
            # dispatch all OS events
            self.dispatch_events()

            # if there was a problem with initialisation and no script was modified yet,
            # then there is no need to retry initialisation
            is_any_script_updated = self.asset_manager.is_any_script_updated()
            if self.has_init_problem and not is_any_script_updated:
                continue

            # if any script files are updated we require reinitialisation
            if is_any_script_updated:
                self.requires_init = True

            # try to initialise the game
            # if a problem is encountered, then end the frame early
            if self.requires_init:
                self._init()
                if self.has_init_problem:
                    continue

            # by now we know our scripts are properly initialised

            # Now that scripts have been handled,
            # we will try to reload assets (which is done only if they have been modified)
            reload_status = self.asset_manager.try_reload_assets()
            if reload_status == LoadStatus.FAILED :
                logger.info( "Error occured during asset loading. Game is now paused!" )
                self.has_content_problem = True
                continue
            else :
                if reload_status == LoadStatus.RELOADED :
                    self.has_content_problem = False

            if self.is_paused or self.has_content_problem:
                continue

            # by this point we have accepted the game should just continue running normally
            # during update and draw we might still encounter problems
            # we do not know necessarily if those are caused by scripts or assets,
            # so we just call them content problems

            now = time()
            dt = now - self.last_update
            self.last_update = now

            if self.throttle_fps:
                sleep_time = ( 1 / self.throttle_fps ) - dt
                sleep( max( sleep_time, 0 ) )

            # TODO:
            # we do not want the framerate to affect physics
            # easiest way to do that is fix the dt here for now
            dt = 1/60

            self._update(dt)
            self.update(dt)

            self._draw_start()
            self.draw()
            self._draw_end()

    # ---------------- Functions that wrap standard game hooks  ----------------

    def _init( self ):
        init_success = self.init()
        if not init_success:
            self.has_init_problem = True
        else:
            self.has_init_problem = False
            self.requires_init = False
            self.has_content_problem = False

    def _update( self, dt ):
        self.fps_counter.update()

    def _draw_start( self ):
        self.clear()

    def _draw_end( self ):
        self.fps_counter.draw()
        self.flip()
        self.frame_count += 1

    # ---------------- Convenience Functions ----------------
    def try_invoke( self, f ):
        try :
            f()
        except Exception as e:
            logger.exception( f'Error occurred during script invokation. Game is now paused! Exception: {e}' )
            self.has_content_problem = True

    # ================ End of standard boilerplate ================
    # ================ Overload the methods below! ================

    def init( self ) -> bool:
        self.asset_manager.script_watcher.clear()
        self.main_script = self.asset_manager.load_main_script( self )
        return self.main_script is not None

    def update( self, dt ):
        self.try_invoke( lambda : self.main_script.vvs_update( dt ) )

    def draw( self ):
        self.try_invoke( lambda : self.main_script.vvs_draw() )