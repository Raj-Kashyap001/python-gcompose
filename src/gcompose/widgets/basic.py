import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk
from ..compose.runtime import Composition
from ..compose.runtime import Composable
from ..styling.css import apply_styles
from ..state import bind as state_bind, Binding


def _apply_binding(widget, bind, default_prop="label"):
    """Apply binding to a widget. Supports Binding objects and legacy tuple/dict formats."""
    if bind is None:
        return

    # New intuitive API: Binding object
    if isinstance(bind, Binding):
        bind.apply_to(widget)
        return

    # Legacy API support: dict format
    if isinstance(bind, dict):
        s = bind.get("state")
        attr = bind.get("attr") or bind.get("name")
        prop = bind.get("prop", default_prop)
        transform = bind.get("transform")
        state_bind(s, attr, widget, prop, transform=transform)
        return

    # Legacy API support: tuple/list format
    try:
        if len(bind) == 2:
            s, attr = bind
            prop = default_prop
            transform = None
        elif len(bind) == 3:
            s, attr, prop = bind
            transform = None
        else:
            s, attr, prop, transform = bind
        state_bind(s, attr, widget, prop, transform=transform)
    except Exception:
        raise ValueError(
            f"bind must be Binding object, tuple (state, attr[, prop[, transform]]), or dict"
        )


def _safe_append(widget):
    """Safely append widget to composition, removing from old parent if needed."""
    parent = widget.get_parent()
    if parent is not None:
        parent.remove(widget)
    Composition.current().append(widget)


@Composable
def Text(value=None, styles=None, bind=None):
    # initial value fallback
    txt = "" if value is None else value
    label = Gtk.Label(label=str(txt), xalign=0)

    _apply_binding(label, bind, default_prop="label")

    apply_styles(label, styles)
    _safe_append(label)
    return label


@Composable
def Button(
    label="",
    on_click=None,
    styles=None,
    bind=None,
    icon=None,
    icon_position="start",
    icon_layout="horizontal",
    icon_gap=6,
):
    # Always create a label child so we can bind to it consistently
    lbl = Gtk.Label(label=str(label), xalign=0)

    if icon:
        # Determine orientation
        orientation = (
            Gtk.Orientation.HORIZONTAL
            if icon_layout == "horizontal"
            else Gtk.Orientation.VERTICAL
        )

        # Create box for layout
        box = Gtk.Box(orientation=orientation, spacing=icon_gap)

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
        # No icon, use label child
        btn = Gtk.Button()
        btn.set_child(lbl)

    # optional binding for the label
    _apply_binding(lbl, bind, default_prop="label")

    if on_click:
        btn.connect("clicked", lambda *_: on_click())
    apply_styles(btn, styles)
    _safe_append(btn)
    return btn


@Composable
def Image(src, styles=None, width=None, height=None):
    """Image composable that supports file paths or icon names. Width and height are mandatory for proper scaling."""
    if width is None or height is None:
        raise ValueError(
            "Image widget requires both width and height parameters for proper scaling"
        )

    if src.startswith("/") or src.startswith("./") or src.startswith("../"):
        # File path
        img = Gtk.Image.new_from_file(src)
    else:
        # Icon name
        img = Gtk.Image.new_from_icon_name(src)

    # Set expand properties to allow the image to fill available space
    img.set_hexpand(True)
    img.set_vexpand(True)
    img.set_halign(Gtk.Align.FILL)
    img.set_valign(Gtk.Align.FILL)

    img.set_pixel_size(min(width, height))  # Use pixel_size for scaling
    img.set_size_request(width, height)

    apply_styles(img, styles)
    _safe_append(img)
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


