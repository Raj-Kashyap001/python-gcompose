"""
Style parser for extracting programmatic properties from CSS-like style strings.
GTK doesn't support width, height, justify-content, align-items in CSS, so we parse
these out and apply them using widget methods.
"""

import re
from typing import Dict, Tuple, Optional

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw


class StyleParser:
    """Parses style strings to extract properties that need programmatic application."""

    # Size properties: w-{value}, h-{value}
    SIZE_PATTERN = re.compile(r"\b(w|h)-(\d+|full|auto|min|max)\b")

    # Alignment properties: justify-{value}, items-{value}
    ALIGN_PATTERN = re.compile(
        r"\b(justify|items)-(start|center|end|stretch|space-between|space-around|space-evenly)\b"
    )

    # Text alignment properties: text-{left|center|right}
    TEXT_PATTERN = re.compile(r"\btext-(left|center|right)\b")

    @staticmethod
    def parse_size_properties(styles: str) -> Tuple[Dict[str, str], str]:
        """
        Extract width/height properties from style string.

        Returns:
            Tuple of (parsed_properties dict, remaining_styles string)
        """
        if not styles:
            return {}, ""

        parsed = {}
        remaining_parts = []

        for part in styles.split():
            match = StyleParser.SIZE_PATTERN.match(part)
            if match:
                prop_type, value = match.groups()
                if prop_type == "w":
                    parsed["width"] = value
                elif prop_type == "h":
                    parsed["height"] = value
            else:
                remaining_parts.append(part)

        return parsed, " ".join(remaining_parts)

    @staticmethod
    def parse_alignment_properties(styles: str) -> Tuple[Dict[str, str], str]:
        """
        Extract justify-content/align-items and text-align properties from style string.

        Returns:
            Tuple of (parsed_properties dict, remaining_styles string)
        """
        if not styles:
            return {}, ""

        parsed = {}
        remaining_parts = []

        for part in styles.split():
            match = StyleParser.ALIGN_PATTERN.match(part)
            if match:
                prop_type, value = match.groups()
                if prop_type == "justify":
                    parsed["justify_content"] = value
                elif prop_type == "items":
                    parsed["align_items"] = value
            else:
                text_match = StyleParser.TEXT_PATTERN.match(part)
                if text_match:
                    parsed["text_align"] = text_match.group(1)
                else:
                    remaining_parts.append(part)

        return parsed, " ".join(remaining_parts)

    @staticmethod
    def parse_all_properties(styles: str) -> Tuple[Dict[str, str], str]:
        """
        Parse all programmatic properties (size and alignment) from style string.

        Returns:
            Tuple of (parsed_properties dict, remaining_styles string)
        """
        if not styles:
            return {}, styles

        # print(f"DEBUG: Parsing styles: '{styles}'")

        # Parse size properties first
        size_props, remaining = StyleParser.parse_size_properties(styles)
        # print(f"DEBUG: Size properties: {size_props}, remaining: '{remaining}'")

        # Then parse alignment properties from remaining
        align_props, final_remaining = StyleParser.parse_alignment_properties(remaining)
        # print(f"DEBUG: Alignment properties: {align_props}, final remaining: '{final_remaining}'")

        # Combine all parsed properties
        all_props = {**size_props, **align_props}
        # print(f"DEBUG: All parsed properties: {all_props}")

        return all_props, final_remaining


def parse_size_value(value: str) -> Optional[int]:
    """
    Convert size value to pixels. Returns None for 'auto' or invalid values.
    Special handling for 'full' which means expand to fill.
    """
    if value == "auto":
        return None
    elif value == "full":
        return -1  # Special marker for full expansion
    elif value in ("min", "max"):
        # For now, treat as auto
        return None
    else:
        try:
            # Assume numeric values are pixels for now
            return int(value)
        except ValueError:
            return None


def apply_size_properties(widget, properties: Dict[str, str]):
    """Apply width/height properties to a GTK widget."""
    width = properties.get("width")
    height = properties.get("height")

    # print(f"DEBUG: Applying size properties: width={width}, height={height}")

    # Check if this is a container (Box)
    is_container = hasattr(widget, "get_orientation")

    if width is not None:
        width_px = parse_size_value(width)
        if width == "full":
            # print("DEBUG: Setting width to full - enabling hexpand")
            widget.set_hexpand(True)
            # Only set FILL alignment for non-containers
            if not is_container:
                # print("DEBUG: Setting halign FILL for non-container")
                widget.set_halign(Gtk.Align.FILL)
        elif width_px is not None and width_px >= 0:
            print(f"DEBUG: Setting width to {width_px}px")
            widget.set_size_request(width_px, -1)

    if height is not None:
        height_px = parse_size_value(height)
        if height == "full":
            # print("DEBUG: Setting height to full - enabling vexpand")
            widget.set_vexpand(True)
            # Only set FILL alignment for non-containers
            if not is_container:
                # print("DEBUG: Setting valign FILL for non-container")
                widget.set_valign(Gtk.Align.FILL)
        elif height_px is not None and height_px >= 0:
            # print(f"DEBUG: Setting height to {height_px}px")
            current_width = widget.get_size_request()[0]
            widget.set_size_request(current_width, height_px)


