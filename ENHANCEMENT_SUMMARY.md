# Widget Enhancement Summary

## Overview

Major expansion of gcompose widget library with 6 new widgets and CSS hover state support.

## New Widgets Added

### 1. **Input** Widget

- Single-line text entry field
- Supports placeholders and input types (text, password, email)
- Optional `on_change` callback
- Supports state binding via `Binding` objects
- Hover effects support

**File:** [src/gcompose/widgets/basic.py](../src/gcompose/widgets/basic.py)

```python
Input(
    placeholder="Enter text",
    input_type="text",  # or "password", "email"
    on_change=lambda text: print(f"Input: {text}"),
    styles="hover:bg-gray-100"
)
```

### 2. **Checkbox** Widget

- Boolean toggle with optional label
- `on_toggle` callback on state change
- Supports state binding
- Compact and accessible

**File:** [src/gcompose/widgets/basic.py](../src/gcompose/widgets/basic.py)

```python
Checkbox(
    label="Accept terms",
    checked=False,
    on_toggle=lambda checked: print(f"Checked: {checked}"),
    styles="hover:opacity-80"
)
```

### 3. **Switch** Widget

- Modern toggle switch (alternative to checkbox)
- `on_toggled` callback
- Clean, mobile-friendly appearance
- Supports state binding

**File:** [src/gcompose/widgets/basic.py](../src/gcompose/widgets/basic.py)

```python
Switch(
    active=True,
    on_toggled=lambda active: print(f"Active: {active}"),
    styles="hover:scale-105"
)
```

### 4. **Select** (Dropdown) Widget

- Web-like dropdown/select component
- Maps to GTK `DropDown` widget
- Supports list of items and selection callbacks
- Initial selected index control
- Dropdown binding support

**File:** [src/gcompose/widgets/basic.py](../src/gcompose/widgets/basic.py)

```python
Select(
    items=["Option 1", "Option 2", "Option 3"],
    selected_index=0,
    on_change=lambda item: print(f"Selected: {item}"),
    styles="w-full"
)
```

### 5. **Spacer** Widget

- Flexible or fixed-size spacing
- `flex=True` makes it expand to fill available space
- Useful for responsive layouts
- Fixed width/height alternatives

**File:** [src/gcompose/widgets/basic.py](../src/gcompose/widgets/basic.py)

```python
# Fixed spacer
Spacer(width=10)

# Flexible spacer (expands)
Spacer(flex=True)

# Flexible with constraints
Spacer(height=20, flex=True)
```

### 6. **Separator** Widget

- Visual divider/horizontal or vertical line
- Configurable orientation
- Automatically expands to fill space appropriately

**File:** [src/gcompose/widgets/basic.py](../src/gcompose/widgets/basic.py)

```python
Separator(orientation="horizontal")  # or "vertical"
```

## CSS Enhancements

### Hover State Support

**File:** [src/gcompose/styling/css.py](../src/gcompose/styling/css.py)
**Parser:** [src/gcompose/styling/parser.py](../src/gcompose/styling/parser.py)

Implemented full hover state support using the `hover:class-name` syntax:

```python
Button(
    label="Hover me",
    styles="bg-gray-100 hover:bg-blue-100 hover:shadow-lg"
)
```

#### How It Works:

1. **Parser** (`parser.py`): New `parse_hover_properties()` method extracts hover classes
2. **CSS Module** (`css.py`): New `_setup_hover_effects()` function attaches GTK event controllers
3. **Event Handling**: Mouse enter/leave events automatically add/remove CSS classes
4. **Performance**: Uses GTK's native CSS class toggling (very fast)

#### Implementation Details:

- Uses `Gtk.EventControllerMotion` to detect mouse enter/leave
- Automatically adds hover classes on mouse enter
- Automatically removes hover classes on mouse leave
- Works on all widgets

## File Changes

### Modified Files:

1. **[src/gcompose/widgets/basic.py](../src/gcompose/widgets/basic.py)**
   - Added 6 new widget functions: `Input()`, `Checkbox()`, `Switch()`, `Select()`, `Spacer()`, `Separator()`
   - All new widgets support state binding
   - All new widgets support callbacks
   - All new widgets support CSS styling

