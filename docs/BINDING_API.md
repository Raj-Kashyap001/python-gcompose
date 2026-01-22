# Binding API - Simplified State Management

The `Binding` class provides an intuitive, web-framework-like API for binding GTK state to widget properties. It abstracts away the complexity of the underlying GObject binding system.

## Quick Overview

**Old (Complex) API:**

```python
Text(
    bind=(state, "count", "label", lambda binding, value: f"Count: {value}"),
    styles="text-blue-400 text-2xl",
)
```

**New (Intuitive) API:**

```python
Text(
    bind=Binding(state, "count", format=lambda value: f"Count: {value}"),
    styles="text-blue-400 text-2xl",
)
```

## Usage

### Basic Binding (1-to-1 Mapping)

Bind a state attribute directly to a widget property:

```python
from gcompose import Text, Binding
from gcompose.state import use_state

state = use_state(name="John")

# Binds state.name to Text label property
Text(bind=Binding(state, "name"))
```

### With Format Function

Transform the state value before displaying it:

```python
state = use_state(count=0)

# Apply custom formatting
Text(bind=Binding(state, "count", format=lambda v: f"Count: {v}"))
```

### Binding to Custom Widget Properties

By default, bindings target the `label` property. Use `widget_prop` to bind to other properties:

```python
state = use_state(progress=0.5)

# Bind to a custom widget property
ProgressBar(bind=Binding(state, "progress", widget_prop="value"))
```

### Complete Example

```python
from gcompose import *
from gcompose.state import use_state

def App():
    state = use_state(count=0)

    def increment():
        state.count += 1

    with Column():
        Text(
            bind=Binding(state, "count", format=lambda v: f"Count: {v}"),
            styles="text-2xl"
        )
        Button("Increment", increment)
```

## API Reference

### `Binding(state, attr, format=None, widget_prop="label")`

**Parameters:**

- `state` (GObject): The state object created with `use_state()` or `make_state()`
- `attr` (str): The attribute name on the state object to bind from
- `format` (callable, optional): Function to transform the value. Signature: `(value) -> str`
- `widget_prop` (str): The widget property to bind to. Default: `"label"`

**Returns:** A `Binding` object that can be passed to widget `bind` parameters

## Backward Compatibility

The old tuple/dict binding syntax is still supported for existing code:

```python
# Old tuple syntax still works
Text(bind=(state, "count", "label", lambda b, v: f"Count: {v}"))

# Old dict syntax still works
Text(bind={
    "state": state,
    "attr": "count",
    "prop": "label",
    "transform": lambda b, v: f"Count: {v}"
})
```

## Under the Hood

The `Binding` class wraps GTK's native `GObject.bind_property()` system, which uses GTK state management (not a custom implementation). This ensures:

- **Performance:** Direct GObject property binding
- **Reactivity:** Automatic re-renders via composition system
- **Type Safety:** GTK's property system handles type conversions
- **Simplicity:** Clean, web-framework-like API

For advanced use cases, you can still use the low-level `bind()` function directly.
