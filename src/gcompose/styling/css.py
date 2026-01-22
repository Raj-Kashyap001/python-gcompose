import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gdk
from .parser import StyleParser, apply_size_properties, apply_alignment_properties

_provider = None


def load_css(path):
    """
    Load CSS file once into GTK.
    """
    global _provider
    if _provider:
        return

    _provider = Gtk.CssProvider()
    _provider.load_from_path(path)

    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(), _provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


def _setup_hover_effects(widget, hover_classes):
    """Setup hover event handlers for widgets to add/remove CSS classes.

    Args:
        widget: GTK widget to apply hover effects to
        hover_classes: List of CSS class names to apply on hover
    """
    if not hover_classes:
        return

    # Create motion controller for mouse enter/leave events
    motion_ctrl = Gtk.EventControllerMotion()

    def on_enter(_controller, *args):
        for cls in hover_classes:
            widget.add_css_class(cls)

    def on_leave(_controller, *args):
        for cls in hover_classes:
            widget.remove_css_class(cls)

    motion_ctrl.connect("enter", on_enter)
    motion_ctrl.connect("leave", on_leave)
    widget.add_controller(motion_ctrl)


def apply_styles(widget, styles_string):
    """
    Apply Tailwind-like classes safely.
    Parses out programmatic properties (width, height, justify, align, hover) and applies them via GTK methods.
    Unknown classes are ignored by GTK.

    Hover format: hover:class-name adds class-name on mouse enter
    """
    if not styles_string:
        # print("DEBUG: No styles to apply")
        return

    # Parse programmatic properties
    parsed_props, css_classes = StyleParser.parse_all_properties(styles_string)

    # Apply programmatic properties
    if parsed_props:
        apply_size_properties(widget, parsed_props)
        apply_alignment_properties(widget, parsed_props)

        # Apply hover effects if present
        if "hover" in parsed_props:
            _setup_hover_effects(widget, parsed_props["hover"])
    else:
        pass
        # print("DEBUG: No programmatic properties found")

    # Apply remaining CSS classes
    if css_classes:
        # print(f"DEBUG: Applying CSS classes: '{css_classes}'")
        for cls in css_classes.split():
            widget.add_css_class(cls)
    else:
        pass
        # print("DEBUG: No CSS classes to apply")
