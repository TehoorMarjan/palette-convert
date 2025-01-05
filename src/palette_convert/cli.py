import itertools
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional

import click

from .palette import ConvertionDefinition, convert
from .readers import get_reader
from .writers import get_writer


class ConvertionInput(NamedTuple):
    inputf: Path
    reader: str


class ConvertionOutputs(NamedTuple):
    outputdir: Path
    writer: str


available_inputs: Dict[str, ConvertionInput] = {
    "ReasonableColors": ConvertionInput(
        Path("reasonable-colors/reasonable-colors-rgb.scss"),
        "reasonablecolors",
    ),
    "OpenColor": ConvertionInput(
        Path("open-color/open-color.json"),
        "opencolor",
    ),
}

available_outputs: Dict[str, ConvertionOutputs] = {
    "Scribus": ConvertionOutputs(Path("scribus/"), "scribus"),
    "GIMP": ConvertionOutputs(Path("gimp/"), "gimp"),
    "LibreOffice": ConvertionOutputs(Path("libreoffice/"), "libreoffice"),
}


@click.command()
@click.option(
    "--output-dir",
    "-d",
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
    "--inputs", "-i", type=str, help="Comma separated list of inputs to run."
)
@click.option(
    "--outputs", "-o", type=str, help="Comma separated list of outputs to run."
)
@click.option(
    "--space",
    "-s",
    type=str,
    help="Override default colorspace of output.",
)
@click.option("--list", is_flag=True, help="List all available conversions.")
def main(
    output_dir: Path,
    vendor: Path,
    inputs: str,
    outputs: str,
    space: Optional[str],
    list: bool,
):
    if list:
        do_list()
        return

    selected_inputs = inputs.split(",") if inputs else available_inputs.keys()
    selected_outputs = (
        outputs.split(",") if outputs else available_outputs.keys()
    )

    do_convertions(output_dir, vendor, selected_inputs, selected_outputs, space)


def do_convertions(
    output_dir: Path,
    vendor: Path,
    inputs: List[str],
    outputs: List[str],
    space: Optional[str],
):
    selected_convertions = itertools.product(inputs, outputs)

    for namein, nameout in selected_convertions:
        if namein not in available_inputs or nameout not in available_outputs:
            click.echo(f"Conversion {namein} to {nameout} not found.")
            continue
        inc = available_inputs[namein]
        outc = available_outputs[nameout]
        input_file = (vendor / inc.inputf).resolve()
        output_writer_dir = (output_dir / outc.outputdir).resolve()

        if not output_writer_dir.exists():
            output_writer_dir.mkdir(parents=True)

        output_file = output_writer_dir / namein
        convertion = ConvertionDefinition(
            inputf=input_file,
            outputf=output_file,
            reader=get_reader(inc.reader),
            writer=get_writer(outc.writer),
            space=space,
        )
        convert(convertion)
        click.echo(f"Converted {namein} to {nameout}")


def do_list():
    click.echo("Available inputs:")
    for name in available_inputs.keys():
        click.echo(f"- {name}")
    click.echo("Available outputs:")
    for name, itm in available_outputs.items():
        spaces = ", ".join(
            (
                space.__name__.removesuffix("Color")
                for space in get_writer(itm.writer).accepted_spaces
            )
        )
        click.echo(f"- {name} (spaces: {spaces})")


if __name__ == "__main__":
    main()
