import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio, Gdk, GdkPixbuf
from pathlib import Path
import os
import shutil

class ComposeApp(Adw.Application):
    def __init__(self, ui_fn, app_id="com.example.gcompose", title="Gcompose Application",
                 icon=None, width=800, height=600, frameless=False,
                 bg_color=None, text_color=None, window_icon=None):
        super().__init__(application_id=app_id)
        self.ui_fn = ui_fn
        self.app_title = title
        self.app_icon = icon
        self.default_width = width
        self.default_height = height
        self.frameless = frameless
        self.bg_color = bg_color
        self.text_color = text_color
        self.window_icon = window_icon
    
    def do_activate(self):
        # 1 Load CSS
        try:
            from gcompose.styling.css import load_css
            css_path = (
                Path(__file__)
                .parent.parent / "styling" / "root.css"
            )
            load_css(str(css_path.resolve()))
        except ImportError:
            print("Warning: Could not load CSS module.")
        except Exception as e:
            print(f"Warning: CSS loading failed: {e}")
        
        # 2 Create window
        win = Adw.ApplicationWindow(application=self)
        win.set_default_size(self.default_width, self.default_height)
        win.set_title(self.app_title)

        # TODO: Implement window icon support for GTK 4
        # GTK 4 requires icons to be installed in the icon theme
        # For now, icons are not set
        
        # 3 Create content area
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Apply root theming
        if self.bg_color or self.text_color:
            self._apply_root_theme(root)
        
        # 4 Setup header bar with ToolbarView (THIS IS THE KEY!)
        if not self.frameless:
            # Create header bar
            header_bar = Adw.HeaderBar()
            header_bar.set_show_end_title_buttons(True)  # Show window controls (minimize, maximize, close)
            header_bar.set_show_start_title_buttons(True)  # Show start buttons if needed
            
            # Use ToolbarView to properly integrate header bar with content
            toolbar_view = Adw.ToolbarView()
            toolbar_view.add_top_bar(header_bar)
            toolbar_view.set_content(root)
            
            # Set the toolbar view as window content
            win.set_content(toolbar_view)
        else:
            # Frameless mode
            win.set_decorated(False)
            win.set_content(root)
        
        # 5 Mount UI into root
        try:
            from .renderer import mount
            mount(root, self.ui_fn, app=self, win=win, frameless=self.frameless)
        except ImportError:
            # Fallback for testing
            lbl = Gtk.Label(label="Renderer not found. UI mounted here.")
            root.append(lbl)
        
        win.present()

    def _apply_root_theme(self, root):
        """Apply background and text color theming to the root container."""
        css_parts = []
        if self.bg_color:
            css_parts.append(f"background-color: {self.bg_color};")
        if self.text_color:
            css_parts.append(f"color: {self.text_color};")

        if css_parts:
            css = f".app-root {{ {' '.join(css_parts)} }}"
            provider = Gtk.CssProvider()
            provider.load_from_string(css)

            # Add CSS class to root
            root.add_css_class("app-root")

            # Apply the provider
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_USER
            )
