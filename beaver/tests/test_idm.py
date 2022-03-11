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

import json
from pathlib import Path
import unittest

from beaver.utils.idm import LocalJSONIdentityManager


class TestLocalIdentityManager(unittest.TestCase):
    """test cases for our local identity manager
        which stores information in JSON
    """

    def test_add_users_to_idm(self):
        """test adding users through the IDM, and
            then check the JSON file matches
        """
        _idm = LocalJSONIdentityManager(Path("_test.json"))
        _idm.add_user_to_group("userA", "groupA")
        _idm.add_user_to_group("userA", "groupB")
        _idm.add_user_to_group("userB", "groupA")

        with open("_test.json", encoding="UTF-8") as idm_file:
            data = json.load(idm_file)
            self.assertEqual(data, {
                "groupA": ["userA", "userB"],
                "groupB": ["userA"]
            })

    def test_get_user_groups_from_idm(self):
        """test adding users to the JSON file
            and reading them through the IDM
        """

        data = {
            "group0": ["user0", "user1"],
            "group1": ["user0"]
        }

        with open("_test.json", "w", encoding="UTF-8") as idm_file:
            json.dump(data, idm_file)

        _idm = LocalJSONIdentityManager(Path("_test.json"))
        self.assertEqual(_idm.get_groups_for_user(
            "user0"), {"group0", "group1"})
        self.assertEqual(_idm.get_groups_for_user("user1"), {"group0"})

    def test_full_idm_usage(self):
        """test full use of IDM, adding users
        and then retrieving users
        """

        _idm = LocalJSONIdentityManager(Path("_test.json"))
        _idm.add_user_to_group("userX", "groupX")
        _idm.add_user_to_group("userX", "groupY")
        _idm.add_user_to_group("userY", "groupX")

        self.assertEqual(_idm.get_groups_for_user(
            "userX"), {"groupX", "groupY"})
        self.assertEqual(_idm.get_groups_for_user("userY"), {"groupX"})
