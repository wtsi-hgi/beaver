import argparse
import sys
from typing import Callable

import beaver.version


def kit_main() -> None:
    parser = argparse.ArgumentParser(
        description="kit command for running images")
    parser.add_argument("-v", "--version", action="store_true",
                        help="view the verson of kit")

    parser.add_argument("-g", "--group", nargs=1, help="group name")
    parser.add_argument("image", help="image to run", nargs="?")
    parser.add_argument(
        "command", help="command to run in container (interactive environment if not provided)", nargs="*")

    parser.usage = "kit -v | -h | [-g GROUP] image-name [command …] "

    args: argparse.Namespace = parser.parse_args()

    if args.version:
        print(f"kit version: {beaver.version.KIT_VERSION}")
        sys.exit(0)

    if not args.image:
        print(parser.usage)
        sys.exit(1)

    print(args)

    ...


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
