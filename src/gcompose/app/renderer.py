from ..compose.runtime import Composition


def _clear(container):
    child = container.get_first_child()
    while child:
        container.remove(child)
        child = container.get_first_child()


def mount(root, render_fn, app=None, win=None, frameless=False):
    """
    Mount root composable and render UI.
    v1: full redraw on every state change.
    """
    Composition.set_root(root)
    Composition.set_app(app)
    Composition.set_window(win)

    def render():
        _clear(root)
        Composition._stack = [root]
        Composition.reset_hooks()
        render_fn()
        Composition._stack.pop()
        Composition.end_render()

    Composition._render = render
    render()
