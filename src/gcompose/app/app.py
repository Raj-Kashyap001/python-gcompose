import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gio
from pathlib import Path

class ComposeApp(Adw.Application):
    def __init__(self, ui_fn, app_id="com.example.gcompose", title="Gcompose Application", icon=None, width=800, height=600, frameless=False):
        # Note: x and y removed as arguments because GTK4 cannot use them
        super().__init__(application_id=app_id)
        self.ui_fn = ui_fn
        self.app_title = title # Renamed to avoid conflict with Gtk.Application.title property if it existed
        self.app_icon = icon
        self.default_width = width
        self.default_height = height
        self.frameless = frameless

    def do_activate(self):
        # 1️⃣ Load CSS (Wrapped in try/except for safety)
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

        # 2️⃣ Create window
        win = Adw.ApplicationWindow(application=self)
        win.set_default_size(self.default_width, self.default_height)
        win.set_title(self.app_title)

        if self.app_icon:
            win.set_icon_name(self.app_icon)

        # 3️⃣ Header Bar / Frameless Logic
        if self.frameless:
            # Removes window border/decorations entirely
            win.set_decorated(False)
        else:
            # Create the default Adwaita Header Bar
            header_bar = Adw.HeaderBar()
            
            # Note: set_show_title_buttons defaults to True, but we keep it explicit if you want.
            # In Adwaita, the header bar automatically creates the space for buttons.
            header_bar.set_show_end_title_buttons(True)
            
            # Use the header bar as the titlebar
            # win.set_titlebar(header_bar)  # Not supported for AdwApplicationWindow

        # 4️⃣ Content Area
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # 'set_content' is specific to Adw.ApplicationWindow (replaces set_child)
        win.set_content(root)

        # 5️⃣ Mount UI
        # We assume this import exists in your project structure
        try:
            from .renderer import mount
            mount(root, self.ui_fn, app=self, win=win, frameless=self.frameless)
        except ImportError:
            # Fallback if renderer is missing (for testing this snippet)
            lbl = Gtk.Label(label="Renderer not found. UI mounted here.")
            root.append(lbl)

        win.present()

        # REMOVED: win.move(self.x, self.y)
        # GTK4 does not support moving windows programmatically. 
        # The window manager (OS) decides placement.