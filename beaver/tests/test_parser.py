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
import unittest

import beaver


class TestKitrgumentPasser(unittest.TestCase):
    """testing the argument parser for kit"""

    def test_no_args_provided(self) -> None:
        """testing not providing any args"""

        _ns = argparse.Namespace()
        _ns.version = False
        _ns.group = None
        _ns.image = None
        _ns.command = []

        with self.assertRaises(ValueError):
            beaver.parse_kit(_ns)

    def test_version_provided(self) -> None:
        """testing provding -v flag"""

        _ns = argparse.Namespace()
        _ns.version = True
        _ns.group = None
        _ns.image = None
        _ns.command = []

        self.assertEqual(beaver.parse_kit(_ns), "version")

    def test_version_and_image_provided(self) -> None:
        """testing providing -v and image"""

        _ns = argparse.Namespace()
        _ns.version = True
        _ns.group = None
        _ns.image = "image"
        _ns.command = []

        self.assertEqual(beaver.parse_kit(_ns), "version")

    def test_image_provided(self) -> None:
        """testing providing only image name"""

        _ns = argparse.Namespace()
        _ns.version = False
        _ns.group = None
        _ns.image = "image"
        _ns.command = []

        self.assertEqual(beaver.parse_kit(_ns), "run")
