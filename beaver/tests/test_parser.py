import argparse
import unittest

import beaver


class TestKitrgumentPasser(unittest.TestCase):

    def test_no_args_provided(self) -> None:

        _ns = argparse.Namespace()
        _ns.version = False
        _ns.group = None
        _ns.image = None
        _ns.command = []

        with self.assertRaises(ValueError):
            beaver.parse_kit(_ns)

    def test_version_provided(self) -> None:

        _ns = argparse.Namespace()
        _ns.version = True
        _ns.group = None
        _ns.image = None
        _ns.command = []

        self.assertEqual(beaver.parse_kit(_ns), "version")

    def test_version_and_image_provided(self) -> None:
        _ns = argparse.Namespace()
        _ns.version = True
        _ns.group = None
        _ns.image = "image"
        _ns.command = []

        self.assertEqual(beaver.parse_kit(_ns), "version")

    def test_image_provided(self) -> None:
        _ns = argparse.Namespace()
        _ns.version = False
        _ns.group = None
        _ns.image = "image"
        _ns.command = []

        self.assertEqual(beaver.parse_kit(_ns), "run")
