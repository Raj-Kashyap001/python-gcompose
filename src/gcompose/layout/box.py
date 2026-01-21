import gi
gi.require_version("Gtk", "4.0")

from gi.repository import Gtk
from contextlib import contextmanager
from ..compose.runtime import Composition

from ..styling.css import apply_styles

@contextmanager
def Column(spacing=8, styles=None):
    box = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL,
        spacing=spacing
    )
    apply_styles(box, styles)
    Composition.push(box)
    yield box
    Composition.pop()


@contextmanager
def Row(spacing=8, styles=None):
    box = Gtk.Box(
        orientation=Gtk.Orientation.HORIZONTAL,
        spacing=spacing
    )
    apply_styles(box, styles)
    Composition.push(box)
    yield box
    Composition.pop()
