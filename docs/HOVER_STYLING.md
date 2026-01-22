# Advanced Styling & Hover Effects Guide

This document shows advanced styling patterns and hover effect usage in gcompose.

## Hover Effects Syntax

Use `hover:class-name` to apply CSS classes on mouse enter:

```python
Button(
    label="Hover Button",
    styles="bg-gray-100 hover:bg-blue-100"
)
```

Multiple hover classes are supported:

```python
Button(
    label="Complex Hover",
    styles="bg-white border-2 border-gray-300 hover:bg-blue-50 hover:border-blue-500 hover:shadow-md"
)
```

## Interactive Form Example

```python
from gcompose.app import Application
from gcompose.layout.box import Column, Row
from gcompose.widgets.basic import *
from gcompose.state import use_state, Binding


def render(app):
    state = use_state(
        email="",
        password="",
        remember_me=False,
        errors=""
    )

    with Column(spacing=16, styles="p-8 w-full h-full"):
        # Header
        Text("Login", styles="text-3xl font-bold text-gray-900")
        Text("Enter your credentials", styles="text-gray-600 mb-6")

        Separator()

        # Email input with hover and focus states
        Text("Email", styles="text-sm font-semibold text-gray-700 mt-4")
        Input(
            placeholder="user@example.com",
            input_type="email",
            bind=Binding(state, "email"),
            styles="w-full bg-white border-2 border-gray-300 hover:border-blue-400 hover:bg-blue-50"
        )

        # Password input
        Text("Password", styles="text-sm font-semibold text-gray-700 mt-4")
        Input(
            placeholder="••••••••",
            input_type="password",
            bind=Binding(state, "password"),
            styles="w-full bg-white border-2 border-gray-300 hover:border-blue-400 hover:bg-blue-50"
        )

        # Remember me checkbox with hover effect
        Checkbox(
            label="Remember me",
            checked=state.remember_me,
            on_toggle=lambda x: setattr(state, "remember_me", x),
            styles="mt-2 hover:opacity-75"
        )

        # Error message (conditional)
        if state.errors:
            Text(
                state.errors,
                styles="bg-red-100 text-red-800 p-3 rounded border-l-4 border-red-500"
            )

        # Spacer to push buttons down
        Spacer(flex=True)

        Separator()

        # Button row with hover effects
        with Row(spacing=8, styles="justify-end mt-6"):
            Button(
                "Cancel",
                styles="bg-gray-200 text-gray-900 p-2 rounded hover:bg-gray-300 hover:shadow-md"
            )
            Button(
                "Sign In",
                styles="bg-blue-600 text-white p-2 rounded hover:bg-blue-700 hover:shadow-lg"
            )


# Run the app
app = Application(app_id="com.example.LoginForm", title="Login Form", width=400, height=500)
app.set_render_function(render)
app.run()
```

## Dashboard Layout with Hover Cards

```python
def render(app):
    with Column(spacing=16, styles="p-6"):
        Text("Dashboard", styles="text-3xl font-bold")

        Separator()

        # Card-like widgets with hover effects
        with Row(spacing=12):
            # Card 1
            with Column(spacing=8, styles="bg-white p-4 rounded shadow hover:shadow-lg"):
                Text("Users", styles="text-sm text-gray-600")
                Text("1,234", styles="text-2xl font-bold")
                Text("↑ 12% from last month", styles="text-xs text-green-600")

            # Card 2
            with Column(spacing=8, styles="bg-white p-4 rounded shadow hover:shadow-lg"):
                Text("Revenue", styles="text-sm text-gray-600")
                Text("$45.2K", styles="text-2xl font-bold")
                Text("↓ 3% from last month", styles="text-xs text-red-600")

            # Card 3
            with Column(spacing=8, styles="bg-white p-4 rounded shadow hover:shadow-lg"):
                Text("Conversion", styles="text-sm text-gray-600")
                ProgressBar(fraction=0.72, show_text=True, text="72%")


app = Application(app_id="com.example.Dashboard", title="Dashboard", width=900, height=600)
app.set_render_function(render)
app.run()
```

## Interactive Select with Hover

```python
def render(app):
    state = use_state(selected_country="")

    with Column(spacing=12, styles="p-6"):
        Text("Choose Location", styles="text-xl font-bold")

        countries = ["🇺🇸 United States", "🇨🇦 Canada", "🇲🇽 Mexico", "🇬🇧 UK", "🇦🇺 Australia"]

        Select(
            items=countries,
            selected_index=0,
            on_change=lambda item: setattr(state, "selected_country", item),
            styles="w-full bg-white hover:bg-gray-50 border-2 border-gray-200 hover:border-blue-400"
        )

        if state.selected_country:
            Text(
                f"Selected: {state.selected_country}",
                styles="text-green-600 mt-4 p-3 bg-green-50 rounded"
            )
```

