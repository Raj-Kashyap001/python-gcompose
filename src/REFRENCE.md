Basic Usage
Start by importing and requiring the version:
Pythonimport gi
gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")
from gi.repository import Adw, Gtk, GLib
Initialize the library with Adw.init() (automatically called if using Adw.Application). Create a simple app:
Pythonclass MyApp(Adw.Application):
def **init**(self):
super().**init**(application_id="com.example.MyApp")
GLib.set_application_name("My Adwaita App")

    def do_activate(self):
        window = Adw.ApplicationWindow(application=self)
        window.set_title("Hello Libadwaita")
        window.set_default_size(400, 300)

        # Add a status page as content
        status = Adw.StatusPage()
        status.set_title("Welcome")
        status.set_description("This is a basic libadwaita example.")
        window.set_content(status)

        window.present()

app = MyApp()
app.run()
This creates a window with a status page. Stylesheets load automatically if using resources; add custom CSS via style-dark.css etc., for dark mode support. For full apps, use Adw.StyleManager to handle themes.
Common Widgets
Libadwaita focuses on adaptive components. Examples:

Adw.HeaderBar: Title bar with buttons – header = Adw.HeaderBar(); header.set_show_start_title_buttons(True)
Adw.ActionRow: List row for preferences – row = Adw.ActionRow(title="Option", subtitle="Details")
Adw.Carousel: Paginated scrolling – carousel = Adw.Carousel(); carousel.append(some_widget)
Adw.ToastOverlay: For notifications – overlay = Adw.ToastOverlay(); toast = Adw.Toast(title="Message"); overlay.add_toast(toast)

Deprecated widgets (e.g., Adw.Flap, Adw.Leaflet) should be avoided in new code; use modern alternatives like Adw.NavigationSplitView.

Libadwaita, version 1.8.3 (released January 2026), is a GTK4-based library designed to provide building blocks for modern GNOME applications. It emphasizes adaptive UI elements that scale from desktops to mobile devices, aligning with GNOME's Human Interface Guidelines (HIG). In Python, libadwaita is accessed through PyGObject, which leverages GObject Introspection (GI) to offer dynamic bindings. This means Python code closely mirrors the C API, with classes and methods available under the gi.repository.Adw namespace. Developers can create responsive, theme-aware apps without manual memory management, benefiting from automatic stylesheet loading and style management.
The library's core strength lies in its widgets for navigation, preferences, animations, and status displays, making it ideal for applications targeting the GNOME ecosystem. Research indicates libadwaita is increasingly adopted for its consistency across devices, though it requires GTK4 (version 4.0 or later) and may introduce breaking changes from GTK3-based code. PyGObject ensures compatibility, but always test on target platforms due to potential rendering differences in Wayland vs. X11 environments.
Installation and Setup
As outlined in the direct answer, installation varies by OS. Once installed, verify with:
Pythonimport gi
print(gi.require_versions()) # Should support 'Adw': '1'
For development, use tools like GNOME Builder or VS Code with PyGObject stubs for autocompletion. Libadwaita requires no explicit build steps in Python, as GI handles introspection at runtime.
Initialization and Application Structure
Libadwaita apps typically extend Adw.Application, which subclasses Gtk.Application and handles initialization:
Pythonimport gi
gi.require_version("Adw", "1")
from gi.repository import Adw

Adw.init() # Sets up themes, icons, and translations; optional if using Adw.Application
Using Adw.Application simplifies stylesheet handling. It auto-loads CSS files from your app's resource path (e.g., /com/example/MyApp/style.css) based on system preferences like dark mode or high contrast, managed by Adw.StyleManager:
Pythonstyle_manager = Adw.StyleManager.get_default()
print(style_manager.get_dark()) # True if dark theme active
For windows, use Adw.ApplicationWindow or Adw.Window for free-form layouts.
Key Classes and Widgets
Libadwaita provides over 70 classes, enums, and functions. Below is a comprehensive table of main elements, categorized by type. Descriptions are based on official docs, with Python usage notes. Deprecated items (e.g., pre-1.4) are marked for awareness.

