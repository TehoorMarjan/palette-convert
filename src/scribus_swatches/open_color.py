import json
from typing import TextIO

from colormath.color_objects import sRGBColor

from .palette import Palette, PaletteReader


class OpenColorReader(PaletteReader):
    @staticmethod
    def convert(f: TextIO) -> Palette:
        data = json.load(f)
        palette = Palette()

        for color_name, color_values in data.items():
            if isinstance(color_values, list):
                for index, color_value in enumerate(color_values, start=1):
                    color = sRGBColor.new_from_rgb_hex(color_value)
                    palette.add_color(f"{color_name}-{index}", color)
            else:
                color = sRGBColor.new_from_rgb_hex(color_values)
                palette.add_color(color_name, color)

        return palette