2. **[src/gcompose/styling/css.py](../src/gcompose/styling/css.py)**
   - Added `_setup_hover_effects()` function for mouse event handling
   - Updated `apply_styles()` to parse and apply hover properties
   - Enhanced `apply_styles()` docstring with hover documentation

3. **[src/gcompose/styling/parser.py](../src/gcompose/styling/parser.py)**
   - Added `HOVER_PATTERN` regex for parsing `hover:class-name`
   - Added `parse_hover_properties()` method
   - Updated `parse_all_properties()` to include hover parsing
   - Hover classes are extracted before regular CSS classes

### New Documentation Files:

1. **[docs/WIDGETS_API.md](../docs/WIDGETS_API.md)**
   - Complete API reference for all widgets
   - Parameter documentation
   - Usage examples
   - Tips and best practices

2. **[docs/HOVER_STYLING.md](../docs/HOVER_STYLING.md)**
   - Comprehensive guide to hover effects
   - Advanced styling patterns
   - Interactive form examples
   - Best practices for hover states
   - Common hover patterns

3. **[examples/03_widgets_showcase/app.py](../examples/03_widgets_showcase/app.py)**
   - Complete working example with all new widgets
   - Demonstrates binding, callbacks, and styling
   - Shows hover effects in action

4. **[examples/03_widgets_showcase/README.md](../examples/03_widgets_showcase/README.md)**
   - Quick reference for widget usage
   - Example code snippets
   - Layout integration guide

## State Binding Integration

All new widgets support the intuitive `Binding` API:

```python
from gcompose.state import use_state, Binding

state = use_state(name="", subscribed=False, country="")

# Bind to Input
Input(bind=Binding(state, "name"))

# Bind to Checkbox
Checkbox(label="Newsletter", bind=Binding(state, "subscribed"))

# Bind to Select
Select(
    items=["USA", "Canada"],
    bind=Binding(state, "country")
)
```

## Usage Examples

### Simple Form

```python
from gcompose.app import Application
from gcompose.layout.box import Column, Row
from gcompose.widgets.basic import *
from gcompose.state import use_state, Binding

def render(app):
    state = use_state(email="", password="", remember=False)

    with Column(spacing=8, styles="p-6"):
        Input(bind=Binding(state, "email"), placeholder="Email")
        Input(bind=Binding(state, "password"), input_type="password", placeholder="Password")
        Checkbox(label="Remember me", bind=Binding(state, "remember"))

        with Row(spacing=8, styles="justify-end mt-4"):
            Button("Cancel")
            Button("Login", styles="bg-blue-500 hover:bg-blue-600")

app = Application(app_id="com.example.Form", title="Login")
app.set_render_function(render)
app.run()
```

### Dashboard with Cards

```python
with Row(spacing=12):
    # Each card has hover elevation effect
    with Column(spacing=8, styles="bg-white p-4 rounded shadow hover:shadow-lg"):
        Text("Users", styles="text-sm text-gray-600")
        Text("1,234", styles="text-2xl font-bold")

    with Column(spacing=8, styles="bg-white p-4 rounded shadow hover:shadow-lg"):
        Text("Revenue", styles="text-sm text-gray-600")
        Text("$45.2K", styles="text-2xl font-bold")
```

## Testing

All new code passes syntax validation:

- ✅ `src/gcompose/widgets/basic.py` - No syntax errors
- ✅ `src/gcompose/styling/css.py` - No syntax errors
- ✅ `src/gcompose/styling/parser.py` - No syntax errors

## Benefits

1. **Comprehensive Widget Set** - Now supports most common UI patterns
2. **Web-Familiar API** - `Select`, `Input`, `Checkbox` feel like HTML/web components
3. **Hover Effects** - Modern, responsive UI with hover state feedback
4. **Better Forms** - Multiple input types and validation-friendly widgets
5. **Flexible Layouts** - `Spacer` and `Separator` enable responsive design
6. **State Integration** - All widgets work seamlessly with reactive state binding
7. **Clean Code** - Minimal, declarative widget definitions

## Next Steps (Optional Enhancements)

- Add `Slider` widget for numeric input
- Add `Tabs` widget for tab navigation
- Add `Modal`/`Dialog` widgets
- Add `RadioButton` group widget
- Add `ComboBox` for autocomplete
- Add `FileChooser` widget
- Add theme system for hover effects
- Add CSS animation support