@Composable
def TextArea(
    value="", styles=None, on_change=None, on_focus_out=None, bind=None, editable=True
):
    """Simplified TextArea widget - widget owns its content.

    Unlike most gcompose widgets, TextArea does NOT synchronize typing back to state.
    Instead, it follows GTK's natural model where the widget owns its content:
    - Initial content comes from `value` parameter (first render only)
    - Call widget.get_text() to read current content
    - Optional `bind` for ONE-WAY loading (state → display only, e.g., file loads)

    Args:
        value: Initial text content (first render only)
        styles: CSS styles to apply
        on_change: Optional callback(text) invoked on every keystroke
        on_focus_out: Optional callback(text) invoked when user leaves field
        bind: Optional Binding for ONE-WAY sync (state→widget) for loading content
        editable: Whether text area is editable (default: True)

    Returns:
        GtkTextView widget with get_text() helper method

    Example:
        state = use_state(current_file="", status="")
        textarea = None

        def load_file(path):
            # Direct widget access: read from file, write to widget
            with open(path, "r") as f:
                buf = textarea.get_buffer()
                buf.set_text(f.read())

        def save_file(path):
            # Direct widget access: read from widget, write to file
            content = textarea.get_text()
            with open(path, "w") as f:
                f.write(content)

        # Render:
        textarea = TextArea(
            value="",
            on_change=lambda text: state.status = f"{len(text)} characters",
            styles="bg-gray-950 text-gray-100 p-3 font-mono",
        )
    """
    from ..compose.runtime import Composition

    hook = Composition.next_hook()

    if hook is None:
        # First render - create widget
        text_buffer = Gtk.TextBuffer()
        text_view = Gtk.TextView(buffer=text_buffer)
        text_view.set_editable(editable)
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        text_view.set_hexpand(True)
        text_view.set_vexpand(True)

        # Set initial value (only on first render)
        text_buffer.set_text(value if value else "")

        # Wrap in ScrolledWindow for scrolling
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(text_view)
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # Create helper to read current text
        def get_buffer_text():
            buf = text_view.get_buffer()
            return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)

        # Store getter on the scrolled window for later access
        scrolled._get_text = get_buffer_text

        # Store widget and buffer for reuse across renders
        Composition.set_hook(
            {
                "text_view": text_view,
                "text_buffer": text_buffer,
                "scrolled": scrolled,
            }
        )

        # Setup on_change callback (local typing event)
        if on_change:

            def on_buffer_changed(_buffer):
                on_change(get_buffer_text())

            text_buffer.connect("changed", on_buffer_changed)

        # Setup on_focus_out callback
        if on_focus_out:
            focus_ctrl = Gtk.EventControllerFocus()

            def on_focus_leave(_controller):
                on_focus_out(get_buffer_text())

            focus_ctrl.connect("leave", on_focus_leave)
            text_view.add_controller(focus_ctrl)

        # Setup ONE-WAY binding (state → widget only, for loading files)
        if bind is not None and isinstance(bind, Binding):

            def on_state_changed(obj, pspec):
                """Sync state to display when state changes externally."""
                new_text = getattr(obj, bind.attr, "")
                current_text = text_buffer.get_text(
                    text_buffer.get_start_iter(),
                    text_buffer.get_end_iter(),
                    False,
                )
                if current_text != str(new_text):
                    text_buffer.set_text(str(new_text))

            bind.state.connect("notify::" + bind.attr, on_state_changed)

    else:
        # Subsequent renders - reuse widget
        text_view = hook["text_view"]
        text_buffer = hook["text_buffer"]
        scrolled = hook["scrolled"]

        # Sync ONE-WAY binding if provided (state → display)
        if bind is not None and isinstance(bind, Binding):
            new_text = getattr(bind.state, bind.attr, "")
            current_text = text_buffer.get_text(
                text_buffer.get_start_iter(),
                text_buffer.get_end_iter(),
                False,
            )
            if current_text != str(new_text):
                text_buffer.set_text(str(new_text))

    # Remove from previous parent if needed
    parent = scrolled.get_parent()
    if parent is not None:
        parent.remove(scrolled)

    apply_styles(text_view, styles)
    Composition.current().append(scrolled)

    return text_view


@Composable
def Input(
    value="",
    placeholder="",
    styles=None,
    on_change=None,
    bind=None,
    editable=True,
    input_type="text",
):
    """Text entry input widget with binding support.

    Args:
        value: Initial text value
        placeholder: Placeholder text
        styles: CSS styles to apply
        on_change: Optional callback(text) invoked on every keystroke
        bind: Optional Binding for two-way sync
        editable: Whether input is editable (default: True)
        input_type: "text", "password", or "email" (affects display)

    Returns:
        GtkEntry widget with get_text() helper
    """
    entry = Gtk.Entry()
    entry.set_text(str(value))
    entry.set_placeholder_text(placeholder)
    entry.set_editable(editable)
    entry.set_hexpand(True)

    # Handle input type
    if input_type == "password":
        entry.set_visibility(False)

    # Setup binding if provided
    _apply_binding(entry, bind, default_prop="text")

    # Setup on_change callback
    if on_change:
        entry.connect("changed", lambda *_: on_change(entry.get_text()))

    apply_styles(entry, styles)

    # Remove from previous parent if needed
    parent = entry.get_parent()
    if parent is not None:
        parent.remove(entry)

    Composition.current().append(entry)
    return entry


