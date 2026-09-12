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



Check the available commands with:

```bash
cpp-gen --help
```

## Install with pipx

To install the CLI tool system-wide for your Ubuntu user, install and configure `pipx` first, then run:

```bash
pipx install .
```

## Defaults

You can define default values for the author and namespace in a `.cpp-gen.env` file in your home directory. For example:

```bash
DEFAULT_AUTHOR="name"
DEFAULT_NAMESPACE="my_namespace"
```

You can easily create this file with the following command:

```bash
echo 'DEFAULT_AUTHOR="name"' >> ~/.cpp-gen.env
echo 'DEFAULT_NAMESPACE="my_namespace"' >> ~/.cpp-gen.env
```