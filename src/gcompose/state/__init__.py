from gi.repository import GObject
from typing import Iterable, Dict, Any

from ..compose.runtime import Composition


def make_state(**kwargs) -> GObject.Object:
    """Create a lightweight GObject state instance with the given initial fields.

    IMPORTANT: State changes DO NOT trigger rerenders anymore. This follows GTK's
    model where state is just data. Only explicit Composition.rerender() calls
    trigger UI updates.

    Example:
        state = make_state(count=0, name="foo")
        state.count = 1  # Just updates the property, no rerender
    """
    props = {}
    for name, val in kwargs.items():
        props[name] = GObject.Property(type=type(val), default=val)

    StateCls = type("State", (GObject.Object,), props)
    inst = StateCls()
    return inst


def adapt(obj: Any, attrs: Iterable[str] = None) -> GObject.Object:
    """Adapt an existing Python object to a GObject with properties.

    - attrs: iterable of attribute names to expose. If None, uses attributes from
      obj.__dict__ (skips callables and private attributes).
    """
    if attrs is None:
        attrs = [n for n in getattr(obj, "__dict__", {}) if not n.startswith("_")]

    # build property map from current values on obj
    props: Dict[str, GObject.Property] = {}
    for name in attrs:
        val = getattr(obj, name)
        props[name] = GObject.Property(type=type(val), default=val)

    AdapterBase = type(f"Adapter_{id(obj)}", (GObject.Object,), props)

    class Adapter(AdapterBase):
        def __init__(self):
            super().__init__()
            self._target = obj
            # initialize values from target
            for n in attrs:
                try:
                    setattr(self, n, getattr(self._target, n))
                except Exception:
                    pass

            # propagate adapter -> target on notify
            self.connect("notify", self._on_notify)

        def _on_notify(self, adapter, pspec):
            name = pspec.name
            try:
                val = getattr(self, name)
                setattr(self._target, name, val)
            except Exception:
                pass

        def pull(self, name: str = None):
            """Copy value(s) from the underlying target -> adapter and emit notify."""
            fields = [name] if name is not None else list(attrs)
            for f in fields:
                try:
                    setattr(self, f, getattr(self._target, f))
                except Exception:
                    pass

    adapter = Adapter()
    return adapter


def bind(state, state_attr, widget, widget_prop="label", flags=None, transform=None):
    """Bind GObject state property to widget property.

    - state: GObject.Object with property `state_attr`
    - widget: target Gtk/GObject
    - widget_prop: name of the target property (default: 'label')
    - flags: GObject.BindingFlags (default includes SYNC_CREATE)
    - transform: optional callable(binding, value) -> transformed value
    """
    if flags is None:
        flags = GObject.BindingFlags.DEFAULT | GObject.BindingFlags.SYNC_CREATE

    if transform is None:
        return state.bind_property(state_attr, widget, widget_prop, flags)
    else:
        return state.bind_property(state_attr, widget, widget_prop, flags, transform)


class Binding:
    """Intuitive binding abstraction for state -> widget properties.

    Simplifies the bind API to be more like web frameworks (React, Svelte, etc).

    Examples:
        # Format with custom transformer
        Binding(state, "count", format=lambda v: f"Count: {v}")

        # Simple property binding (1-to-1)
        Binding(state, "name")

        # Bind to specific widget property (default is "label")
        Binding(state, "progress", widget_prop="value")
    """

    def __init__(self, state, attr, format=None, widget_prop="label"):
        """Create a binding descriptor.

        Args:
            state: GObject state instance
            attr: attribute name on state to bind from
            format: optional callable(value) -> str to transform the value
            widget_prop: widget property to bind to (default: "label")
        """
        self.state = state
        self.attr = attr
        self.format = format
        self.widget_prop = widget_prop

    def apply_to(self, widget):
        """Apply this binding to a widget."""
        transform = None
        if self.format is not None:
            # Wrap format function to match GObject.bind_property signature
            transform = lambda binding, value: self.format(value)

        bind(self.state, self.attr, widget, self.widget_prop, transform=transform)


def use_state(**kwargs):
    """Create or retrieve a persistent state object from the composition hook storage.

    IMPORTANT: State changes do NOT trigger rerenders. This is GTK-style state.

    Example:
        state = use_state(count=0)
        state.count += 1  # Just updates the property, does NOT rerender
    """
    hook = Composition.next_hook()
    if hook is None:
        s = make_state(**kwargs)
        Composition.set_hook(s)
        return s
    return hook


__all__ = ["make_state", "adapt", "bind", "use_state", "Binding"]
