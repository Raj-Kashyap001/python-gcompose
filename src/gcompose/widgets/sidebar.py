import gi

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from gi.repository import Adw, Gtk
from contextlib import contextmanager
from ..compose.runtime import Composition
from ..styling.css import apply_styles


@contextmanager
def SidebarLayout(styles=None, min_sidebar_width=200, max_sidebar_width=300):
    split_view = Adw.NavigationSplitView()
    split_view.set_min_sidebar_width(min_sidebar_width)
    split_view.set_max_sidebar_width(max_sidebar_width)
    apply_styles(split_view, styles)
    # Append to current (root)
    Composition.current().append(split_view)

    # Add toggle button to header bar if available
    window = Composition._window
    if window:
        content = window.get_content()
        if hasattr(content, "get_top_bar"):  # ToolbarView
            header_bar = content.get_top_bar()
            if header_bar:
                # Create toggle button
                toggle_button = Gtk.ToggleButton()
                toggle_button.set_icon_name("sidebar-show-symbolic")
                toggle_button.set_tooltip_text("Toggle Sidebar")
                toggle_button.set_active(True)
                toggle_button.connect(
                    "toggled", lambda btn: split_view.set_show_sidebar(btn.get_active())
                )
                header_bar.pack_start(toggle_button)

    # Temporarily push to stack so that child context managers can access it as current
    Composition._stack.append(split_view)
    try:
        yield split_view
    finally:
        Composition._stack.pop()


@contextmanager
def SidebarContent(styles=None):
    # Get the parent split view
    parent = Composition.current()
    if not isinstance(parent, Adw.NavigationSplitView):
        raise ValueError("SidebarContent must be used inside SidebarLayout")

    # Create a scrolled window for the sidebar content
    scrolled = Gtk.ScrolledWindow()
    scrolled.add_css_class("navigation-sidebar")  # GNOME styling
    scrolled.set_policy(
        Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC
    )  # No horizontal scroll
    apply_styles(scrolled, styles)

    # Create a box for the content
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    scrolled.set_child(box)

    # Create navigation page
    page = Adw.NavigationPage(child=scrolled, title="Menu", tag="sidebar")
    parent.set_sidebar(page)

    # Push the box to the composition stack (NOT append)
    Composition._stack.append(box)  # Use _stack.append instead of push

    yield box

    Composition._stack.pop()  # Use _stack.pop instead of pop


@contextmanager
def SidebarMainScreen(styles=None):
    # Get the parent split view
    parent = Composition.current()
    if not isinstance(parent, Adw.NavigationSplitView):
        raise ValueError("SidebarMainScreen must be used inside SidebarLayout")

    # Create a scrolled window for the main content
    scrolled = Gtk.ScrolledWindow()
    scrolled.set_policy(
        Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC
    )  # No horizontal scroll
    apply_styles(scrolled, styles)

    # Create a box for the content
    box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
    scrolled.set_child(box)

    # Create navigation page
    page = Adw.NavigationPage(child=scrolled, title="Home", tag="content")
    parent.set_content(page)

    # Push the box to the composition stack (NOT append)
    Composition._stack.append(box)  # Use _stack.append instead of push

    yield box

    Composition._stack.pop()  # Use _stack.pop instead of pop
