# File Dialogs Utility - Implementation Summary

## Overview

Created an intuitive, web-framework-like abstraction layer over GTK 4's file chooser dialogs. The utility uses callback-based design patterns similar to modern web APIs and JavaScript frameworks.

## Files Created

### Core Implementation

- **[src/gcompose/utils/**init**.py](src/gcompose/utils/__init__.py)** - Utils package exports
- **[src/gcompose/utils/file_dialogs.py](src/gcompose/utils/file_dialogs.py)** - Main file dialog implementation (336 lines)

### Documentation

- **[docs/FILE_DIALOGS_API.md](docs/FILE_DIALOGS_API.md)** - Complete API reference and usage guide

### Examples

- **[examples/file_dialogs_example.py](examples/file_dialogs_example.py)** - Demonstrates all features (open, save, pick folder, multiple selection)
- **[examples/text_editor_example.py](examples/text_editor_example.py)** - Practical use case (simple text editor)

### Updated Files

- **[src/gcompose/**init**.py](src/gcompose/__init__.py)** - Exports file dialog utilities

## API

### Quick Functions (Simple Cases)

```python
# Open single file
open_file(title, on_file, filters=None, initial_folder=None, parent_window=None)

# Save file
save_file(title, on_file, filters=None, initial_folder=None, suggested_name=None, parent_window=None)

# Pick folder
pick_folder(title, on_folder, initial_folder=None, parent_window=None)
```

### FileDialog Class (Advanced)

```python
# More control with additional options
FileDialog.open_file(
    title,
    multiple=False,
    filters=None,
    on_file=None,
    on_files=None,
    on_cancel=None,
    parent_window=None,
    initial_folder=None
)
```

## Usage Examples

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
    on_file=lambda path: print(f"Save to: {path}")
)
```

### Multiple File Selection

```python
from gcompose import FileDialog

FileDialog.open_file(
    title="Select Images",
    multiple=True,
    filters=[{"name": "Images", "pattern": "*.png;*.jpg"}],
    on_files=lambda paths: print(f"Selected {len(paths)} files"),
    on_cancel=lambda: print("Cancelled")
)
```

### Pick Folder

```python
from gcompose import pick_folder

pick_folder(
    title="Select Project",
    on_folder=lambda path: print(f"Project: {path}")
)
```

## Design Principles

✅ **Callback-Based** - Async pattern familiar to web developers
✅ **Intuitive API** - Simple, readable syntax with sensible defaults
✅ **GTK-Native** - Uses GTK 4's native file chooser, no custom dialogs
✅ **Type-Safe** - Clean parameter passing with optional arguments
✅ **Composable** - Easy integration with gcompose widgets and state
✅ **Consistent** - Follows React/Svelte callback patterns

## Key Features

### File Filters

Define filters as list of dicts:

```python
filters = [
    {"name": "Text Files", "pattern": "*.txt"},
    {"name": "Images", "pattern": "*.png;*.jpg;*.gif"},
    {"name": "All Files", "pattern": "*"}
]
```

### Initial Paths

Set starting directory with `initial_folder` parameter:

```python
open_file(
    initial_folder="~/Documents",
    on_file=lambda path: ...
)
```

### Cancellation Handling

Optional `on_cancel` callback for user cancellations:

```python
FileDialog.open_file(
    on_file=lambda path: handle_success(path),
    on_cancel=lambda: print("User cancelled")
)
```

### Parent Windows

Modal dialogs with `parent_window` parameter:

```python
open_file(
    title="...",
    parent_window=my_gtk_window,
    on_file=lambda path: ...
)
```

## Integration with gcompose

### With State Binding

```python
from gcompose import *
from gcompose.state import use_state

state = use_state(file_path="")

def on_file_selected(path):
    state.file_path = path

open_file(on_file=on_file_selected)

Text(bind=Binding(state, "file_path", format=lambda v: f"File: {v}"))
```

### Complete Example

See [examples/file_dialogs_example.py](examples/file_dialogs_example.py) for full working application with:

- Multiple file selection
- File path display
- Status messages
- Icon integration

## Implementation Details

- **GTK 4** - Uses Gtk.FileChooserDialog
- **Gio Integration** - Robust path handling via Gio.File
- **Non-Blocking** - All dialogs are async via callbacks
- **Auto-Cleanup** - Dialogs automatically destroyed after interaction
- **Path Expansion** - Supports `~` in `initial_folder` via Path.expanduser()

## Benefits Over Direct GTK Usage

| Aspect         | Direct GTK             | Our Utility      |
| -------------- | ---------------------- | ---------------- |
| Code Length    | 40+ lines              | 3-5 lines        |
| Learning Curve | Steep                  | Flat             |
| Callback Style | Signals + Response IDs | Simple callbacks |
| Error Handling | Manual                 | Integrated       |
| Filter Syntax  | Complex                | Simple dicts     |
| Multiple Files | Different API          | Same API         |

## Files Exported from Main Module

```python
from gcompose import FileDialog, open_file, save_file, pick_folder
```

All utilities are immediately available after gcompose import.
