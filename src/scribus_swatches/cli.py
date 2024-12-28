from pathlib import Path
import click
from typing import Dict, Optional
from .scribus import Convertion
from .reasonable_colors import ReasonableColorsConverter


convertions: Dict[str, Convertion] = {
    "ReasonableColors": Convertion(
        Path("reasonable-colors/reasonable-colors-rgb.scss"),
        Path("Reasonable_Colors.xml"),
        ReasonableColorsConverter,
        "CMYK",
    )
}


@click.command()
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(
        dir_okay=True,
        file_okay=False,
        path_type=Path,
        resolve_path=True,
        writable=True,
    ),
    default="out",
    help="Directory for generated swatches.",
)
@click.option(
    "--vendor",
    "-v",
    type=click.Path(
        dir_okay=True,
        file_okay=False,
        path_type=Path,
        resolve_path=True,
        readable=True,
    ),
    default="vendor/",
    help="Directory where the vendor files are located.",
)
@click.option(
    "--only", "-n", type=str, help="Comma separated list of conversions to run."
)
@click.option(
    "--space",
    "-s",
    type=click.Choice(("RGB", "CMYK"), case_sensitive=True),
    help="Override default colorspace of output.",
)
@click.option("--list", is_flag=True, help="List all available conversions.")
def main(
    output_dir: Path, vendor: Path, only: str, space: Optional[str], list: bool
):
    if list:
        click.echo("Available conversions:")
        for name in convertions.keys():
            click.echo(f"- {name}")
        return

    if not output_dir.exists():
        output_dir.mkdir()

    selected_convertions = only.split(",") if only else convertions.keys()

    for name in selected_convertions:
        if name in convertions:
            convertion = convertions[name]
            input_file = (vendor / convertion.inputf).resolve()
            output_file = (output_dir / convertion.outputf).resolve()
            space = space or convertion.space
            with (
                open(input_file, "r", encoding="utf-8") as fin,
                open(output_file, "wb") as fout,
            ):
                swatch = convertion.converter.convert(fin)
                swatch.write(fout, space)
            click.echo(f"Converted {name} to {convertion.outputf!s}")
        else:
            click.echo(f"Conversion {name} not found.")


if __name__ == "__main__":
    main()
