# Widget Showcase

This example demonstrates all gcompose widgets, including the newly added ones.

## Available Widgets

### Input

Text entry field with optional placeholder and callback support.

```python
Input(
    placeholder="Enter text",
    on_change=lambda text: print(f"Input: {text}"),
    input_type="text",  # or "password", "email"
    styles="w-full hover:bg-gray-100"
)
```

**Props:**

- `value` (str): Initial text value
- `placeholder` (str): Placeholder text
- `on_change` (callable): Callback on text change
- `input_type` (str): "text", "password", or "email"
- `editable` (bool): Whether field is editable
- `bind` (Binding): Optional state binding

---

### Checkbox

Checkbox with optional label and toggle callback.

```python
Checkbox(
    label="Accept terms",
    checked=False,
    on_toggle=lambda checked: print(f"Checked: {checked}"),
    styles="hover:opacity-80"
)
```

**Props:**

- `label` (str): Label text
- `checked` (bool): Initial state
- `on_toggle` (callable): Toggle callback
- `bind` (Binding): Optional state binding

---

### Switch

Toggle switch (like a modern checkbox).

```python
Switch(
    active=True,
    on_toggled=lambda active: print(f"Active: {active}"),
    styles="hover:scale-105"
)
```

**Props:**

- `active` (bool): Initial state
- `on_toggled` (callable): Toggle callback
- `bind` (Binding): Optional state binding

---

### Select

Dropdown/select widget with options (like HTML `<select>`).

```python
Select(
    items=["Option 1", "Option 2", "Option 3"],
    selected_index=0,
    on_change=lambda item: print(f"Selected: {item}"),
    styles="w-full"
)
```

**Props:**

- `items` (list): Items to display
- `selected_index` (int): Initially selected index
- `on_change` (callable): Selection change callback
- `bind` (Binding): Optional state binding

---

### Spacer

Flexible or fixed-size spacer for layout.

```python
# Fixed 10px spacer
Spacer(width=10)

# Flexible spacer that grows to fill space
with Row():
    Text("Left")
    Spacer(flex=True)
    Text("Right")

# Flexible spacer with height
Spacer(height=20, flex=True)
```

**Props:**

- `width` (int): Fixed width in pixels
- `height` (int): Fixed height in pixels
- `flex` (bool): If True, expands to fill space
- `styles` (str): CSS classes

---

### Separator

Visual divider/separator line.

```python
Separator(orientation="horizontal")  # or "vertical"

# Example:
with Column():
    Text("Section 1")
    Separator()
    Text("Section 2")
```

**Props:**

- `orientation` (str): "horizontal" or "vertical"
- `styles` (str): CSS classes

---

## Style Enhancements

### Hover Effects

Use `hover:class-name` syntax to apply CSS classes on hover:

```python
Button(
    label="Hover me",
    styles="bg-gray-100 hover:bg-blue-100 hover:shadow-lg"
)

Input(
    placeholder="Focus here",
    styles="border-gray-300 hover:border-blue-500"
)
```

When the user hovers over the widget, the hover classes are automatically added to its CSS class list and removed when the mouse leaves.

---

## State Binding

All input widgets support state binding via the `bind` parameter:

```python
state = use_state(name="", newsletter=False)

# Bind to Input
Input(bind=Binding(state, "name"))

# Bind to Checkbox
Checkbox(label="Newsletter", bind=Binding(state, "newsletter"))

# Bind to Select
Select(
    items=["USA", "Canada"],
    bind=Binding(state, "country")
)
```

---

## Example Usage

See `app.py` for a complete working example with all widgets.

Run with:

```bash
python app.py
```

---

## Layout Integration

All widgets work seamlessly with `Column()` and `Row()` contexts:

```python
with Column(spacing=8):
    Text("Form")
    Input(placeholder="Name")
    Checkbox(label="Terms")

    with Row(spacing=4):
        Button("Cancel")
        Spacer(flex=True)
        Button("Submit")

    Separator()
    Text("Footer")
```

---

## CSS Class Support

All widgets support GTK CSS classes. Combine with Tailwind-like utility classes:

- `bg-{color}` - Background color
- `text-{color}` - Text color
- `p-{size}` - Padding
- `m-{size}` - Margin
- `w-{size}` - Width
- `h-{size}` - Height
- `rounded` - Border radius
- `shadow` - Box shadow

Example:

```python
Button(
    label="Primary",
    styles="bg-blue-500 text-white p-3 rounded shadow hover:bg-blue-600"
)
```