@Composable
def Checkbox(label="", checked=False, on_toggle=None, bind=None, styles=None):
    """Checkbox widget with optional label and binding support.

    Args:
        label: Label text to display next to checkbox
        checked: Initial checked state
        on_toggle: Optional callback(is_checked) invoked on toggle
        bind: Optional Binding for state sync
        styles: CSS styles to apply

    Returns:
        GtkCheckButton widget
    """
    check = Gtk.CheckButton(label=label)
    check.set_active(checked)

    # Setup binding if provided
    if bind is not None:
        if isinstance(bind, Binding):
            # Two-way binding for checkbuttons
            bind.apply_to(check)
        else:
            _apply_binding(check, bind, default_prop="active")

    # Setup on_toggle callback
    if on_toggle:
        check.connect("toggled", lambda *_: on_toggle(check.get_active()))

    apply_styles(check, styles)
    Composition.current().append(check)
    return check


@Composable
def Switch(active=False, on_toggled=None, bind=None, styles=None):
    """Toggle switch widget with optional callback and binding.

    Args:
        active: Initial state
        on_toggled: Optional callback(is_active) invoked on toggle
        bind: Optional Binding for state sync
        styles: CSS styles to apply

    Returns:
        GtkSwitch widget
    """
    switch = Gtk.Switch()
    switch.set_active(active)

    # Setup binding if provided
    if bind is not None:
        if isinstance(bind, Binding):
            bind.apply_to(switch)
        else:
            _apply_binding(switch, bind, default_prop="active")

    # Setup on_toggled callback
    if on_toggled:
        switch.connect("notify::active", lambda *_: on_toggled(switch.get_active()))

    apply_styles(switch, styles)
    Composition.current().append(switch)
    return switch


@Composable
def Select(items, selected_index=0, on_change=None, bind=None, styles=None):
    """Dropdown/Select widget mimicking web select with options.

    Args:
        items: List of items to display
        selected_index: Index of initially selected item
        on_change: Optional callback(selected_item) invoked on selection change
        bind: Optional Binding for state sync
        styles: CSS styles to apply

    Returns:
        GtkDropDown widget
    """
    # Create a StringList from items
    string_list = Gtk.StringList.new(None)
    for item in items:
        string_list.append(str(item))

    # Create dropdown
    dropdown = Gtk.DropDown.new(string_list, None)
    dropdown.set_selected(selected_index)

    # Setup binding if provided
    if bind is not None:
        if isinstance(bind, Binding):
            # For dropdown, we bind to selected property
            modified_binding = Binding(
                bind.state, bind.attr, format=bind.format, widget_prop="selected"
            )
            modified_binding.apply_to(dropdown)
        else:
            # Support legacy binding format for selected property
            _apply_binding(dropdown, bind, default_prop="selected")

    # Setup on_change callback
    if on_change:

        def on_dropdown_change(*_):
            selected_idx = dropdown.get_selected()
            if selected_idx < len(items):
                on_change(items[selected_idx])

        dropdown.connect("notify::selected", on_dropdown_change)

    apply_styles(dropdown, styles)
    Composition.current().append(dropdown)
    return dropdown


@Composable
def Spacer(width=None, height=None, flex=False, styles=None):
    """Flexible spacer widget for spacing between elements.

    Args:
        width: Fixed width in pixels (use instead of flex for fixed sizing)
        height: Fixed height in pixels (use instead of flex for fixed sizing)
        flex: If True, spacer expands to fill available space (default: False)
        styles: CSS styles to apply

    Returns:
        GtkBox widget (invisible spacer)

    Example:
        # Fixed 10px spacer
        Spacer(width=10)

        # Flexible spacer that expands
        Spacer(flex=True)

        # Flexible spacer with max height
        with Row():
            Text("Left")
            Spacer(flex=True)
            Text("Right")
    """
    spacer = Gtk.Box()

    if flex:
        spacer.set_hexpand(True)
        spacer.set_vexpand(True)
    else:
        if width is not None:
            spacer.set_size_request(width, -1)
        if height is not None:
            current_width = spacer.get_size_request()[0]
            spacer.set_size_request(current_width, height)

    apply_styles(spacer, styles)
    Composition.current().append(spacer)
    return spacer


@Composable
def Separator(orientation="horizontal", styles=None):
    """Visual separator/divider widget.

    Args:
        orientation: "horizontal" or "vertical" (default: "horizontal")
        styles: CSS styles to apply

    Returns:
        GtkSeparator widget

    Example:
        with Column():
            Text("Section 1")
            Separator()
            Text("Section 2")
    """
    if orientation not in ("horizontal", "vertical"):
        raise ValueError('orientation must be "horizontal" or "vertical"')

    orientation_enum = (
        Gtk.Orientation.HORIZONTAL
        if orientation == "horizontal"
        else Gtk.Orientation.VERTICAL
    )
    separator = Gtk.Separator(orientation=orientation_enum)

    # Set expand properties to fill space appropriately
    if orientation == "horizontal":
        separator.set_hexpand(True)
    else:
        separator.set_vexpand(True)

    apply_styles(separator, styles)
    Composition.current().append(separator)
    return separator
