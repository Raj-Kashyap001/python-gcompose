import gi
gi.require_version("Gtk", "4.0")

from gi.repository import Gtk
from ..compose.runtime import Composition
from ..compose.runtime import Composable
from ..styling.css import apply_styles

@Composable
def Text(value, styles=None):
    label = Gtk.Label(label=str(value), xalign=0)
    apply_styles(label, styles)
    Composition.current().append(label)
    return label


@Composable
def Button(label, on_click=None, styles=None):
    btn = Gtk.Button(label=label)
    if on_click:
        btn.connect("clicked", lambda *_: on_click())
    apply_styles(btn, styles)
    Composition.current().append(btn)
    return btn
