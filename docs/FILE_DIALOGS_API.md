# File Dialogs API - Intuitive File Handling

The file dialogs utility provides a clean, web-framework-like API for file operations in GTK applications. It abstracts away GTK 4's lower-level file chooser complexity with callback-based interactions.

## Quick Overview

### Simple File Open

```python
from gcompose import open_file

open_file(
    title="Select Image",
    on_file=lambda path: print(f"Selected: {path}")
)
```

### Save with Filters

```python
from gcompose import save_file

save_file(
    title="Save Document",
    suggested_name="document.txt",
    filters=[
        {"name": "Text Files", "pattern": "*.txt"},
        {"name": "All Files", "pattern": "*"}
    ],
    on_file=lambda path: handle_save(path)
)
```

### Pick Folder

```python
from gcompose import pick_folder

pick_folder(
    title="Select Project Folder",
    on_folder=lambda path: print(f"Project: {path}")
)
```

## Full API Reference

### Convenience Functions (Simple Cases)

#### `open_file(title, on_file, filters=None, initial_folder=None, parent_window=None)`

Open a single file selection dialog.

**Parameters:**

- `title` (str): Dialog window title
- `on_file` (callable): Callback with signature `(path: str)` → None
- `filters` (list): Optional list of `{"name": str, "pattern": str}` dicts
- `initial_folder` (str): Initial folder path
- `parent_window` (Gtk.Window): Parent window for modal dialog

**Example:**

```python
open_file(
    title="Select Image",
    filters=[{"name": "Images", "pattern": "*.png;*.jpg;*.gif"}],
    on_file=lambda path: load_image(path)
)
```

#### `save_file(title, on_file, filters=None, initial_folder=None, suggested_name=None, parent_window=None)`

Open a file save dialog.

**Parameters:**

- `title` (str): Dialog window title
- `on_file` (callable): Callback with signature `(path: str)` → None
- `filters` (list): Optional list of file type filters
- `initial_folder` (str): Initial folder path
- `suggested_name` (str): Pre-filled filename suggestion
- `parent_window` (Gtk.Window): Parent window for modal dialog

**Example:**

```python
save_file(
    title="Export Data",
    suggested_name="export.csv",
    filters=[{"name": "CSV Files", "pattern": "*.csv"}],
    on_file=lambda path: export_data(path)
)
```

#### `pick_folder(title, on_folder, initial_folder=None, parent_window=None)`

Open a folder selection dialog.

**Parameters:**

- `title` (str): Dialog window title
- `on_folder` (callable): Callback with signature `(path: str)` → None
- `initial_folder` (str): Initial folder path
- `parent_window` (Gtk.Window): Parent window for modal dialog

**Example:**

```python
pick_folder(
    title="Select Working Directory",
    on_folder=lambda path: set_project_root(path)
)
```

### `FileDialog` Class (Advanced)

For more control, use the `FileDialog` class directly.

#### `FileDialog.open_file(...)`

Open file selection with additional options.

**Additional Parameters:**

- `multiple` (bool): Allow multiple file selection (default: False)
- `on_files` (callable): Callback for multiple selection: `(paths: List[str])` → None
- `on_cancel` (callable): Callback when dialog is cancelled: `()` → None

**Example (Multiple Selection):**

```python
from gcompose import FileDialog

FileDialog.open_file(
    title="Select Images",
    multiple=True,
    filters=[{"name": "Images", "pattern": "*.png;*.jpg"}],
    on_files=lambda paths: process_images(paths),
    on_cancel=lambda: print("Cancelled")
)
```

#### `FileDialog.save_file(...)`

Open file save with the same signature as the convenience function.

#### `FileDialog.pick_folder(...)`

Open folder selection with the same signature as the convenience function.

## File Filter Specification

Filters are specified as a list of dictionaries:

```python
filters = [
    {"name": "Text Files", "pattern": "*.txt"},
    {"name": "Python Files", "pattern": "*.py"},
    {"name": "Web Files", "pattern": "*.html;*.css;*.js"},
    {"name": "All Files", "pattern": "*"}
]
```

Each filter dict contains:

- `name` (str): Human-readable name shown in the dropdown
- `pattern` (str): File glob pattern(s), multiple separated by `;`

## Complete Example

```python
from gcompose import *
from gcompose.state import use_state

def App():
    state = use_state(file_path="")

    def on_open():
        open_file(
            title="Open Document",
            filters=[
                {"name": "Text Files", "pattern": "*.txt"},
                {"name": "All Files", "pattern": "*"}
            ],
            on_file=lambda path: print(f"Opened: {path}")
        )

    def on_save():
        save_file(
            title="Save Document",
            suggested_name="document.txt",
            on_file=lambda path: print(f"Saved to: {path}")
        )

    def on_pick_folder():
        pick_folder(
            title="Select Project",
            on_folder=lambda path: print(f"Project: {path}")
        )

    with Column(styles="p-4"):
        Text("File Operations")
        with Row(styles="gap-2 mt-4"):
            Button("Open", on_open)
            Button("Save", on_save)
            Button("Pick Folder", on_pick_folder)
```

## Callback-Based Design

All file dialogs are asynchronous and callback-based, similar to web APIs like the File API:

- User interacts with dialog
- On success, appropriate callback is invoked with result(s)
- `on_cancel` is invoked if user cancels
- Dialog is automatically destroyed after interaction

This pattern is familiar to web developers and integrates naturally with GTK's event system.

## Implementation Details

- Uses GTK 4's `FileChooserDialog`
- Paths are returned as absolute strings
- Works with `Gio.File` internally for robust path handling
- Supports relative paths via `Path.expanduser()` for `initial_folder`
- All dialogs are non-blocking (async)
