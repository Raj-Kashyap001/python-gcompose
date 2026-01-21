import sys
import os
sys.path.insert(0, os.path.abspath('../..'))
from gcompose import ComposeApp
from ui import App

app = ComposeApp(App, app_id="com.example.gcompose.v1")
app.run()
