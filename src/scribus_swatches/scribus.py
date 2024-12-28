from pathlib import Path
from lxml import etree
from colormath.color_objects import ColorBase, sRGBColor, CMYKColor
from colormath.color_conversions import convert_color
from typing import NamedTuple, Optional, TextIO, Type


class SwatchColor(NamedTuple):
    """
    A named tuple representing a swatch color.
    Attributes:
        name (str): The name of the color swatch.
        color (ColorBase): The color value associated with the swatch.
    """

    name: str
    color: ColorBase


class ScribusSwatch:
    """
    A class to manage a collection of color swatches for Scribus.
    """

    def __init__(self):
        self.colors: list[SwatchColor] = []

    def add_color(self, name: str, color: ColorBase):
        """
        Adds a color to the swatch list.

        Args:
            name (str): The name of the color.
            color (ColorBase): The color object to add. It can be an instance of
                        RGBColor, CMYKColor, or any other color type.

        Raises:
            ValueError: If the provided color space is not 'RGB' or 'CMYK'.

        """
        self.colors.append(SwatchColor(name, color))

    def write(self, f: TextIO, space: Optional[str] = None):
        """
        Write the colors to an XML file in the Scribus color format.

        Args:
            file (str or file-like object): The file path or file object where
                        the XML data will be written.
            space (str, optional): Overrides the color space for all colors.
                        If not provided, the color space will be inferred from
                        the color object. If provided, it must be either 'RGB'
                        or 'CMYK'.

        Raises:
            ValueError: If an unsupported color type is encountered.

        The XML structure will have a root element <SCRIBUSCOLORS> and each
        color will be represented as a <COLOR> element with attributes for the
        color values and names. RGB colors will have an attribute 'RGB' with
        the color value in hexadecimal format, and CMYK colors will have an
        attribute 'CMYK' with the color value in hexadecimal format.
        """
        if space.upper() not in ["RGB", "CMYK"]:
            raise ValueError("space must be either 'RGB' or 'CMYK'")
        space = space.upper()

        root = etree.Element("SCRIBUSCOLORS")
        for name, color in self.colors:
            if space is None:
                if isinstance(color, sRGBColor):
                    spaceitm = "RGB"
                elif isinstance(color, CMYKColor):
                    spaceitm = "CMYK"
                else:
                    color = convert_color(color, CMYKColor)
                    spaceitm = "CMYK"
            else:
                spaceitm = space
                target_space = sRGBColor if space == "RGB" else CMYKColor
                if not isinstance(color, target_space):
                    color = convert_color(color, target_space)

            if spaceitm == "RGB":
                color_value = color.get_rgb_hex()
                etree.SubElement(root, "COLOR", RGB=color_value, NAME=name)
            else:  # CMYK
                color_value = (
                    f"#{int(color.cmyk_c * 255):02x}"
                    f"{int(color.cmyk_m * 255):02x}"
                    f"{int(color.cmyk_y * 255):02x}"
                    f"{int(color.cmyk_k * 255):02x}"
                )
                etree.SubElement(root, "COLOR", CMYK=color_value, NAME=name)

        tree = etree.ElementTree(root)
        tree.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8")


class ConverterBase:
    @staticmethod
    def convert(f: TextIO) -> ScribusSwatch:
        raise NotImplementedError(
            "convert method must be implemented in subclass"
        )


class Convertion(NamedTuple):
    """
    An available convertion operation.
    """

    inputf: Path
    outputf: Path
    converter: Type[ConverterBase]
    space: Optional[str] = None
