from gcompose import *
from gi.repository import GObject

"""Counter Application"""


class CounterState(GObject.Object):
    count = GObject.Property(type=int, default=0)

    def increment(self):
        self.count += 1

    def decrement(self):
        if self.count > 0:
            self.count -= 1


def App():
    state = CounterState()

    with Column(styles="w-full h-full justify-center items-center p-4"):
        label = Text("", styles="text-blue-400 text-2xl")
        state.bind_property(
            "count",
            label,
            "label",
            GObject.BindingFlags.DEFAULT | GObject.BindingFlags.SYNC_CREATE,
            lambda binding, value: f"Count: {value}",
        )

        with Row(styles="mt-2"):
            Button(
                "Increment",
                lambda: state.increment(),
                styles="bg-green-600",
                icon="list-add",
            )
            Button(
                "Decrement",
                lambda: state.decrement(),
                styles="bg-red-600",
                icon="list-remove",
            )
