import argparse
import sys
from typing import Callable

import beaver.version

_KIT_USAGE: str = "kit -v | -h | [-g GROUP] image-name [command …] "


def parse_kit(args: argparse.Namespace) -> str:
    if args.version:
        print(f"kit version: {beaver.version.KIT_VERSION}")
        return "version"

    if not args.image:
        raise ValueError

    print(args)
    ...
    return "run"


def kit_main() -> None:
    parser = argparse.ArgumentParser(
        description="kit command for running images")
    parser.add_argument("-v", "--version", action="store_true",
                        help="view the verson of kit")

    parser.add_argument("-g", "--group", help="group name")
    parser.add_argument("image", help="image to run", nargs="?")
    parser.add_argument(
        "command", help="command to run in container (interactive environment if not provided)", nargs="*")

    parser.usage = _KIT_USAGE

    try:
        parse_kit(parser.parse_args())
    except ValueError:
        print(parser.usage)
        sys.exit(1)


def beaver_web_main() -> None:
    print("Beaver Web")
    ...


def beaver_build_main() -> None:
    print("Beaver Build")
    ...


def beaver_main() -> None:
    parser = argparse.ArgumentParser(description="main beaver command")
    parser.add_argument("module", choices=[
                        "web", "build"], help="which module would you like to run")
    args: argparse.Namespace = parser.parse_args()

    modules_to_funcs: dict[str, Callable[[], None]] = {
        "web": beaver_web_main,
        "build": beaver_build_main
    }

    modules_to_funcs[args.module]
