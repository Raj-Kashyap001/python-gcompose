# Widget API Reference

Complete reference for all gcompose widgets and their APIs.

## Basic Widgets

### Text

Display static text.

```python
Text(
    value="Hello World",
    styles="text-lg font-bold",
    bind=None  # Optional binding for dynamic text
)
```

### Button

Clickable button with optional icon.

```python
Button(
    label="Click me",
    on_click=lambda: print("Clicked"),
    styles="bg-blue-500 hover:bg-blue-600",
    icon="dialog-ok",  # GTK icon name or path
    icon_position="start",  # or "end"
)
```

### Image

Display image from file or icon name.

```python
Image(
    src="/path/to/image.png",  # or "image-icon"
    width=100,
    height=100,
    styles="rounded shadow"
)
```

---

## Input Widgets

### Input

Single-line text entry.

```python
Input(
    value="",
    placeholder="Enter text",
    input_type="text",  # "text", "password", "email"
    on_change=lambda text: ...,
    bind=None,
    editable=True,
    styles=""
)
```

### TextArea

Multi-line text editor.

```python
textarea = TextArea(
    value="Initial text",
    on_change=lambda text: ...,
    on_focus_out=lambda text: ...,
    editable=True,
    bind=None,
    styles="h-200 font-mono"
)

# Read content:
content = textarea.get_text()
```

**Note:** TextArea stores state internally, not in reactive state.

### Checkbox

Boolean checkbox with label.

```python
Checkbox(
    label="Accept terms",
    checked=False,
    on_toggle=lambda checked: ...,
    bind=None,
    styles=""
)
```

### Switch

Toggle switch (modern checkbox style).

```python
Switch(
    active=False,
    on_toggled=lambda active: ...,
    bind=None,
    styles=""
)
```

### Select

Dropdown/select list.

```python
Select(
    items=["Option A", "Option B", "Option C"],
    selected_index=0,
    on_change=lambda item: ...,
    bind=None,
    styles="w-full"
)
```

---

## Display Widgets

### ProgressBar

Progress indicator.

```python
ProgressBar(
    fraction=0.65,  # 0.0 - 1.0
    show_text=True,
    text="65%",
    styles=""
)
```

### List

Selectable list of items.

```python
List(
    items=["Item 1", "Item 2", "Item 3"],
    selection_mode="none",  # "single", "multiple", "none"
    on_select=lambda item: ...,
    styles="h-200"
)
```

---

## Layout Widgets

### Spacer

Flexible or fixed spacing.

```python
# Fixed 10px spacer
Spacer(width=10)

# Flexible spacer that grows
Spacer(flex=True)

# Spacer with height constraint
Spacer(height=20, flex=True)
```

### Separator

Horizontal or vertical divider.

```python
Separator(orientation="horizontal")  # or "vertical"
```

### Column

Vertical container (context manager).

```python
with Column(spacing=8, styles="p-4"):
    Text("Header")
    # Child widgets here
```

### Row

Horizontal container (context manager).

```python
with Row(spacing=8):
    Text("Left")
    Spacer(flex=True)
    Text("Right")
```

---

## State & Binding

### use_state

Create persistent reactive state.

```python
state = use_state(count=0, name="")
state.count += 1  # Updates property
```

### Binding

Create declarative state bindings.

```python
from gcompose.state import Binding

state = use_state(name="", email="")

# Simple binding
Input(bind=Binding(state, "name"))

# With custom formatter
Input(
    bind=Binding(
        state,
        "email",
        widget_prop="text",
        format=lambda v: f"Email: {v}"
    )
)
```

---

## Styling

### CSS Classes

Apply Tailwind-like utilities:

```python
Button(styles="bg-blue-500 text-white p-3 rounded")
```

Common classes:

- `bg-{color}` - Background
- `text-{color}` - Text color
- `p-{n}` - Padding
- `m-{n}` - Margin
- `w-{n}` - Width
- `h-{n}` - Height
- `rounded` - Border radius
- `shadow` - Box shadow

### Hover Effects

Apply classes on mouse hover:

```python
Button(
    label="Hover me",
    styles="bg-gray-100 hover:bg-blue-100 hover:shadow-lg"
)
```

All `hover:*` classes are automatically added on mouse enter and removed on mouse leave.

### Size Properties

Programmatic sizing:

```python
Text("Content", styles="w-200 h-100")  # 200px × 100px
Text("Full", styles="w-full h-full")   # Fill available space
```

### Alignment

Alignment within containers:

```python
with Row(styles="justify-center items-center"):
    # Horizontally and vertically centered content
```

Options:

- `justify-start`, `justify-center`, `justify-end`, `justify-stretch`
- `items-start`, `items-center`, `items-end`, `items-stretch`

---

## Event Handlers

### Callbacks

Widgets support optional callbacks:

```python
Button(on_click=lambda: ...)
Input(on_change=lambda text: ...)
Checkbox(on_toggle=lambda checked: ...)
Select(on_change=lambda item: ...)
Switch(on_toggled=lambda active: ...)
```

### Focus Events

Some widgets support focus events:

```python
TextArea(
    on_focus_out=lambda text: print(f"Left field with: {text}")
)
```

---

## Tips & Best Practices

1. **TextArea is not reactive** - Use `widget.get_text()` to read content
2. **Use Spacer(flex=True)** for responsive layouts
3. **Combine layouts** - Column/Row can be nested
4. **Hover classes** - Use `hover:` prefix for interactive effects
5. **State binding** - Use `Binding` for declarative UI updates
6. **CSS Classes** - Load custom CSS with `load_css(path)`

---

## Full Widget Example

```python
from gcompose.app import Application
from gcompose.layout.box import Column, Row
from gcompose.widgets.basic import *
from gcompose.state import use_state, Binding

def render(app):
    state = use_state(name="", subscribed=False)

    with Column(spacing=16, styles="p-6"):
        Text("Subscribe", styles="text-2xl font-bold")

        Input(
            placeholder="Your name",
            bind=Binding(state, "name"),
            styles="hover:bg-gray-50"
        )

        Checkbox(
            label="Subscribe to newsletter",
            on_toggle=lambda x: setattr(state, "subscribed", x)
        )

        Separator()

        with Row(spacing=8, styles="justify-end"):
            Button("Cancel")
            Button("Subscribe", styles="bg-blue-500 text-white hover:bg-blue-600")

app = Application(app_id="com.example.Sub", title="Subscribe")
app.set_render_function(render)
app.run()
```
