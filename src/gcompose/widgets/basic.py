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
def Button(label, on_click=None, styles=None, icon=None, icon_position='start', icon_layout='horizontal', icon_gap=6):
    if icon:
        # Determine orientation
        orientation = Gtk.Orientation.HORIZONTAL if icon_layout == 'horizontal' else Gtk.Orientation.VERTICAL

        # Create box for layout
        box = Gtk.Box(orientation=orientation, spacing=icon_gap)

        # Create label
        lbl = Gtk.Label(label=str(label), xalign=0)

        # Create icon
        if icon.startswith('/') or icon.startswith('./') or icon.startswith('../'):
            # Image file path
            img = Gtk.Image.new_from_file(icon)
        else:
            # Theme icon name
            img = Gtk.Image.new_from_icon_name(icon)

        # Pack based on position
        if icon_position == 'start':
            box.append(img)
            box.append(lbl)
        else:
            box.append(lbl)
            box.append(img)

        # Create button with box as child
        btn = Gtk.Button()
        btn.set_child(box)
    else:
        # No icon, simple button
        btn = Gtk.Button(label=label)

    if on_click:
        btn.connect("clicked", lambda *_: on_click())
    apply_styles(btn, styles)
    Composition.current().append(btn)
    return btn
