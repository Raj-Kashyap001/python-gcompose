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
        Gdk.Display.get_default(),
        _provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


def apply_styles(widget, styles_string):
    """
    Apply Tailwind-like classes safely.
    Parses out programmatic properties (width, height, justify, align) and applies them via GTK methods.
    Unknown classes are ignored by GTK.
    """
    if not styles_string:
        print("DEBUG: No styles to apply")
        return

    print(f"DEBUG: Applying styles to widget: '{styles_string}'")

    # Parse programmatic properties
    parsed_props, css_classes = StyleParser.parse_all_properties(styles_string)

    # Apply programmatic properties
    if parsed_props:
        print(f"DEBUG: Applying programmatic properties: {parsed_props}")
        apply_size_properties(widget, parsed_props)
        apply_alignment_properties(widget, parsed_props)
    else:
        print("DEBUG: No programmatic properties found")

    # Apply remaining CSS classes
    if css_classes:
        print(f"DEBUG: Applying CSS classes: '{css_classes}'")
        for cls in css_classes.split():
            widget.add_css_class(cls)
    else:
        print("DEBUG: No CSS classes to apply")
