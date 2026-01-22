import sys
import os

sys.path.insert(0, os.path.abspath("../../src"))
from gcompose import ComposeApp
from ui import App

app = ComposeApp(
    App,
    app_id="com.example.widgets",
    title="Widget Showcase",
    width=400,
    height=300,
)
app.run()
