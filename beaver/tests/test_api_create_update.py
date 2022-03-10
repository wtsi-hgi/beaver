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

from fastapi.testclient import TestClient

import beaver.db.db
from beaver.db.names import ImageNameAdjective, ImageNameName
from beaver.db.packages import GitHubPackage, Package
import beaver.http
from . import set_up_database


class TestAPICreateUpdateEndpoints(unittest.TestCase):
    """testing all API endpoints that create or update data
        with fake SQLite DB
    """

    def setUp(self) -> None:

        set_up_database()

        self.app = beaver.http.app
        self.client = TestClient(self.app)

    def test_create_package_not_github_linked(self):
        """test createing a new package, not linked to
            a github repository

        Expects:
            - returned data from api call to match what we sent
            - info in DB to match what we sent

        """
        new_package = {
            "package_name": "testPackage0",
            "package_version": None,
            "commonly_used": True,
            "package_type": "std",
            "github_filename": None,
            "github_package": None
        }

        response = self.client.post("/packages/", json=new_package)
        assert response.status_code == 200
        data = response.json()
        package_id = data["package_id"]
        del data["package_id"]
        assert data == new_package

        new_package["package_id"] = package_id
        del new_package["github_package"]

        database = next(beaver.db.db.get_db())

        db_package = database.query(Package).filter(
            Package.package_id == package_id).one().__dict__
        del db_package["_sa_instance_state"]
        db_package["package_type"] = db_package["package_type"].value
        assert db_package == new_package

    def test_create_package_github_linked(self):
        """test creating a new package that is linked to a github
            repository

        Expects:
            - the API response to be the same as what we gave it
            - the new data in the DB to be the same as what we
                gave it
        """
        new_package = {
            "package_name": "testPackage1",
            "package_version": "1.0",
            "commonly_used": False,
            "package_type": "std",
            "github_filename": None,
            "github_package": {
                "github_user": "testGHUser1",
                "repository_name": "testRepoName",
                "commit_hash": "abc123"
            }
        }

        response = self.client.post("/packages/", json=new_package)
        assert response.status_code == 200
        data = response.json()

        package_id = data["package_id"]
        gh_package_id = data["github_package"]["package_id"]
        del data["package_id"]
        del data["github_package"]["package_id"]

        assert data == new_package
        assert package_id == gh_package_id

        new_package["package_id"] = package_id
        new_package["github_package"]["package_id"] = gh_package_id

        database = next(beaver.db.db.get_db())

        db_package = database.query(Package).filter(
            Package.package_id == package_id).one().__dict__
        del db_package["_sa_instance_state"]
        db_package["package_type"] = db_package["package_type"].value

        gh_package = database.query(GitHubPackage).filter(
            GitHubPackage.package_id == gh_package_id).one().__dict__
        del gh_package["_sa_instance_state"]
        db_package["github_package"] = gh_package
        new_package["github_package"]["github_package_id"] = gh_package_id
        print(db_package)
        print(new_package)
        assert db_package == new_package

    def test_create_new_name_elements_adjectives(self):
        """test adding new adjectives to the possibilites of
            image names

        Expects:
            - the response we get back from the API is what we sent
            - the adjectives in the DB are what we've added
        """
        new_adjectives = {
            "names": [],
            "adjectives": [
                f"new_adj_{i}" for i in range(4)
            ]
        }

        response = self.client.post("/names/", json=new_adjectives)
        assert response.status_code == 200
        data = response.json()
        assert data == new_adjectives

        database = next(beaver.db.db.get_db())

        db_adjectives = [x.adjective for x in database.query(
            ImageNameAdjective).all()]
        assert all(x in db_adjectives for x in new_adjectives["adjectives"])

    def test_create_new_name_elements_names(self):
        """test adding new names to the possibilites of
            image names

        Expects:
            - the response we get back from the API is what we sent
            - the names in the DB are what we've added
        """
        new_adjectives = {
            "adjectives": [],
            "names": [
                f"new_name_{i}" for i in range(4)
            ]
        }

        response = self.client.post("/names/", json=new_adjectives)
        assert response.status_code == 200
        data = response.json()
        assert data == new_adjectives

        database = next(beaver.db.db.get_db())

        db_names = [x.name for x in database.query(ImageNameName).all()]
        assert all(x in db_names for x in new_adjectives["names"])

    def tearDown(self) -> None:
        os.remove("_tmp_db.db")
