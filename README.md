# Palette Convert

This repository contains a tool for managing color palettes.

## Features

- Create palettes for Scribus or GIMP/Inkscape
- Palette from Reasonable Colors
- Palette from Open Color

## Installation

To install the required dependencies, use [Poetry](https://python-poetry.org/):

```bash
poetry install
```

## Usage

To see the available options, run:

```bash
poetry run palette-convert --help
poetry run palette-convert --list
```

### Options

```text
Usage: palette-convert [OPTIONS]

Options:
  -d, --output-dir DIRECTORY  Directory for generated swatches.
  -v, --vendor DIRECTORY      Directory where the vendor files are located.
  -i, --inputs TEXT           Comma separated list of inputs to run.
  -o, --outputs TEXT          Comma separated list of outputs to run.
  -s, --space TEXT            Override default colorspace of output.
  --list                      List all available conversions.
  --help                      Show this message and exit.
```

```text
Available inputs:
- ReasonableColors
- OpenColor
Available outputs:
- Scribus (spaces: CMYK, sRGB)
- GIMP (spaces: sRGB)
```

## Tools

In order to check the compliance of the code with respect to the guidelines, run

```bash
poetry run poe lint
```

To generate all palettes and create a zip file, use

```bash
poetry run poe package
```

## License

This repository is licensed under the CC0 License. See the [LICENSE](LICENSE) file for more information.

Modules in the `vendor` directory have their own licenses.

## Contributing / Questions

Contributions are welcome! Please open an issue or submit a pull request.
