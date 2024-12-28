import re
from typing import TextIO

from colormath.color_objects import sRGBColor

from .palette import Palette, PaletteReader


class ReasonableColorsReader(PaletteReader):
    @staticmethod
    def convert(f: TextIO) -> Palette:
        palette = Palette()
        color_pattern = re.compile(
            r"\$color-([\w-]+):\s*rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)"
        )
        for line in f:
            match = color_pattern.match(line)
            if match:
                name, r, g, b = match.groups()
                color = sRGBColor(int(r), int(g), int(b), is_upscaled=True)
                palette.add_color(name, color)
        return palette