CategoryNameTypeDescriptionPython Example/NotesApplications & WindowsAdw.ApplicationClassBase for GNOME apps, handles styles and init.app = Adw.Application(application_id="com.example.App")Adw.ApplicationWindowClassFree-form window tied to app.win = Adw.ApplicationWindow(application=app)Adw.WindowClassGeneric window.win = Adw.Window(title="App")Adw.WindowTitleClassSets title/subtitle.title = Adw.WindowTitle(title="Main", subtitle="Sub")Dialogs & PreferencesAdw.AboutDialogClassApp info dialog (since 1.5).dialog = Adw.AboutDialog(application_name="MyApp")Adw.AlertDialogClassMessage/question dialog (since 1.5).dialog = Adw.AlertDialog(heading="Confirm?")Adw.PreferencesDialogClassPreferences dialog (since 1.5).pref = Adw.PreferencesDialog()Adw.PreferencesGroupClassGroups rows in preferences.group = Adw.PreferencesGroup(title="Settings")Adw.PreferencesPageClassPage in preferences.page = Adw.PreferencesPage(name="general")Adw.PreferencesRowClassBase row for preferences.Subclass for custom rows.Adw.ShortcutsDialogClassKeyboard shortcuts dialog (since 1.8).shortcuts = Adw.ShortcutsDialog()Navigation & LayoutAdw.NavigationViewClassPage-based navigation (since 1.4).nav = Adw.NavigationView(); nav.push(page)Adw.NavigationSplitViewClassSidebar + content (since 1.4).split = Adw.NavigationSplitView(sidebar=side_widget)Adw.OverlaySplitViewClassOverlay sidebar (since 1.4).Similar to split view but adaptive.Adw.ToolbarViewClassPage with top/bottom bars (since 1.4).view = Adw.ToolbarView(content=main_widget)Adw.MultiLayoutViewClassSwitches layouts (since 1.6).multi = Adw.MultiLayoutView()Adw.BreakpointBinClassSize-based layout changes (since 1.4).bin = Adw.BreakpointBin(child=widget)Containers & AdaptiveAdw.CarouselClassPaginated scrolling.carousel = Adw.Carousel(); carousel.append(page)Adw.ClampClassConstrains child size.clamp = Adw.Clamp(child=widget, maximum_size=400)Adw.HeaderBarClassTitle bar.bar = Adw.HeaderBar(show_start_title_buttons=True)Adw.StatusPageClassEmpty/error states.status = Adw.StatusPage(title="Error", icon_name="dialog-error")Adw.ToastOverlayClassShows toasts.overlay = Adw.ToastOverlay(child=content)Adw.ViewStackClassStacked views.stack = Adw.ViewStack(); stack.add_named(widget, "name")Adw.ViewSwitcherClassAdaptive switcher.switcher = Adw.ViewSwitcher(stack=stack)Rows & ListsAdw.ActionRowClassAction-presenting row.row = Adw.ActionRow(title="Click Me")Adw.ComboRowClassDropdown selection row.row = Adw.ComboRow(model=model)Adw.EntryRowClassText entry row (since 1.2).row = Adw.EntryRow(title="Input")Adw.ExpanderRowClassExpandable row.row = Adw.ExpanderRow(title="Details")Adw.SwitchRowClassToggle row (since 1.4).row = Adw.SwitchRow(title="Enable")AnimationsAdw.AnimationClassBase animation.anim = Adw.TimedAnimation(widget=widget, from_value=0, to_value=1)Adw.SpringAnimationClassSpring-based.Physics-based easing.Adw.TimedAnimationClassTime-based.anim.play()Enums & ModelsAdw.AnimationStateEnumAnimation states (idle, paused, etc.).state = Adw.AnimationState.PLAYINGAdw.ColorSchemeEnumTheme schemes (default, dark).Used in StyleManager.Adw.EnumListModelClassModel for enum values.model = Adw.EnumListModel(enum_type=Adw.ColorScheme)FunctionsAdw.initFunctionInitializes library.Adw.init()Adw.is_initializedFunctionChecks init status.if Adw.is_initialized(): ...DeprecatedAdw.FlapClassOld adaptive container (deprecated 1.4).Migrate to split views.Adw.LeafletClassOld box/stack (deprecated 1.4).Use NavigationView.Adw.MessageDialogClassOld message dialog (deprecated 1.6).Use AlertDialog.
This table covers ~80% of the API; full details in references. For enums like Adw.FoldThreshold (natural, always), use Adw.FoldThreshold.NATURAL.
Advanced Usage and Examples
For a preferences window:
Pythonpref_win = Adw.PreferencesWindow()
page = Adw.PreferencesPage()
group = Adw.PreferencesGroup(title="General")
row = Adw.ActionRow(title="Option 1", subtitle="Toggle me")
switch = Gtk.Switch(valign=Gtk.Align.CENTER)
row.add_suffix(switch)
group.add(row)
page.add(group)
pref_win.add(page)
pref_win.present()
Animations example:
Pythontarget = Adw.CallbackAnimationTarget(callback=lambda value: print(value))
anim = Adw.TimedAnimation(value_from=0, value_to=100, duration=1000, target=target)
anim.play()
Libadwaita integrates with GResources for icons/themes. For mobile adaptability, use breakpoints: breakpoint = Adw.Breakpoint(condition=Adw.BreakpointCondition.parse("max-width: 400px")).
Best Practices and Considerations
Follow GNOME HIG for UI consistency. Test dark/high-contrast modes. Since libadwaita evolves, check changelogs for deprecations (e.g., Adw.AboutWindow deprecated in 1.6). Performance: Use clamps for large UIs. Community examples on GitHub (e.g., python-gtk repos) provide real-world apps.
This documentation compiles key aspects within context limits; for exhaustive method signatures, consult API references.
Key Citations

Releases · GNOME / libadwaita - GitLab
libadwaita-1.8.3 - Linux From Scratch!
Adw – 1 - GNOME
GNOME Python API documentation — GNOME Python API
Overview — PyGObject
Adwaita - PyGObject - GNOME
Tutorials - PyGObject - GNOME
Adwaita Application - PyGObject - GNOME
Getting Started - PyGObject - GNOME
