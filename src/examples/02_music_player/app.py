import sys
import os

sys.path.insert(0, os.path.abspath("../.."))
from gcompose import ComposeApp
from ui import App

app = ComposeApp(
    App,
    app_id="com.gcompose.music_player",
    title="Music Player",
    width=800,
    height=600,
)
app.run()
