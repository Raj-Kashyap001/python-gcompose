from .runtime import Composition

class WindowState:
    def __init__(self, window):
        self.window = window
        self._maximized = window.is_maximized()
        # Connect to window state events to keep track
        self.window.connect("notify::maximized", self._on_maximized_changed)

    def _on_maximized_changed(self, window, param):
        self._maximized = window.is_maximized()
        Composition.rerender()

    def minimize(self):
        self.window.minimize()

    def toggle_maximize(self):
        if self._maximized:
            self.window.unmaximize()
        else:
            self.window.maximize()

    def is_maximized(self):
        return self._maximized

    def close(self):
        self.window.close()

def get_window_state():
    return WindowState(Composition._window)