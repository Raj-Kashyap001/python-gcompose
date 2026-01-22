from gcompose import *


"""Counter Application"""

from gcompose.state import use_state


def App():
    state = use_state(count=0)

    def increment():
        state.count += 1

    def decrement():
        if state.count > 0:
            state.count -= 1

    with Column(styles="w-full h-full justify-center items-center p-4"):
        Text(
            bind=Binding(state, "count", format=lambda value: f"Count: {value}"),
            styles="text-blue-400 text-2xl",
        )

        with Row(styles="mt-2"):
            Button(
                "Increment",
                lambda: increment(),
                styles="bg-green-600",
                icon="list-add",
            )
            Button(
                "Decrement",
                lambda: decrement(),
                styles="bg-red-600",
                icon="list-remove",
            )
