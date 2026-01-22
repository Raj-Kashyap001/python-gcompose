"""
gcompose public API

v1 exposes only the minimal primitives needed to build
simple declarative GTK applications.
"""

from .app.app import ComposeApp

from .compose.runtime import Composable
from .compose.window_state import get_window_state

from .layout.box import Row, Column, ScrollRow, ScrollColumn, HeaderBar
from .widgets.basic import (
    Text,
    Button,
    Image,
    ProgressBar,
    List,
    TextArea,
    Input,
    Checkbox,
    Switch,
    Select,
    Spacer,
    Separator,
)
from .widgets.sidebar import SidebarLayout, SidebarContent, SidebarMainScreen
from .state import Binding
from .utils import FileDialog, open_file, save_file, pick_folder
