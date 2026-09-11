# cpp-gen

`cpp-gen` is a command-line tool for generating C++ boilerplate files.

## Install for development

Create and activate a virtual environment first:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the package in editable mode:

```bash
pip install -e .
```

Copy the example environment file:

```bash
cp .env.example .env
```

Setting default values for `DEFAULT_AUTHOR` and `DEFAULT_NAMESPACE` in `.env` is optional.

Check the available commands with:

```bash
cpp-gen --help
```

## Install with pipx

To install the CLI tool system-wide for your Ubuntu user, install and configure `pipx` first, then run:

```bash
pipx install .
```
