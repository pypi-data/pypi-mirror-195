# Transforms janky 'internals' into easy to work with tool
import os
import typing

from py4web import DAL as P4WDAL

from .debugbar import DummyDebugBar, DebugBar
from .env import is_debug
from .internals import patch_py4


class DebugTools:
    # by default, it is not enabled! This is so you can still import it on production,
    # but don't actually show any debug info. enable(on_off) can be called with e.g. an ENV variable
    enabled = False
    db: P4WDAL
    debug_bar = DummyDebugBar()
    IS_DEBUG: bool = is_debug()

    def enable(
        self,
        # general settings:
        db: P4WDAL,
        enabled: bool | None = None,  # OVERWRITES errorpage_enabled and debugbar_enabled
        set_env_var: bool = True,

        # error screen settings:
        errorpage_enabled: bool = None,  # value of 'enabled' is used by default
        errorpage_renderer: typing.Callable = None,

        # debugbar settings:
        debugbar_enabled: bool = None,  # value of 'enabled' is used by default
        debugbar_fancy_rendering: bool = True,
        debugbar_style: typing.Literal["bootstrap"] = "bootstrap",
        debugbar_slow_threshold_ms: int = 10,
    ):
        """
        By default, on_off looks at PY4WEB_DEBUG_MODE in the env

        @todo: debugbar style (bootstrap/default, bulma, ...)
        """
        if enabled is None:
            enabled = is_debug()

        self.db = db
        self.enabled = enabled

        self.IS_DEBUG = enabled
        if enabled:
            if errorpage_enabled in (True, None):
                patch_py4(errorpage_renderer)

            if debugbar_enabled in (True, None):
                self.debug_bar = DebugBar(db, debugbar_fancy_rendering, debugbar_style, debugbar_slow_threshold_ms)

            if set_env_var:
                # will change the result of is_debug (hopefully)
                os.environ["PY4WEB_DEBUG_MODE"] = "1"
        else:
            self.debug_bar = DummyDebugBar()


tools = DebugTools()

