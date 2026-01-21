from .runtime import Composition

class State:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

    def set(self, new_value):
        self.value = new_value
        Composition.rerender()


def use_state(initial):
    state = Composition.next_hook()
    if state is None:
        state = State(initial)
        Composition.set_hook(state)
    return state.get, state.set
