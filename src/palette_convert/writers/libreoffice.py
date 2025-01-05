from pathlib import Path
from typing import BinaryIO

from colormath.color_objects import sRGBColor
from lxml import etree

from ..palette import Palette, PaletteWriter


class LibreOfficeWriter(PaletteWriter):
    """
    LibreOfficeWriter is a class that is responsible for writing color palettes
    to an XML file in the LibreOffice color format.
    """

    accepted_spaces = [sRGBColor]

    @staticmethod
    def format_filepath(filepath: Path) -> Path:
        """
        Ensure the filepath ends with the .soc extension.

        Args:
            filepath (Path): The original file path.

        Returns:
            Path: The file path with the .soc extension.
        """
        if filepath.suffix == ".soc":
            return filepath
        return filepath.with_suffix(".soc")

    @staticmethod
    def write(f: BinaryIO, palette: Palette):
        """
        Write the colors to an XML file in the LibreOffice color format.

        Args:
            f (BinaryIO): The file object where the XML data will be written.
            palette (Palette): The palette object containing the colors to write.

        Raises:
            ValueError: If an unsupported color type is encountered.
        """
        nsmap = {
            "office": "http://openoffice.org/2000/office",
            "style": "http://openoffice.org/2000/style",
            "text": "http://openoffice.org/2000/text",
            "table": "http://openoffice.org/2000/table",
            "draw": "http://openoffice.org/2000/drawing",
            "fo": "http://www.w3.org/1999/XSL/Format",
            "xlink": "http://www.w3.org/1999/xlink",
            "dc": "http://purl.org/dc/elements/1.1/",
            "meta": "http://openoffice.org/2000/meta",
            "number": "http://openoffice.org/2000/datastyle",
            "svg": "http://www.w3.org/2000/svg",
            "chart": "http://openoffice.org/2000/chart",
            "dr3d": "http://openoffice.org/2000/dr3d",
            "math": "http://www.w3.org/1998/Math/MathML",
            "form": "http://openoffice.org/2000/form",
            "script": "http://openoffice.org/2000/script",
        }
        color_table_tag = etree.QName(nsmap["office"], "color-table")
        color_tag = etree.QName(nsmap["draw"], "color")
        color_attr = etree.QName(nsmap["draw"], "color")
        name_attr = etree.QName(nsmap["draw"], "name")

        root = etree.Element(color_table_tag, nsmap=nsmap)
        for name, color in palette.colors:
            if isinstance(color, sRGBColor):
                color_value = color.get_rgb_hex()
                elm = etree.SubElement(root, color_tag)
                elm.set(name_attr, name)
                elm.set(color_attr, color_value)
            else:
                raise ValueError(f"Unsupported color type: {type(color)}")

        tree = etree.ElementTree(root)
        tree.write(f, pretty_print=True, xml_declaration=True, encoding="UTF-8")
