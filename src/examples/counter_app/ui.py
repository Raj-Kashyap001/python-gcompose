from gcompose import *

def App():
    count, set_count = use_state(0)
    with Column():
        Text(f"Count: {count()}")

        with Row():
            Button("-", lambda: set_count(count() - 1))
            Button("+", lambda: set_count(count() + 1))
