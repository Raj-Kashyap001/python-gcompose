"""File dialog utilities with intuitive, web-framework-like syntax.

Provides simple abstractions over GTK 4 file chooser dialogs.

Examples:
    # Simple open file dialog
    FileDialog.open_file(
        title="Open Document",
        on_file=lambda path: print(f"Selected: {path}")
    )

    # Open multiple files
    FileDialog.open_file(
        title="Select Files",
        multiple=True,
        on_files=lambda paths: print(f"Selected {len(paths)} files")
    )

    # Save file with filters
    FileDialog.save_file(
        title="Save Document",
        filters=[
            {"name": "Text Files", "pattern": "*.txt"},
            {"name": "All Files", "pattern": "*"}
        ],
        on_file=lambda path: print(f"Save to: {path}")
    )

    # Pick a folder
    FileDialog.pick_folder(
        title="Select Folder",
        on_folder=lambda path: print(f"Folder: {path}")
    )
"""

import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gio
from pathlib import Path
from typing import Callable, Optional, List, Dict


class FileDialog:
    """High-level file dialog interface with intuitive API."""

    @staticmethod
    def open_file(
        title: str = "Open File",
        multiple: bool = False,
        filters: Optional[List[Dict[str, str]]] = None,
        on_file: Optional[Callable[[str], None]] = None,
        on_files: Optional[Callable[[List[str]], None]] = None,
        on_cancel: Optional[Callable[[], None]] = None,
        parent_window=None,
        initial_folder: Optional[str] = None,
    ) -> None:
        """Open a file selection dialog.

        Args:
            title: Dialog title
            multiple: Allow multiple file selection
            filters: List of dicts with "name" and "pattern" keys
            on_file: Callback for single file selection - called with file path
            on_files: Callback for multiple file selection - called with list of paths
            on_cancel: Callback when dialog is cancelled
            parent_window: Parent GTK window
            initial_folder: Initial folder path to open

        Example:
            FileDialog.open_file(
                title="Select Image",
                filters=[{"name": "Images", "pattern": "*.png;*.jpg"}],
                on_file=lambda path: print(f"Selected: {path}")
            )
        """
        dialog = Gtk.FileChooserDialog(
            title=title,
            action=Gtk.FileChooserAction.OPEN,
            transient_for=parent_window,
        )

        # Add buttons
        dialog.add_buttons(
            "Cancel",
            Gtk.ResponseType.CANCEL,
            "Open",
            Gtk.ResponseType.OK,
        )

        # Set multiple selection if requested
        dialog.set_select_multiple(multiple)

        # Add filters
        if filters:
            for filter_spec in filters:
                file_filter = Gtk.FileFilter()
                file_filter.set_name(filter_spec.get("name", "Unknown"))
                for pattern in filter_spec.get("pattern", "").split(";"):
                    file_filter.add_pattern(pattern.strip())
                dialog.add_filter(file_filter)

        # Set initial folder
        if initial_folder:
            path = Path(initial_folder).expanduser()
            if path.is_dir():
                dialog.set_current_folder(Gio.File.new_for_path(str(path)))

        def on_response(dialog, response_id):
            if response_id == Gtk.ResponseType.OK:
                if multiple and on_files:
                    files = dialog.get_files()
                    paths = [f.get_path() for f in files]
                    on_files(paths)
                elif on_file:
                    file = dialog.get_file()
                    if file:
                        on_file(file.get_path())
            elif response_id == Gtk.ResponseType.CANCEL and on_cancel:
                on_cancel()

            dialog.destroy()

        dialog.connect("response", on_response)
        dialog.present()

    @staticmethod
    def save_file(
        title: str = "Save File",
        filters: Optional[List[Dict[str, str]]] = None,
        on_file: Optional[Callable[[str], None]] = None,
        on_cancel: Optional[Callable[[], None]] = None,
        parent_window=None,
        initial_folder: Optional[str] = None,
        suggested_name: Optional[str] = None,
    ) -> None:
        """Open a file save dialog.

        Args:
            title: Dialog title
            filters: List of dicts with "name" and "pattern" keys
            on_file: Callback for file selection - called with file path
            on_cancel: Callback when dialog is cancelled
            parent_window: Parent GTK window
            initial_folder: Initial folder path to open
            suggested_name: Suggested filename

        Example:
            FileDialog.save_file(
                title="Save Document",
                suggested_name="document.txt",
                filters=[{"name": "Text Files", "pattern": "*.txt"}],
                on_file=lambda path: print(f"Save to: {path}")
            )
        """
        dialog = Gtk.FileChooserDialog(
            title=title,
            action=Gtk.FileChooserAction.SAVE,
            transient_for=parent_window,
        )

        # Add buttons
        dialog.add_buttons(
            "Cancel",
            Gtk.ResponseType.CANCEL,
            "Save",
            Gtk.ResponseType.OK,
        )

        # Add filters
        if filters:
            for filter_spec in filters:
                file_filter = Gtk.FileFilter()
                file_filter.set_name(filter_spec.get("name", "Unknown"))
                for pattern in filter_spec.get("pattern", "").split(";"):
                    file_filter.add_pattern(pattern.strip())
                dialog.add_filter(file_filter)

        # Set initial folder
        if initial_folder:
            path = Path(initial_folder).expanduser()
            if path.is_dir():
                dialog.set_current_folder(Gio.File.new_for_path(str(path)))

        # Set suggested filename
        if suggested_name:
            dialog.set_current_name(suggested_name)

        def on_response(dialog, response_id):
            if response_id == Gtk.ResponseType.OK and on_file:
                file = dialog.get_file()
                if file:
                    on_file(file.get_path())
            elif response_id == Gtk.ResponseType.CANCEL and on_cancel:
                on_cancel()

            dialog.destroy()

        dialog.connect("response", on_response)
        dialog.present()

    @staticmethod
    def pick_folder(
        title: str = "Select Folder",
        on_folder: Optional[Callable[[str], None]] = None,
        on_cancel: Optional[Callable[[], None]] = None,
        parent_window=None,
        initial_folder: Optional[str] = None,
    ) -> None:
        """Open a folder selection dialog.

        Args:
            title: Dialog title
            on_folder: Callback for folder selection - called with folder path
            on_cancel: Callback when dialog is cancelled
            parent_window: Parent GTK window
            initial_folder: Initial folder path to open

        Example:
            FileDialog.pick_folder(
                title="Select Project Folder",
                on_folder=lambda path: print(f"Folder: {path}")
            )
        """
        dialog = Gtk.FileChooserDialog(
            title=title,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            transient_for=parent_window,
        )

        # Add buttons
        dialog.add_buttons(
            "Cancel",
            Gtk.ResponseType.CANCEL,
            "Select",
            Gtk.ResponseType.OK,
        )

        # Set initial folder
        if initial_folder:
            path = Path(initial_folder).expanduser()
            if path.is_dir():
                dialog.set_current_folder(Gio.File.new_for_path(str(path)))

        def on_response(dialog, response_id):
            if response_id == Gtk.ResponseType.OK and on_folder:
                file = dialog.get_file()
                if file:
                    on_folder(file.get_path())
            elif response_id == Gtk.ResponseType.CANCEL and on_cancel:
                on_cancel()

            dialog.destroy()

        dialog.connect("response", on_response)
        dialog.present()


# Convenience functions (shorter API)
def open_file(
    title: str = "Open File",
    on_file: Callable[[str], None] = None,
    filters: Optional[List[Dict[str, str]]] = None,
    initial_folder: Optional[str] = None,
    parent_window=None,
) -> None:
    """Convenience function to open a single file.

    If parent_window is not provided, auto-detects the active GTK window.

    Example:
        open_file(
            title="Select File",
            on_file=lambda path: print(f"Selected: {path}")
        )
    """
    # Auto-detect parent window if not provided
    if parent_window is None:
        app = Gtk.Application.get_default()
        if app and app.get_windows():
            parent_window = app.get_windows()[0]

    FileDialog.open_file(
        title=title,
        multiple=False,
        filters=filters,
        on_file=on_file,
        initial_folder=initial_folder,
        parent_window=parent_window,
    )


def save_file(
    title: str = "Save File",
    on_file: Callable[[str], None] = None,
    filters: Optional[List[Dict[str, str]]] = None,
    initial_folder: Optional[str] = None,
    suggested_name: Optional[str] = None,
    parent_window=None,
) -> None:
    """Convenience function to save a file.

    If parent_window is not provided, auto-detects the active GTK window.

    Example:
        save_file(
            title="Save Document",
            suggested_name="document.txt",
            on_file=lambda path: print(f"Save to: {path}")
        )
    """
    # Auto-detect parent window if not provided
    if parent_window is None:
        app = Gtk.Application.get_default()
        if app and app.get_windows():
            parent_window = app.get_windows()[0]

    FileDialog.save_file(
        title=title,
        filters=filters,
        on_file=on_file,
        initial_folder=initial_folder,
        suggested_name=suggested_name,
        parent_window=parent_window,
    )


def pick_folder(
    title: str = "Select Folder",
    on_folder: Callable[[str], None] = None,
    initial_folder: Optional[str] = None,
    parent_window=None,
) -> None:
    """Convenience function to pick a folder.

    If parent_window is not provided, auto-detects the active GTK window.

    Example:
        pick_folder(
            title="Select Project",
            on_folder=lambda path: print(f"Folder: {path}")
        )
    """
    # Auto-detect parent window if not provided
    if parent_window is None:
        app = Gtk.Application.get_default()
        if app and app.get_windows():
            parent_window = app.get_windows()[0]

    FileDialog.pick_folder(
        title=title,
        on_folder=on_folder,
        initial_folder=initial_folder,
        parent_window=parent_window,
    )


__all__ = ["FileDialog", "open_file", "save_file", "pick_folder"]
