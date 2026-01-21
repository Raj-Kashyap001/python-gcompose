import gi
gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gdk

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
    Unknown classes are ignored by GTK.
    """
    if not styles_string:
        return

    for cls in styles_string.split():
        widget.add_css_class(cls)
