from gcompose import *

def App():
    count, set_count = use_state(0)
    with Column(styles="p-4"):
        Text(f"Count: {count()}", styles="text-blue-400 text-2xl")

        with Row():
            Button("-", lambda: set_count(count() - 1), styles="bg-red-600")
            Button("+", lambda: set_count(count() + 1), styles="bg-green-600")
