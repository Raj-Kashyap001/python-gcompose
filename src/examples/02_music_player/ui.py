from gcompose import *

"""Simple Music Player"""


def App():
    with SidebarLayout(styles="h-full"):
        sidebar_content()
        main_screen_content()


def sidebar_content():
    with SidebarContent():
        with Column(styles="p-4 w-md h-full"):
            # Header
            Text("Music Library", styles="text-lg font-bold mb-4")

            # Action buttons
            with Row(styles="mb-4"):
                Button("Import", icon="document-open", styles="mr-2 flex-none")
                Button("Open", icon="folder-open", styles="flex-none")

            # Music list placeholder
            Text("Songs:", styles="text-md font-semibold mb-2")
            with Column(styles="bg-gray-100 p-2 rounded"):
                Text("TheFatRat - Xenogenesis (Outro Song).mp3", styles="text-sm")
                # Add more songs here


def main_screen_content():
    with SidebarMainScreen():
        with Column(styles="p-4 items-center justify-center h-full w-full"):
            # Album art placeholder
            with Row(styles="mb-8 justify-center"):
                # Placeholder for album art - using a large button as placeholder
                Button("", icon="media-optical", styles="bg-gray-200")

            # Demo Song info
            Text(
                "TheFatRat - Xenogenesis (Outro Song)",
                styles="text-xl font-bold mb-2 text-center",
            )
            Text("Now Playing", styles="text-gray-600 mb-8 text-center")

            # Player controls
            with Row(styles="items-center justify-center"):
                Button("", icon="media-skip-backward", styles="mr-4")
                Button("", icon="media-playback-start", styles="mr-4")
                Button("", icon="media-skip-forward", styles="mr-4")

            # Progress bar placeholder
            with Row(styles="w-full max-w-md mt-4"):
                # Simple progress indicator
                Text("0:00 / 3:45", styles="text-sm text-gray-600")
