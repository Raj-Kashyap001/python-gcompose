"""
Comprehensive Widget Showcase
Demonstrates all gcompose widgets including new ones:
- Input (text entry)
- Checkbox
- Switch (toggle)
- Select (dropdown)
- Spacer
- Separator
- ScrollColumn/ScrollRow (scrollable containers)
- Hover effects in styles
"""

from gcompose import *
from gcompose.state import use_state


def App():
    """Main widget showcase with responsive scrollable layout"""
    state = use_state(
        name="",
        email="",
        terms_accepted=False,
        newsletter=True,
        country="",
        feedback="",
        progress=0.5,
    )

    # Use ScrollColumn for main content - scrollable and responsive
    with ScrollColumn(spacing=16):
        # ===== Header with Padding =====
        with Column(spacing=0, styles="p-6"):
            with Row(spacing=8, styles="items-center"):
                Text("Widget Showcase", styles="text-2xl font-bold")
                Spacer(flex=True)
                Button("Help", styles="hover:bg-blue-100")

            Separator(orientation="horizontal")

        # ===== Content sections with padding =====
        with Column(spacing=16, styles="p-6"):
            # ===== Text Input Section =====
            Text("Text Input", styles="text-xl font-semibold")
            with Column(spacing=8):
                Input(
                    placeholder="Enter your name",
                    value=state.name,
                    on_change=lambda v: setattr(state, "name", v),
                    styles="hover:bg-gray-100",
                )
                Input(
                    placeholder="Enter email",
                    input_type="email",
                    on_change=lambda v: setattr(state, "email", v),
                    styles="hover:bg-gray-100",
                )
                Input(
                    placeholder="Password",
                    input_type="password",
                    styles="hover:bg-gray-100",
                )

            Separator(orientation="horizontal")

            # ===== Checkbox & Switch Section =====
            Text("Checkboxes & Switches", styles="text-xl font-semibold")
            with Column(spacing=8):
                Checkbox(
                    label="I agree to terms",
                    checked=state.terms_accepted,
                    on_toggle=lambda checked: setattr(state, "terms_accepted", checked),
                )
                with Row(spacing=8, styles="items-center"):
                    Text("Newsletter subscription:")
                    Spacer(flex=True)
                    Switch(
                        active=state.newsletter,
                        on_toggled=lambda active: setattr(state, "newsletter", active),
                    )

            Separator(orientation="horizontal")

            # ===== Select/Dropdown Section =====
            Text("Select Dropdown", styles="text-xl font-semibold")
            with Column(spacing=8):
                Text("Choose your country:", styles="text-sm text-gray-600")
                Select(
                    items=["USA", "Canada", "Mexico", "UK", "Australia"],
                    selected_index=0,
                    on_change=lambda item: setattr(state, "country", item),
                    styles="w-full",
                )

            Separator(orientation="horizontal")

            # ===== Progress Section =====
            Text("Progress Bar", styles="text-xl font-semibold")
            ProgressBar(fraction=0.65, show_text=True, text="65%")

            # ===== List Section =====
            Text("List Example", styles="text-xl font-semibold")
            with ScrollColumn(
                spacing=0, styles="h-200 border-2 border-gray-300 rounded"
            ):
                List(
                    items=["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6"],
                    selection_mode="single",
                    styles="",
                )

            Separator(orientation="horizontal")

            # ===== TextArea Section =====
            Text("Text Area (Scrollable)", styles="text-xl font-semibold")
            TextArea(
                value="Share your feedback here...",
                on_change=lambda text: setattr(state, "feedback", text),
                styles="h-150 hover:bg-blue-50",
            )

        # ===== Footer with Padding =====
        with Column(spacing=0, styles="p-6"):
            Separator(orientation="horizontal")

            with Row(spacing=8, styles="justify-end"):
                Button("Cancel", styles="bg-gray-200 hover:bg-gray-300")
                Button("Submit", styles="bg-blue-500 text-white hover:bg-blue-600")
