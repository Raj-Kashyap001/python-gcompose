# Quick Reference: New Widgets & Hover Effects

## Widget Quick Reference

### Input

```python
Input(
    value="",
    placeholder="hint text",
    input_type="text",  # "text", "password", "email"
    on_change=callback,
    bind=Binding(state, "attr"),
    styles="hover:bg-gray-100"
)
```

### Checkbox

```python
Checkbox(
    label="Label text",
    checked=False,
    on_toggle=callback,
    bind=Binding(state, "attr")
)
```

### Switch

```python
Switch(
    active=False,
    on_toggled=callback,
    bind=Binding(state, "attr")
)
```

### Select (Dropdown)

```python
Select(
    items=["Option 1", "Option 2"],
    selected_index=0,
    on_change=callback,
    bind=Binding(state, "attr")
)
```

### Spacer

```python
Spacer(width=10)           # Fixed 10px
Spacer(flex=True)          # Flexible, grows
Spacer(height=20)          # Fixed height
```

### Separator

```python
Separator()                         # Horizontal
Separator(orientation="vertical")   # Vertical
```

---

## Hover Effects

### Syntax

```python
# Single hover class
styles="hover:bg-blue-100"

# Multiple hover classes
styles="bg-gray-100 hover:bg-blue-100 hover:shadow-lg"

# Combined with regular classes
styles="rounded shadow hover:shadow-xl hover:opacity-95"
```

### Common Patterns

```python
# Color change
styles="bg-gray-100 hover:bg-blue-100"

# Shadow elevation (card effect)
styles="shadow hover:shadow-lg"

# Border emphasis
styles="border-gray-300 hover:border-blue-500"

# Text emphasis
styles="text-gray-600 hover:text-blue-600 hover:font-semibold"

# Combined
styles="bg-white border-gray-200 shadow hover:bg-blue-50 hover:border-blue-400 hover:shadow-md"
```

---

## Form Example

```python
def render(app):
    state = use_state(name="", email="", agreed=False)

    with Column(spacing=8, styles="p-6"):
        # Name input
        Text("Name", styles="font-semibold text-sm text-gray-700")
        Input(
            placeholder="Full name",
            bind=Binding(state, "name"),
            styles="w-full border-2 border-gray-300 hover:border-blue-400"
        )

        # Email input
        Text("Email", styles="font-semibold text-sm text-gray-700 mt-4")
        Input(
            placeholder="email@example.com",
            input_type="email",
            bind=Binding(state, "email"),
            styles="w-full border-2 border-gray-300 hover:border-blue-400"
        )

        # Checkbox
        Checkbox(
            label="I agree to terms",
            bind=Binding(state, "agreed"),
            styles="mt-4"
        )

        # Separator
        Separator()

        # Buttons
        with Row(spacing=8, styles="justify-end"):
            Button("Cancel", styles="hover:bg-gray-200")
            Button("Submit", styles="bg-blue-500 text-white hover:bg-blue-600")

app = Application(app_id="com.example.Form", title="Form")
app.set_render_function(render)
app.run()
```

---

## Layout with Spacer

```python
# Space elements apart
with Row(spacing=0):
    Text("Left")
    Spacer(flex=True)      # Pushes next item to right
    Text("Right")

# Create gaps
with Column(spacing=0):
    Button("Button 1")
    Spacer(height=20)      # 20px gap
    Button("Button 2")
    Spacer(flex=True)      # Take remaining space
    Button("Bottom")
```

---

## Card with Hover

```python
with Column(
    spacing=8,
    styles="bg-white p-4 rounded shadow hover:shadow-lg"
):
    Text("Card Title", styles="font-bold")
    Text("Card content here")
```

---

## Dashboard Layout

```python
with Column(spacing=16, styles="p-6"):
    # Header
    Text("Dashboard", styles="text-3xl font-bold")
    Separator()

    # Cards row
    with Row(spacing=12):
        # Card 1
        with Column(spacing=4, styles="bg-white p-4 rounded shadow hover:shadow-lg"):
            Text("Metric 1", styles="text-sm text-gray-600")
            Text("123", styles="text-2xl font-bold")

        # Card 2
        with Column(spacing=4, styles="bg-white p-4 rounded shadow hover:shadow-lg"):
            Text("Metric 2", styles="text-sm text-gray-600")
            Text("456", styles="text-2xl font-bold")

    Spacer(flex=True)
    Separator()

    # Footer buttons
    with Row(spacing=8, styles="justify-end"):
        Button("Cancel", styles="hover:bg-gray-200")
        Button("Save", styles="bg-green-500 text-white hover:bg-green-600")
```

---

## Hover Best Practices

✅ **DO:**

- Use consistent hover colors across the app
- Make hover effects visible but subtle
- Test hover on different background colors
- Use shadow elevation for card-like components
- Combine multiple hover effects for rich feedback

❌ **DON'T:**

- Make hover changes too dramatic
- Use too many different hover styles
- Forget that mobile users can't hover
- Make important interactions rely only on hover
- Make hover effects too slow or jarring

---

## State Binding Quick Tips

```python
# Create state
state = use_state(field1="", field2=False)

# Bind to Input
Input(bind=Binding(state, "field1"))

# Read from state
current_value = state.field1

# Update state
state.field2 = True

# Format with Binding
Input(
    bind=Binding(
        state,
        "count",
        format=lambda v: f"Count: {v}"
    )
)
```

---

## Imports

```python
from gcompose.app import Application
from gcompose.layout.box import Column, Row
from gcompose.widgets.basic import (
    Text, Button, Image, ProgressBar, List, TextArea,
    Input, Checkbox, Switch, Select, Spacer, Separator
)
from gcompose.state import use_state, Binding
from gcompose.styling.css import load_css, apply_styles
```

---

## Documentation Links

- **Full Widget API:** [WIDGETS_API.md](../../docs/WIDGETS_API.md)
- **Hover Effects Guide:** [HOVER_STYLING.md](../../docs/HOVER_STYLING.md)
- **Examples:** [03_widgets_showcase/](../03_widgets_showcase/)
- **Enhancement Summary:** [ENHANCEMENT_SUMMARY.md](../../ENHANCEMENT_SUMMARY.md)
