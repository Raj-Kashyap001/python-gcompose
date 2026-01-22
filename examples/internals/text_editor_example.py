"""
Practical Example - Simple Text Editor with File Operations

Demonstrates:
- TextArea widget for text editing
- File dialogs for open/save
- State management with Binding
- Practical application of file utilities
"""

import sys
import os

sys.path.insert(0, os.path.abspath("../../src"))
from gcompose import *
from gcompose.state import use_state

from gcompose import ComposeApp


def TextEditor():
    """Simple text editor app using file dialogs and TextArea."""

    state = use_state(
        current_file="Untitled",
        file_path="",
        status="Ready",
    )

    # Keep reference to textarea widget for direct access
    textarea_widget = None

    def new_file():
        # Clear textarea by directly clearing the buffer
        if textarea_widget:
            buf = textarea_widget.get_buffer()
            buf.set_text("")
        state.current_file = "Untitled"
        state.file_path = ""
        state.status = "New file created"

    def open_file_dialog():
        from gcompose import open_file

        open_file(
            title="Open Text File",
            filters=[
                {"name": "Text Files", "pattern": "*.txt"},
                {"name": "Python Files", "pattern": "*.py"},
                {"name": "All Files", "pattern": "*"},
            ],
            on_file=lambda path: load_file(path),
        )

    def load_file(path):
        try:
            with open(path, "r") as f:
                content = f.read()
                # Directly update the textarea widget buffer
                if textarea_widget:
                    buf = textarea_widget.get_buffer()
                    buf.set_text(content)
            state.current_file = path.split("/")[-1]
            state.file_path = path
            state.status = f"Opened: {state.current_file}"
        except Exception as e:
            state.status = f"Error opening file: {str(e)}"

    def save_file_dialog():
        from gcompose import save_file

        save_file(
            title="Save Text File",
            suggested_name=(
                state.current_file
                if state.current_file != "Untitled"
                else "document.txt"
            ),
            filters=[
                {"name": "Text Files", "pattern": "*.txt"},
                {"name": "Python Files", "pattern": "*.py"},
                {"name": "All Files", "pattern": "*"},
            ],
            on_file=lambda path: save_file_to(path),
        )

    def save_file_to(path):
        try:
            # Read text directly from TextArea widget
            if textarea_widget:
                text_content = textarea_widget.get_text()
            else:
                text_content = ""

            with open(path, "w") as f:
                f.write(text_content)
                state.current_file = path.split("/")[-1]
                state.file_path = path
                state.status = f"Saved: {state.current_file}"
        except Exception as e:
            state.status = f"Error saving file: {str(e)}"

    with Column(styles="w-full h-full bg-gray-900"):
        # Toolbar
        with Row(styles="bg-gray-800 p-2 gap-2 border-b border-gray-700"):
            Button("New", new_file, icon="document-new", styles="bg-blue-600")
            Button(
                "Open", open_file_dialog, icon="document-open", styles="bg-green-600"
            )
            Button(
                "Save", save_file_dialog, icon="document-save", styles="bg-orange-600"
            )

        # Editor area - TextArea with direct widget access
        with Column(styles="flex-1"):
            textarea_widget = TextArea(
                value="",
                on_change=lambda text: setattr(
                    state, "status", f"{len(text)} characters"
                ),
                styles="bg-gray-950 text-gray-100 p-3 font-mono text-sm",
                editable=True,
            )

        # Status bar
        Text(
            bind=Binding(
                state,
                "status",
                format=lambda v: f"* {state.current_file} | {v}",
            ),
            styles="bg-gray-800 p-2 text-xs text-gray-500 border-t border-gray-700",
        )


app = ComposeApp(
    TextEditor,
    app_id="com.example.text_editor_app",
    title="TextEditor App",
    width=800,
    height=600,
)
app.run()
