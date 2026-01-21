from functools import wraps

class Composition:
    _root = None
    _stack = []
    _render = None
    _hook_index = 0
    _hooks = []
    _rendering = False
    _app = None
    _window = None

    @classmethod
    def set_root(cls, root):
        cls._root = root

    @classmethod
    def set_app(cls, app):
        cls._app = app

    @classmethod
    def set_window(cls, window):
        cls._window = window

    @classmethod
    def rerender(cls):
        if cls._render:
            cls._render()

    @classmethod
    def current(cls):
        return cls._stack[-1]

    @classmethod
    def push(cls, widget):
        cls.current().append(widget)
        cls._stack.append(widget)

    @classmethod
    def pop(cls):
        cls._stack.pop()

    @classmethod
    def reset_hooks(cls):
        cls._hook_index = 0
        cls._rendering = True

    @classmethod
    def end_render(cls):
        cls._rendering = False

    @classmethod
    def next_hook(cls):
        if not cls._rendering:
            raise RuntimeError("use_state must be called within a composable function during rendering")
        if cls._hook_index >= len(cls._hooks):
            cls._hooks.append(None)
        hook = cls._hooks[cls._hook_index]
        cls._hook_index += 1
        return hook

    @classmethod
    def set_hook(cls, hook):
        cls._hooks[cls._hook_index - 1] = hook


def Composable(fn):
    """
    Marks a function as composable.
    v1: semantic only (no runtime behavior).
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper
