import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gio, GObject
from tinytag import TinyTag


class MusicPlayer(GObject.Object):
    def __init__(self):
        super().__init__()
        self.media = None
        self.current_song_path = None

    def open_file_picker(self, parent_window, callback):
        """
        Utility to trigger the system file dialog.
        callback: function(path, metadata)
        """
        dialog = Gtk.FileDialog.new()
        dialog.set_title("Select Audio File")

        # Audio filters
        filter_audio = Gtk.FileFilter()
        filter_audio.set_name("Audio Files")
        filter_audio.add_mime_type("audio/*")
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(filter_audio)
        dialog.set_filters(filters)

        # Async call to open
        dialog.open(parent_window, None, self._on_file_selected, callback)

    def _on_file_selected(self, dialog, result, callback):
        try:
            file = dialog.open_finish(result)
            if file:
                path = file.get_path()
                self.load_and_play(path)

                # Extract metadata
                metadata = TinyTag.get(path)

                if callback:
                    callback(path, metadata)
        except Exception as e:
            print(f"File selection error: {e}")

    def load_and_play(self, path):
        """Stops current stream and starts a new file."""
        if self.media:
            self.media.set_playing(False)

        self.current_song_path = path
        file = Gio.File.new_for_path(path)
        self.media = Gtk.MediaFile.new_for_file(file)
        self.media.set_playing(True)

    def toggle_play(self):
        """Toggles between play and pause. Returns the new state."""
        if self.media:
            new_state = not self.media.get_playing()
            self.media.set_playing(new_state)
            return new_state
        return False


# --- Instance creation ---
# This is the object you will import in your other files
audio_player = MusicPlayer()
