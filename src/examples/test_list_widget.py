#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.abspath("../.."))

from gcompose import ComposeApp
from gcompose.widgets.basic import List, Text


def on_item_selected(item):
    print(f"Selected item: {item}")


def App():
    Text("List Widget Test", styles="title")

    # Test with no selection
    Text("List with no selection:", styles="subtitle")
    List(["Item 1", "Item 2", "Item 3"], styles="list-no-selection")

    # Test with single selection
    Text("List with single selection:", styles="subtitle")
    List(
        ["Option A", "Option B", "Option C"],
        selection_mode="single",
        on_select=on_item_selected,
        styles="list-single-selection",
    )

    # Test with multiple selection
    Text("List with multiple selection:", styles="subtitle")
    List(
        ["Choice 1", "Choice 2", "Choice 3", "Choice 4"],
        selection_mode="multiple",
        styles="list-multiple-selection",
    )


app = ComposeApp(
    App,
    app_id="com.example.gcompose_list_test",
    title="List Widget Test",
    width=400,
    height=600,
)
app.run()
