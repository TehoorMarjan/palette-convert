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
```

### Options

```text
Usage: palette-convert [OPTIONS]

Options:
    -o, --output-dir DIRECTORY  Directory for generated swatches.
    -v, --vendor DIRECTORY      Directory where the vendor files are located.
    -n, --only TEXT             Comma separated list of conversions to run.
    -s, --space [RGB|CMYK]      Override default colorspace of output.
    --list                      List all available conversions.
    --help                      Show this message and exit.
```

## License

This repository is licensed under the CC0 License. See the [LICENSE](LICENSE) file for more information.

Modules in the `vendor` directory have their own licenses.

## Contributing / Questions

Contributions are welcome! Please open an issue or submit a pull request.