## Button Variations with Hover

```python
def render(app):
    with Column(spacing=12, styles="p-6"):
        Text("Button Variations", styles="text-2xl font-bold mb-4")

        # Primary button
        Button(
            "Primary Button",
            styles="bg-blue-600 text-white p-3 rounded hover:bg-blue-700 hover:shadow-md"
        )

        # Secondary button
        Button(
            "Secondary Button",
            styles="bg-gray-200 text-gray-900 p-3 rounded hover:bg-gray-300 hover:shadow-md"
        )

        # Danger button
        Button(
            "Delete",
            styles="bg-red-600 text-white p-3 rounded hover:bg-red-700 hover:shadow-md"
        )

        # Success button
        Button(
            "Save",
            styles="bg-green-600 text-white p-3 rounded hover:bg-green-700 hover:shadow-md"
        )

        # Outlined button
        Button(
            "Outlined",
            styles="border-2 border-blue-600 text-blue-600 p-3 rounded hover:bg-blue-50"
        )

        # Ghost button
        Button(
            "Ghost",
            styles="text-gray-600 p-3 hover:bg-gray-100 rounded"
        )


app = Application(app_id="com.example.Buttons", title="Button Showcase", width=400, height=400)
app.set_render_function(render)
app.run()
```

## Form with Validation Feedback

```python
def render(app):
    state = use_state(
        email="",
        password="",
        form_submitted=False,
        email_error=None,
        password_error=None
    )

    def validate():
        errors = {}
        if not state.email or "@" not in state.email:
            errors["email"] = "Invalid email"
        if not state.password or len(state.password) < 6:
            errors["password"] = "Password must be at least 6 characters"

        state.email_error = errors.get("email")
        state.password_error = errors.get("password")
        state.form_submitted = len(errors) == 0

    with Column(spacing=12, styles="p-8 w-full h-full"):
        Text("Registration", styles="text-3xl font-bold mb-2")

        Separator()

        # Email field with error display
        Text("Email", styles="text-sm font-semibold text-gray-700 mt-4")
        Input(
            placeholder="user@example.com",
            bind=Binding(state, "email"),
            styles="w-full border-2 hover:border-blue-400 " + (
                "border-red-500 hover:border-red-600" if state.email_error else "border-gray-300"
            )
        )
        if state.email_error:
            Text(state.email_error, styles="text-red-600 text-sm mt-1")

        # Password field with error display
        Text("Password", styles="text-sm font-semibold text-gray-700 mt-4")
        Input(
            placeholder="••••••••",
            input_type="password",
            bind=Binding(state, "password"),
            styles="w-full border-2 hover:border-blue-400 " + (
                "border-red-500 hover:border-red-600" if state.password_error else "border-gray-300"
            )
        )
        if state.password_error:
            Text(state.password_error, styles="text-red-600 text-sm mt-1")

        Spacer(flex=True)

        Separator()

        # Submit button
        Button(
            "Register",
            on_click=validate,
            styles="w-full bg-blue-600 text-white p-3 rounded font-semibold hover:bg-blue-700 hover:shadow-lg"
        )

        if state.form_submitted:
            Text("✓ Registration successful!", styles="text-green-600 text-center mt-4 p-3 bg-green-50 rounded")


app = Application(app_id="com.example.Register", title="Registration", width=400, height=500)
app.set_render_function(render)
app.run()
```

## Key Hover Patterns

### 1. **Brightness/Opacity Change**

```python
# Slightly darken on hover
styles="hover:opacity-90"

# Brighten background
styles="bg-gray-100 hover:bg-blue-100"
```

### 2. **Shadow Elevation**

```python
# Add shadow on hover (card effect)
styles="shadow hover:shadow-lg"

# Increase shadow intensity
styles="shadow-md hover:shadow-xl"
```

### 3. **Border Emphasis**

```python
# Change border color on hover
styles="border-gray-300 hover:border-blue-500"

# Add border on hover
styles="hover:border-2 hover:border-blue-500"
```

### 4. **Text Emphasis**

```python
# Make text bolder on hover
styles="hover:font-bold"

# Change text color
styles="text-gray-600 hover:text-blue-600"
```

### 5. **Combined Effects**

```python
# Multiple effects together
styles="bg-gray-100 border-gray-300 shadow hover:bg-blue-50 hover:border-blue-500 hover:shadow-lg"
```

## Best Practices

1. **Consistency** - Use the same hover pattern across similar widgets
2. **Subtlety** - Don't make hover changes too dramatic
3. **Performance** - Hover effects are applied via CSS class toggling (very fast)
4. **Accessibility** - Ensure hover states are visible and meaningful
5. **Mobile** - Remember that touchscreen devices don't have hover (use tactile feedback instead)
6. **User Feedback** - Use hover to indicate interactivity
