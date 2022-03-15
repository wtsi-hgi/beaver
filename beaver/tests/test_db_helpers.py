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

import os
import unittest

import beaver.db.db
from beaver.db.groups import Group
from beaver.db.names import ImageNameAdjective, ImageNameName, generate_random_image_name
from beaver.db.users import User
import beaver.http
from beaver.tests import set_up_database


class TestDBHelpers(unittest.TestCase):
    """testing helper functions that interact with the DB"""

    def setUp(self) -> None:
        set_up_database()

        database = next(beaver.db.db.get_db())

        self.possible_image_names = {
            "adjective0-name0",
            "adjective0-name1",
            "adjective1-name0",
            "adjective1-name1"
        }

        for i in range(2):
            _adj = ImageNameAdjective(adjective=f"adjective{i}")
            database.add(_adj)

            _name = ImageNameName(name=f"name{i}")
            database.add(_name)

        new_user = User(user_name="testUser")
        new_group = Group(group_name="testGroup")
        database.add(new_user)
        database.add(new_group)

        database.commit()

    def test_generating_image_name(self):
        """test that we can generate a random image name
        and it is like what we'd expect
        """

        database = next(beaver.db.db.get_db())
        image_name = generate_random_image_name(
            database, "testUser", "testGroup")

        self.assertIn(
            image_name, {f"testUser-testGroup-{x}" for x in self.possible_image_names})

    def test_get_user_id_from_user_name_that_doesnt_exist(self):
        """test that when we request the user id for a user
        that doesn't exist, it creates the user in the database
        and returns the new id
        """
        database = next(beaver.db.db.get_db())
        user_id = User.get_or_make_user_id_for_user_name(
            "testNewUser", database)
        self.assertEqual(user_id, 2)
        self.assertEqual(database.query(User).filter(
            User.user_name == "testNewUser").count(), 1)

    def test_get_user_id_from_user_name(self):
        """test getting a user id from the DB given the username"""

        database = next(beaver.db.db.get_db())
        user_id = User.get_or_make_user_id_for_user_name("testUser", database)
        self.assertEqual(user_id, 1)

    def test_get_group_id_from_group_name_that_doesnt_exist(self):
        """test that when we request the group id for a group
        that doesn't exist, it creates the group in the database
        and returns the new id
        """
        database = next(beaver.db.db.get_db())
        group_id = Group.get_or_make_group_id_for_group_name(
            "testNewGroup", database)
        self.assertEqual(group_id, 2)
        self.assertEqual(database.query(Group).filter(
            Group.group_name == "testNewGroup").count(), 1)

    def test_get_group_id_from_group_name(self):
        """test getting a group id from the DB given the groupname"""

        database = next(beaver.db.db.get_db())
        group_id = Group.get_or_make_group_id_for_group_name(
            "testGroup", database)
        self.assertEqual(group_id, 1)

    def tearDown(self) -> None:
        os.remove("_tmp_db.db")
