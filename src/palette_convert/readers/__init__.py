from typing import Optional

from ..palette import PaletteReader
from .open_color import OpenColorReader
from .reasonable_colors import ReasonableColorsReader


def get_reader(name: str) -> Optional[PaletteReader]:
    """
    Retrieve a palette reader class based on the given name.
    Args:
        name (str): The name of the palette reader to retrieve.
    Returns:
        Optional[PaletteReader]: The corresponding palette reader class if
            found, otherwise None.
    Available readers:
        - "reasonablecolors": ReasonableColorsReader
        - "opencolor": OpenColorReader
    """

    return {
        "reasonablecolors": ReasonableColorsReader,
        "opencolor": OpenColorReader,
    }.get(name, None)
