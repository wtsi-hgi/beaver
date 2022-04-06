"""
HGI Beaver - Software Provisioning
Copyright (C) 2022 Genome Research Limited

Author: Michael Grace <mg38@sanger.ac.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import sys
from typing import Callable

import uvicorn

import beaver.version
import beaver.utils.env

_KIT_USAGE: str = "kit -v | -h | [-g GROUP] image-name [command …] "


def parse_kit(args: argparse.Namespace) -> str:
    """Parse the namespace of arguments to kit

    Args:
        args: argparse.Namespace - the CLI arguments
            provided

    Returns:
        str: what action has been taken

    Raises:
        ValueError: if neither -v flag or an image
            name provided
    """
    if args.version:
        print(f"kit version: {beaver.version.KIT_VERSION}")
        return "version"

    if not args.image:
        raise ValueError

    print(args)
    ...
    return "run"


def kit_main() -> None:
    """The main function for kit"""

    parser = argparse.ArgumentParser(
        description="kit command for running images")
    parser.add_argument("-v", "--version", action="store_true",
                        help="view the verson of kit")

    parser.add_argument("-g", "--group", help="group name")
    parser.add_argument("image", help="image to run", nargs="?")
    parser.add_argument(
        "command",
        help="command to run in container (interactive environment if not provided)",
        args="*"
    )

    parser.usage = _KIT_USAGE

    try:
        parse_kit(parser.parse_args())
    except ValueError:
        print(parser.usage)
        sys.exit(1)


def beaver_web_main(debug: bool = False) -> None:
    """The main function for the beaver web app"""

    uvicorn.run(
        "beaver.http:app",
        host="0.0.0.0",
        port=4557,
        reload=debug,
        debug=debug
    )


def beaver_build_main(_: bool = False) -> None:
    """The main function for the beaver builder"""

    print("Beaver Build")
    ...


def beaver_main() -> None:
    """The main beaver function, calling either the web app or builder"""

    parser = argparse.ArgumentParser(description="main beaver command")
    parser.add_argument("--debug", "-debug",
                        help="run in debug mode", action="store_true")
    parser.add_argument("module", choices=[
                        "web", "build"], help="which module would you like to run")
    args: argparse.Namespace = parser.parse_args()

    modules_to_funcs: dict[str, Callable[[bool], None]] = {
        "web": beaver_web_main,
        "build": beaver_build_main
    }

    beaver.utils.env.load_config_from_file("beaver_config.yml")

    modules_to_funcs[args.module](args.debug)
