from gcompose import *

"""Counter Application"""

def App():
    count, set_count = use_state(0)
    with Column(styles="w-full h-full justify-start items-end p-4"):
        Text(f"Count: {count()}", styles="text-blue-400 text-2xl")

        with Row(styles="mt-2"):
            Button("Increment", lambda: set_count(count() + 1), styles="bg-green-600", icon='list-add')
            Button("Decrement", lambda: set_count(count() - 1), styles="bg-red-600", icon='list-remove')
