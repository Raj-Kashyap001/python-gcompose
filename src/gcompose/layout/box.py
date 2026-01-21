import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk
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

@contextmanager  
def HeaderBar(as_type=Row, spacing=8, styles=None):
    if as_type not in (Row, Column):
        raise ValueError("as_type must be Row or Column")
    
    # Create the box first (but don't push it yet)
    box = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL if as_type == Column else Gtk.Orientation.HORIZONTAL,
        spacing=spacing
    )
    apply_styles(box, styles)
    
    # Create window handle and set box as its child
    handle = Gtk.WindowHandle()
    handle.set_child(box)
    
    # Add handle to current parent and push box to stack
    parent = Composition.current()
    parent.append(handle)
    Composition._stack.append(box)
    
    yield box
    
    Composition._stack.pop()