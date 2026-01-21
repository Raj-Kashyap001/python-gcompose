import gi
import sys
from tinytag import TinyTag

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gio, Adw, GLib

song_path = "Elektronomia - The Sky High [NCS Release].mp3"


def print_song_info(path):
    try:
        tag = TinyTag.get(path)
        print("--- Song Information ---")
        print(f"Title:  {tag.title}")
        print(f"Artist: {tag.artist}")
        print(f"Album:  {tag.album}")
        print(f"Length: {tag.duration:.2f} seconds")
        print("------------------------")
    except Exception as e:
        print(f"Could not read metadata: {e}")


class MusicApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.example.MusicPlayer")

    def do_activate(self):
        # 1. Print Metadata
        print_song_info(song_path)

        # 2. Setup Playback
        file = Gio.File.new_for_path(song_path)
        self.media = Gtk.MediaFile.new_for_file(file)

        # 3. Play
        print("Playing audio... (Close the window to stop)")
        self.media.set_playing(True)

        # 4. We need a window to keep the application alive
        window = Adw.ApplicationWindow(application=self)
        window.set_title("Audio Player")
        window.set_default_size(300, 100)

        # Simple UI to show it's working
        status = Adw.StatusPage(title="Now Playing", description=song_path)
        window.set_content(status)
        window.present()


app = MusicApp()
app.run(sys.argv)
