from gcompose import *

"""Counter Application"""

def App(styles="w-full h-full justify-center items-center p-4"):
    count, set_count = use_state(0)
    with Column():
        Text(f"Count: {count()}", styles="text-blue-400 text-2xl")

        with Row():
            Button("Increment", lambda: set_count(count() + 1), styles="bg-green-600", icon='list-add')
            Button("Decrement", lambda: set_count(count() - 1), styles="bg-red-600 p-4 text-lg", icon='list-remove', icon_position="end", icon_layout='horizontal', icon_gap=24)
