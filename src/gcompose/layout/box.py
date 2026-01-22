import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk
from contextlib import contextmanager
from ..compose.runtime import Composition
from ..styling.css import apply_styles


@contextmanager
def Column(spacing=8, styles=None):
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=spacing)
    apply_styles(box, styles)
    Composition.push(box)
    yield box
    Composition.pop()


@contextmanager
def Row(spacing=8, styles=None):
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=spacing)
    apply_styles(box, styles)
    Composition.push(box)
    yield box
    Composition.pop()


@contextmanager
def ScrollColumn(spacing=8, styles=None):
    """Scrollable vertical container - auto-scrolls when content exceeds viewport.

    Use this for lists, forms, or any vertically-stacked content that might overflow.
    Scrollbars appear automatically when needed (web-like behavior).

    Args:
        spacing: Space between children
        styles: CSS classes

    Example:
        with ScrollColumn():
            for i in range(100):
                Text(f"Item {i}")
    """
    # Inner box for content
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=spacing)

    # Padding wrapper (applies padding inline to scrollable area)
    padding_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    apply_styles(padding_box, styles)
    padding_box.append(box)
    padding_box.set_vexpand(True)
    padding_box.set_hexpand(True)

    # Wrap in ScrolledWindow
    scrolled = Gtk.ScrolledWindow()
    scrolled.set_child(padding_box)
    scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
    scrolled.set_vexpand(True)
    scrolled.set_hexpand(True)

    # Add to parent
    parent = Composition.current()
    parent.append(scrolled)

    # Push box for children
    Composition.push(box)
    yield box
    Composition.pop()


@contextmanager
def ScrollRow(spacing=8, styles=None):
    """Scrollable horizontal container - auto-scrolls when content exceeds viewport.

    Use this for horizontal lists or tab-like layouts that might overflow.
    Scrollbars appear automatically when needed (web-like behavior).

    Args:
        spacing: Space between children
        styles: CSS classes

    Example:
        with ScrollRow():
            for i in range(50):
                Button(f"Tab {i}")
    """
    # Inner box for content
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=spacing)

    # Padding wrapper (applies padding inline to scrollable area)
    padding_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
    apply_styles(padding_box, styles)
    padding_box.append(box)
    padding_box.set_vexpand(True)
    padding_box.set_hexpand(True)

    # Wrap in ScrolledWindow
    scrolled = Gtk.ScrolledWindow()
    scrolled.set_child(padding_box)
    scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
    scrolled.set_vexpand(True)
    scrolled.set_hexpand(True)

    # Add to parent
    parent = Composition.current()
    parent.append(scrolled)

    # Push box for children
    Composition.push(box)
    yield box
    Composition.pop()


@contextmanager
def HeaderBar(as_type=Row, spacing=8, styles=None):
    if as_type not in (Row, Column):
        raise ValueError("as_type must be Row or Column")

    # Create the box first (but don't push it yet)
    box = Gtk.Box(
        orientation=(
            Gtk.Orientation.VERTICAL
            if as_type == Column
            else Gtk.Orientation.HORIZONTAL
        ),
        spacing=spacing,
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
