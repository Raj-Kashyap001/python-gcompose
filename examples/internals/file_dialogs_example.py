"""
File Dialogs Example - Demonstrates the file operation utilities

Shows how to use open_file, save_file, and pick_folder with intuitive syntax.
"""

import sys
import os

sys.path.insert(0, os.path.abspath("../../src"))
from gcompose import *
from gcompose.state import use_state

from gcompose import ComposeApp


def App():
    state = use_state(current_file="", status_message="Ready", last_action="")

    def on_open_file():
        open_file(
            title="Open Document",
            filters=[
                {"name": "Text Files", "pattern": "*.txt"},
                {"name": "Python Files", "pattern": "*.py"},
                {"name": "All Files", "pattern": "*"},
            ],
            on_file=lambda path: (
                setattr(state, "current_file", path),
                setattr(state, "status_message", f"Opened: {path}"),
            ),
        )

    def on_save_file():
        save_file(
            title="Save Document",
            suggested_name="document.txt",
            filters=[
                {"name": "Text Files", "pattern": "*.txt"},
                {"name": "All Files", "pattern": "*"},
            ],
            on_file=lambda path: (
                setattr(state, "status_message", f"Saved to: {path}"),
            ),
        )

    def on_pick_project():
        pick_folder(
            title="Select Project Folder",
            on_folder=lambda path: (
                setattr(state, "status_message", f"Project: {path}"),
            ),
        )

    def on_open_multiple():
        FileDialog.open_file(
            title="Select Multiple Files",
            multiple=True,
            filters=[
                {"name": "Images", "pattern": "*.png;*.jpg;*.gif"},
                {"name": "All Files", "pattern": "*"},
            ],
            on_files=lambda paths: (
                setattr(state, "status_message", f"Selected {len(paths)} files"),
            ),
            on_cancel=lambda: setattr(state, "status_message", "Selection cancelled"),
        )

    with Column(styles="w-full h-full p-8 justify-start gap-4"):
        Text("File Operations Example", styles="text-3xl font-bold")

        # Status display
        Text(
            bind=Binding(state, "status_message", format=lambda v: f"Status: {v}"),
            styles="text-lg text-blue-400 mt-4",
        )

        # File path display
        Text(
            bind=Binding(
                state, "current_file", format=lambda v: f"Current: {v or 'None'}"
            ),
            styles="text-sm text-gray-400 mt-2",
        )

        # Button group
        with Row(styles="gap-4 mt-8"):
            Button(
                "Open File",
                on_open_file,
                styles="bg-blue-600 hover:bg-blue-700",
                icon="document-open",
            )
            Button(
                "Save File",
                on_save_file,
                styles="bg-green-600 hover:bg-green-700",
                icon="document-save",
            )
            Button(
                "Pick Folder",
                on_pick_project,
                styles="bg-purple-600 hover:bg-purple-700",
                icon="folder",
            )
            Button(
                "Multiple Files",
                on_open_multiple,
                styles="bg-orange-600 hover:bg-orange-700",
                icon="edit-select-all",
            )


app = ComposeApp(
    App,
    app_id="com.example.filedialogexample",
    title="file dialog example",
    width=400,
    height=300,
)
app.run()
