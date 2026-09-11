import re
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader

load_dotenv()

DEFAULT_AUTHOR = os.getenv("DEFAULT_AUTHOR", None)
DEFAULT_NAMESPACE = os.getenv("DEFAULT_NAMESPACE", None)

parser = argparse.ArgumentParser(
    prog="C++ Boilerplate Generator",
    description="A command-line interface for generating boilerplate-ready C++ files.",
    epilog="By TeRacksito",
)

parser.add_argument(
    "filename",
    help="The path and name where the boilerplate will be generated. Must use snake_case. Do not include extension.",
)

parser.add_argument(
    "--author",
    "-a",
    default=DEFAULT_AUTHOR,
    required=False if DEFAULT_AUTHOR else True,
    help=f"The Author of the generated files.{f" Default is '{DEFAULT_AUTHOR}'" if DEFAULT_AUTHOR else ""}",
)

parser.add_argument(
    "--namespace",
    "-n",
    default=DEFAULT_NAMESPACE,
    required=False if DEFAULT_NAMESPACE else True,
    help=f"The Namespaces the generated files will use. {f" Default is '{DEFAULT_NAMESPACE}'" if DEFAULT_NAMESPACE else ""}",
)

parser.add_argument(
    "--overwrite",
    "-w",
    action="store_true",
    help="If true, the program will overwrite existing output files. Default is false.",
)

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument(
    "--class",
    "-c",
    dest="is_class",
    const="class",
    action="store_const",
    help="If true, the generated boilerplate will be a class. Default is false",
)

group.add_argument(
    "--function",
    "-f",
    dest="is_function",
    const="function",
    action="store_const",
    help="If true, the generated boilerplate will be a function. Default is false",
)


def write_file(filepath: Path, content: str, overwrite: bool):
    if filepath.exists() and not overwrite:
        print(f"Skipped: '{filepath}' already exists. Use --overwrite to overwrite it.")
        return

    status = "Overwritten" if filepath.exists() else "Created"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content)
    print(f"{status}: {filepath}")


def main():
    args = parser.parse_args(["--help"] if len(sys.argv) == 1 else None)

    mode: str | None = args.is_class or args.is_function or None

    if not mode:
        raise ValueError("You must specify either --class or --function.")

    base_path = Path(args.filename)
    class_name = "".join(word.capitalize() for word in base_path.name.split("_"))
    guard_base = base_path.as_posix().strip("./")
    guard = re.sub(r"[^a-zA-Z0-9]", "_", guard_base).upper() + "_H"

    header_path = Path(f"{args.filename}.h")
    source_path = Path(f"{args.filename}.cc")
    include_fname = header_path.as_posix()

    env = Environment(loader=PackageLoader("cpp_gen", "templates"))
    template_h = env.get_template("header.h.j2")
    template_cc = env.get_template("source.cc.j2")

    now = datetime.now()

    context = {
        "author": args.author,
        "namespace": args.namespace,
        "mode": mode,
        "class_name": class_name,
        "function_name": class_name,
        "guard": guard,
        "year": now.strftime("%Y"),
        "date": now.strftime("%Y-%m-%d"),
    }

    rendered_h = template_h.render(fname_h=header_path.name, **context)
    rendered_cc = template_cc.render(
        fname_cc=source_path.name, include_fname=include_fname, **context
    )

    print(f"Generating {mode} '{class_name}'")
    write_file(header_path, rendered_h, getattr(args, "overwrite", False))
    write_file(source_path, rendered_cc, getattr(args, "overwrite", False))


if __name__ == "__main__":
    main()
