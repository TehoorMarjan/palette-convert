from pathlib import Path
from typing import BinaryIO

from colormath.color_objects import CMYKColor, sRGBColor
from lxml import etree

from ..palette import Palette, PaletteWriter


class ScribusWriter(PaletteWriter):
    """
    ScribusWriter is a class that is responsible for writing color palettes to
    an XML file in the Scribus color format.
    """

    accepted_spaces = [CMYKColor, sRGBColor]

    @staticmethod
    def format_filepath(filepath: Path) -> Path:
        """
        Ensure the filepath ends with the .xml extension.

        Args:
            filepath (Path): The original file path.

        Returns:
            Path: The file path with the .xml extension.
        """
        if filepath.suffix == ".xml":
            return filepath
        return filepath.with_suffix(".xml")

    @staticmethod
    def write(f: BinaryIO, palette: Palette):
        """
        Write the colors to an XML file in the Scribus color format.

        Args:
            file (str or file-like object): The file path or file object where
                        the XML data will be written.
            palette (Palette): The palette object containing the colors to write.

        Raises:
            ValueError: If an unsupported color type is encountered.

        The XML structure will have a root element <SCRIBUSCOLORS> and each
        color will be represented as a <COLOR> element with attributes for the
        color values and names. RGB colors will have an attribute 'RGB' with
        the color value in hexadecimal format, and CMYK colors will have an
        attribute 'CMYK' with the color value in hexadecimal format.
        """
        root = etree.Element("SCRIBUSCOLORS")
        for name, color in palette.colors:
            if isinstance(color, sRGBColor):
                space = "RGB"
            elif isinstance(color, CMYKColor):
                space = "CMYK"
            else:
                raise ValueError(f"Unsupported color type: {type(color)}")

            if space == "RGB":
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
