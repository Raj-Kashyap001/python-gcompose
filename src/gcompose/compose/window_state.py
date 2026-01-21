from .runtime import Composition

class WindowState:
    def __init__(self, window):
        self.window = window

    def minimize(self):
        self.window.minimize()

    def toggle_maximize(self):
        if self.window.is_maximized():
            self.window.unmaximize()
        else:
            self.window.maximize()

    def is_maximized(self):
        return self.window.is_maximized()

    def close(self):
        self.window.close()

def get_window_state():
    return WindowState(Composition._window)