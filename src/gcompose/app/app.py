import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, Gio
from pathlib import Path

class ComposeApp(Adw.Application):
    def __init__(self, ui_fn, app_id="com.example.gcompose", title="Gcompose Application", 
                 icon=None, width=800, height=600, frameless=False):
        super().__init__(application_id=app_id)
        self.ui_fn = ui_fn
        self.app_title = title
        self.app_icon = icon
        self.default_width = width
        self.default_height = height
        self.frameless = frameless
    
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
        
        if self.app_icon:
            win.set_icon_name(self.app_icon)
        
        # 3 Create content area
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
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