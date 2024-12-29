from pathlib import Path
from typing import (
    Any,
    BinaryIO,
    List,
    NamedTuple,
    Optional,
    TextIO,
    Type,
    Union,
)

import colormath
from colormath.color_conversions import convert_color
from colormath.color_objects import ColorBase


class Palette:
    """
    A class to manage a collection of colors.
    """

    def __init__(self):
        self.colors: list[PaletteColor] = []

    def add_color(self, name: str, color: ColorBase):
        """
        Adds a color to the swatch list.

        Args:
            name (str): The name of the color.
            color (ColorBase): The color object to add. It can be an instance of
                        RGBColor, CMYKColor, or any other color type.
        """
        self.colors.append(PaletteColor(name, color))


class PaletteColor(NamedTuple):
    """
    A named tuple representing a swatch color.
    Attributes:
        name (str): The name of the color swatch.
        color (ColorBase): The color value associated with the swatch.
    """

    name: str
    color: ColorBase


class PaletteReader:
    """
    PaletteReader is a base class for any palette reader implementation.
    """

    @staticmethod
    def convert(f: TextIO) -> Palette:
        raise NotImplementedError(
            "convert method must be implemented in subclass"
        )


class PaletteWriter:
    """
    PaletteWriter is a base class for any palette writer implementation.
    """

    accepted_spaces: Union[List[ColorBase], Any] = Any

    @staticmethod
    def format_filepath(filepath: Path) -> Path:
        return filepath

    @staticmethod
    def write(f: BinaryIO, palette: Palette):
        raise NotImplementedError(
            "write method must be implemented in subclass"
        )


class PaletteAdapter:
    """
    Adapter class to convert a palette to a specific color space so that it is
    suitable for the following writer.
    """

    @classmethod
    def create_for(cls, target: Union[str, PaletteWriter]):
        """
        Create a palette for the given target.

        Parameters:
            target (Union[str, PaletteWriter]): The target color space or
                        PaletteWriter instance. If a string is provided,
                        it should correspond to a valid color space name.

        Returns:
            Palette: An instance of the Palette class initialized with the
                appropriate color spaces.

        Raises:
            ValueError: If the provided string does not correspond to a
                    supported color space.
        """
        if isinstance(target, str):
            if not hasattr(colormath.color_objects, f"{target}Color"):
                raise ValueError(f"Unsupported color space: {target}")
            spaces = [getattr(colormath.color_objects, f"{target}Color")]
        else:
            spaces = target.accepted_spaces
        return cls(spaces)

    def __init__(self, spaces: List[ColorBase]):
        self.spaces = spaces

    def convert_palette(self, palette: Palette) -> Palette:
        """
        Convert the colors in the palette to the target color space.
        """
        if self.spaces is Any:
            return palette
        new_palette = Palette()
        for name, color in palette.colors:
            if type(color) in self.spaces:
                new_palette.add_color(name, color)
            else:
                new_color = convert_color(color, self.spaces[0])
                new_palette.add_color(name, new_color)
        return new_palette


class ConvertionDefinition(NamedTuple):
    """
    An available convertion operation.
    """

    inputf: Path
    outputf: Path
    reader: Type[PaletteReader]
    writer: Type[PaletteWriter]
    space: Optional[str] = None


def convert(definition: ConvertionDefinition):
    """
    Convert a palette from one format to another using the given definition.
    """
    with open(definition.inputf, "r", encoding="utf-8") as fin:
        palette = definition.reader.convert(fin)
    adapter = PaletteAdapter.create_for(definition.space or definition.writer)
    new_palette = adapter.convert_palette(palette)
    filepath = definition.writer.format_filepath(definition.outputf)
    with open(filepath, "wb") as fout:
        definition.writer.write(fout, new_palette)