def apply_alignment_properties(widget, properties: Dict[str, str]):
    # """Apply justify-content/align-items and text-align properties to a GTK widget."""
    justify = properties.get("justify_content")
    align = properties.get("align_items")
    text_align = properties.get("text_align")

    # print(f"DEBUG: Applying alignment properties: justify={justify}, align={align}")

    # For GTK Box containers, set alignment on the container itself
    if hasattr(widget, "get_orientation") or isinstance(
        widget, Adw.NavigationSplitView
    ):
        if isinstance(widget, Adw.NavigationSplitView):
            # Handle Adw.NavigationSplitView alignment
            if justify == "start":
                widget.set_halign(Gtk.Align.START)
            elif justify == "center":
                widget.set_halign(Gtk.Align.CENTER)
            elif justify == "end":
                widget.set_halign(Gtk.Align.END)

            if align == "start":
                widget.set_valign(Gtk.Align.START)
            elif align == "center":
                widget.set_valign(Gtk.Align.CENTER)
            elif align == "end":
                widget.set_valign(Gtk.Align.END)
            elif align == "stretch":
                widget.set_valign(Gtk.Align.FILL)
        else:
            orientation = widget.get_orientation()
            # print(f"DEBUG: Widget is a Box with orientation: {orientation}")

            if orientation == Gtk.Orientation.HORIZONTAL:
                # For horizontal boxes (Row)
                if justify == "start":
                    # print("DEBUG: Setting horizontal box halign to START")
                    widget.set_halign(Gtk.Align.START)
                elif justify == "center":
                    # print("DEBUG: Setting horizontal box halign to CENTER")
                    widget.set_halign(Gtk.Align.CENTER)
                elif justify == "end":
                    # print("DEBUG: Setting horizontal box halign to END")
                    widget.set_halign(Gtk.Align.END)

                # align-items affects vertical alignment of the box
                if align == "start":
                    widget.set_valign(Gtk.Align.START)
                elif align == "center":
                    widget.set_valign(Gtk.Align.CENTER)
                elif align == "end":
                    widget.set_valign(Gtk.Align.END)
                elif align == "stretch":
                    widget.set_valign(Gtk.Align.FILL)

            elif orientation == Gtk.Orientation.VERTICAL:
                # For vertical boxes (Column)
                if justify == "start":
                    # print("DEBUG: Setting vertical box valign to START")
                    widget.set_valign(Gtk.Align.START)
                elif justify == "center":
                    # print("DEBUG: Setting vertical box valign to CENTER")
                    widget.set_valign(Gtk.Align.CENTER)
                elif justify == "end":
                    # print("DEBUG: Setting vertical box valign to END")
                    widget.set_valign(Gtk.Align.END)

                # align-items affects horizontal alignment of the box
                if align == "start":
                    widget.set_halign(Gtk.Align.START)
                elif align == "center":
                    # print("DEBUG: Setting vertical box halign to CENTER for items-center")
                    widget.set_halign(Gtk.Align.CENTER)
                elif align == "end":
                    widget.set_halign(Gtk.Align.END)
                elif align == "stretch":
                    widget.set_halign(Gtk.Align.FILL)

    # For non-container widgets, apply basic alignment
    else:
        print(f"DEBUG: Widget is not a Box container: {widget}")
        if hasattr(widget, "set_halign"):
            if justify == "start":
                # print("DEBUG: Setting widget halign to START")
                widget.set_halign(Gtk.Align.START)
            elif justify == "center":
                # print("DEBUG: Setting widget halign to CENTER")
                widget.set_halign(Gtk.Align.CENTER)
            elif justify == "end":
                print("DEBUG: Setting widget halign to END")
                widget.set_halign(Gtk.Align.END)

        if hasattr(widget, "set_valign"):
            if align == "start":
                # print("DEBUG: Setting widget valign to START")
                widget.set_valign(Gtk.Align.START)
            elif align == "center":
                # print("DEBUG: Setting widget valign to CENTER")
                widget.set_valign(Gtk.Align.CENTER)
            elif align == "end":
                # print("DEBUG: Setting widget valign to END")
                widget.set_valign(Gtk.Align.END)
            elif align == "stretch":
                # print("DEBUG: Setting widget valign to FILL")
                widget.set_valign(Gtk.Align.FILL)

    # Handle text alignment for labels
    if text_align and hasattr(widget, "set_xalign"):
        if text_align == "left":
            widget.set_xalign(0.0)
        elif text_align == "center":
            widget.set_xalign(0.5)
        elif text_align == "right":
            widget.set_xalign(1.0)
