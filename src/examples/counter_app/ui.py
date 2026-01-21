from gcompose import *

def App():
    count, set_count = use_state(0)
    win = get_window_state()
    with Column(styles="p-4"):
        with HeaderBar():
            Text("Logo")
            Button("MIN", lambda: win.minimize())
            Button("MAX" if win.is_maximized() else "RES", lambda: win.toggle_maximize())
            Button("CLOSE", lambda: win.close())
        
        Text(f"Count: {count()}", styles="text-blue-400 text-2xl")

        with Row():
            Button("-", lambda: set_count(count() - 1), styles="bg-red-600")
            Button("+", lambda: set_count(count() + 1), styles="bg-green-600")
