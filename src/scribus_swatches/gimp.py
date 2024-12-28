import io
from pathlib import Path
from typing import BinaryIO

from colormath.color_objects import sRGBColor

from .palette import Palette, PaletteWriter


class GIMPWriter(PaletteWriter):
    accepted_spaces = [sRGBColor]

    @staticmethod
    def format_filepath(filepath: Path) -> Path:
        """
        Ensure the filepath ends with the .gpl extension.

        Args:
            filepath (Path): The original file path.

        Returns:
            Path: The file path with the .gpl extension.
        """
        if filepath.suffix == ".gpl":
            return filepath
        return filepath.with_suffix(".gpl")

    @staticmethod
    def write(f: BinaryIO, palette: Palette):
        """
        Write the colors to a GIMP Palette file.

        Args:
            file (str or file-like object): The file path or file object where
                        the GIMP Palette data will be written.
            palette (Palette): The palette object containing the colors to write.

        Raises:
            ValueError: If an unsupported color type is encountered.

        The GIMP Palette file format is a simple text format where each color
        is represented as a line with the color values separated by spaces.
        The first line of the file is a header with the number of colors in
        the palette.
        """
        ft = io.TextIOWrapper(f, encoding="utf-8")
        ft.write("GIMP Palette\n")
        name = ft.name.split("/")[-1].split(".")[0]
        ft.write(f"Name: {name}\n")
        ft.write("#\n")
        # f.write(f"{len(palette.colors)}\n")
        for name, color in palette.colors:
            if isinstance(color, sRGBColor):
                r, g, b = color.get_upscaled_value_tuple()
                ft.write(f"{r:3d} {g:3d} {b:3d} {name}\n")
            else:
                raise ValueError(f"Unsupported color type: {type(color)}")
