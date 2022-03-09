"""
HGI Beaver - Software Provisioning
Copyright (C) 2022 Michael Grace <mg38@sanger.ac.uk>

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

from datetime import datetime
import unittest
import sqlite3
import os

from fastapi.testclient import TestClient
from beaver.db.image_usage import ImageUsage
from beaver.db.images import Image, ImageContents

from beaver.db.packages import GitHubPackage, Package
from beaver.db.groups import Group
from beaver.db.users import User
import beaver.db.db
import beaver.http


class TestAPIGetEndpoints(unittest.TestCase):
    """testing all API get endpoints with fake SQLite DB"""

    def setUp(self) -> None:
        try:
            os.remove("_tmp_db.db")
        except FileNotFoundError:
            pass

        sqlite3.connect("_tmp_db.db")

        self.app = beaver.http.app
        self.client = TestClient(self.app)

        beaver.db.db.create_connectors("sqlite:///./_tmp_db.db")
        beaver.db.db.create_db()

        # Now Add a Load of Testing Data to Extract
        database = next(beaver.db.db.get_db())

        # Make some useres and groups
        for i in range(3):
            _user = User(user_name=f"testUser{i}")
            database.add(_user)

            _group = Group(group_name=f"testGroup{i}")
            database.add(_group)

        # Make Some Packages
        # First, a std package, not from Git
        _package_a = Package(
            package_name="testPackage1"
        )
        database.add(_package_a)

        # Now a package with a Git Filename
        _package_b = Package(
            package_name="testPackage2",
            github_filename="test.filename"
        )
        database.add(_package_b)

        # Now something linked to a GitHub repo
        _package_c = Package(
            package_name="testPackage3"
        )
        database.add(_package_c)
        database.commit()
        database.refresh(_package_c)

        _gh_package = GitHubPackage(
            package_id=_package_c.package_id,
            github_user="testGHUser",
            repository_name="testRepoName"
        )
        database.add(_gh_package)

        self.image_usage_time = datetime(2006, 1, 2, 22, 4, 5)

        # Let's create a few images
        for i in range(1, 3):
            _image = Image(
                image_name=f"testImage{i}",
                user_id=i,
                group_id=i
            )
            database.add(_image)
            database.commit()
            database.refresh(_image)

            _image_usage = ImageUsage(
                image_id=i,
                user_id=i,
                group_id=i,
                datetime=self.image_usage_time
            )

            database.add(_image_usage)

        # We'll also add some contents to images
        _image_contents = ImageContents(
            image_id=1,
            package_id=1
        )

        database.add(_image_contents)

        database.commit()

    def test_get_root(self):
        """test root endpoint

        Expects: {
                "message": "Hello World"
                }
        """
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    def test_get_packages(self):
        """test retrieving package information

        Expects:
            - three packages returned in list
            - testPackage1 has no associated gh_file or package
            - testPackage2 has a gh filename
            - testPackage3 has a linked github repo
            - this repo is by the user 'testGHUser' and
                the repo is called 'testRepoName'
        """
        response = self.client.get("/packages")
        assert response.status_code == 200
        res_data = response.json()
        assert len(res_data) == 3

        _package_a = [x for x in res_data if x["package_name"]
                      == "testPackage1"][0]
        assert _package_a["github_filename"] is None
        assert _package_a["github_package"] is None

        _package_b = [x for x in res_data if x["package_name"]
                      == "testPackage2"][0]
        assert _package_b["github_filename"] == "test.filename"
        assert _package_b["github_package"] is None

        _package_c = [x for x in res_data if x["package_name"]
                      == "testPackage3"][0]
        assert _package_c["github_filename"] is None
        assert _package_c["github_package"] is not None
        _gh = _package_c["github_package"]
        assert _gh["github_user"] == "testGHUser"
        assert _gh["repository_name"] == "testRepoName"

    def test_image_usage_by_user(self):
        """test collecting image usage information
        for a particular user

        We are requesting for user id 1
        Expects:
            - usage of image by uid 1 to come back,
                used Jan 2 2006
            - no other image's to be returned

        """

        response = self.client.get("/images/usage/byuser/1")
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1
        assert data[0]["user_id"] == 1
        assert data[0]["datetime"] == self.image_usage_time.isoformat()

    def test_image_usage_by_group(self):
        """test collecting image usage information
        for a particular group

        We are requesting for group id 2
        Expects:
            - usage of image by gid 2 to come back
                used Jan 2 2006
            - no other images to be returned

        """

        response = self.client.get("/images/usage/bygroup/2")
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1
        assert data[0]["group_id"] == 2
        assert data[0]["datetime"] == self.image_usage_time.isoformat()

    def test_image_usage_by_image(self):
        """test collecting image usage information
        for a particular image

        We are requesting for image id 1
        Expects:
            - usage of image id 1 to come back
                used Jan 2 2006
            - no other images to be returned

        """

        response = self.client.get("/images/usage/byimage/1")
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 1
        assert data[0]["image_id"] == 1
        assert data[0]["datetime"] == self.image_usage_time.isoformat()

    def test_image_usage_by_package(self):
        """test collecting image usage information
            for a particular package

        We are requesting for package id 1

        Expects:
            - usage of image id 1 to come back
                used Jan 2 2006
            - no other images to be returned

        """

        response = self.client.get("/images/usage/bypackage/1")
        assert response.status_code == 200
        data = response.json()
        print(data)
        assert len(data) == 1
        assert data[0]["image_id"] == 1
        assert data[0]["datetime"] == self.image_usage_time.isoformat()

    def tearDown(self) -> None:
        os.remove("_tmp_db.db")
