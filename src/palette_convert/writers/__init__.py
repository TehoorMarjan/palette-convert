from typing import Optional

from ..palette import PaletteWriter
from .gimp import GIMPWriter
from .libreoffice import LibreOfficeWriter
from .scribus import ScribusWriter


def get_writer(name: str) -> Optional[PaletteWriter]:
    """
    Retrieve a palette writer class based on the given name.
    Args:
        name (str): The name of the palette reader to retrieve.
    Returns:
        Optional[PaletteWriter]: The corresponding palette reader class if
            found, otherwise None.
    Available readers:
        - "reasonablecolors": ReasonableColorsReader
        - "opencolor": OpenColorReader
    """

    return {
        "gimp": GIMPWriter,
        "scribus": ScribusWriter,
        "libreoffice": LibreOfficeWriter,
    }.get(name, None)
