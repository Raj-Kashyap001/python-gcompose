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
def Button(
    label,
    on_click=None,
    styles=None,
    icon=None,
    icon_position="start",
    icon_layout="horizontal",
    icon_gap=6,
):
    if icon:
        # Determine orientation
        orientation = (
            Gtk.Orientation.HORIZONTAL
            if icon_layout == "horizontal"
            else Gtk.Orientation.VERTICAL
        )

        # Create box for layout
        box = Gtk.Box(orientation=orientation, spacing=icon_gap)

        # Create label
        lbl = Gtk.Label(label=str(label), xalign=0)

        # Create icon
        if icon.startswith("/") or icon.startswith("./") or icon.startswith("../"):
            # Image file path
            img = Gtk.Image.new_from_file(icon)
        else:
            # Theme icon name
            img = Gtk.Image.new_from_icon_name(icon)

        # Pack based on position
        if icon_position == "start":
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


@Composable
def Image(source, styles=None, width=None, height=None):
    """Image composable that supports file paths or icon names"""
    if source.startswith("/") or source.startswith("./") or source.startswith("../"):
        # File path
        img = Gtk.Image.new_from_file(source)
    else:
        # Icon name
        img = Gtk.Image.new_from_icon_name(source)

    if width and height:
        img.set_size_request(width, height)
    elif width:
        img.set_size_request(width, -1)
    elif height:
        img.set_size_request(-1, height)

    apply_styles(img, styles)
    Composition.current().append(img)
    return img


@Composable
def ProgressBar(fraction=0.0, styles=None, show_text=False, text=None):
    """Progress bar composable"""
    progress = Gtk.ProgressBar()
    progress.set_fraction(fraction)
    if show_text:
        progress.set_show_text(True)
    if text:
        progress.set_text(text)
    apply_styles(progress, styles)
    Composition.current().append(progress)
    return progress


@Composable
def List(items, styles=None, selection_mode="none", on_select=None):
    """List composable that displays a list of items"""
    list_box = Gtk.ListBox()

    # Set selection mode
    if selection_mode == "single":
        list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
    elif selection_mode == "multiple":
        list_box.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
    else:
        list_box.set_selection_mode(Gtk.SelectionMode.NONE)

    # Add items to the list
    for item in items:
        label = Gtk.Label(label=str(item))
        list_box.append(label)

    # Handle selection
    if on_select:

        def on_row_selected(_list_box, row):
            if row:
                index = row.get_index()
                on_select(items[index])

        list_box.connect("row-selected", on_row_selected)

    apply_styles(list_box, styles)
    Composition.current().append(list_box)
    return list_box
