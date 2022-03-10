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
from beaver.db.names import ImageNameAdjective, ImageNameName
from beaver.db.jobs import Job

from beaver.db.packages import GitHubPackage, Package
from beaver.db.groups import Group
from beaver.db.users import User
import beaver.db.db
import beaver.http
from beaver.models.jobs import JobStatus


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

        self.default_time = datetime(2006, 1, 2, 22, 4, 5)
        self.now = datetime.now()

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
                datetime=self.default_time
            )

            database.add(_image_usage)

        # We'll also add some contents to images
        _image_contents = ImageContents(
            image_id=1,
            package_id=1
        )

        # Add a few possible image name sections
        for i in range(5):
            _adjective = ImageNameAdjective(
                adjective=f"adj{i}"
            )
            database.add(_adjective)

            _name = ImageNameName(
                name=f"name{i}"
            )
            database.add(_name)

        database.add(_image_contents)

        # Let's now sort out some jobs
        # 7 Queued Jobs
        # (we don't particulary care that they're all
        # for the same image)
        for i in range(7):
            _job = Job(
                job_id=f"q{i}",
                image_id=1
            )
            database.add(_job)

        # 4 Jobs Building Definition
        for i in range(4):
            _job = Job(
                job_id=f"bd{i}",
                image_id=1,
                status=JobStatus.BuildingDefinition,
                starttime=self.default_time
            )

            database.add(_job)

        # 2 Jobs Pending Actual Build
        for i in range(2):
            _job = Job(
                job_id=f"p{i}",
                image_id=1,
                status=JobStatus.DefinitionMade,
                starttime=self.default_time
            )

            database.add(_job)

        # 8 Jobs Building Image
        for i in range(8):
            _job = Job(
                job_id=f"bi{i}",
                image_id=1,
                status=JobStatus.BuildingImage,
                starttime=self.default_time
            )

            database.add(_job)

        # 5 Completed Builds in Last 24 Hours
        for i in range(5):
            _job = Job(
                job_id=f"c{i}",
                image_id=1,
                status=JobStatus.Succeeded,
                starttime=self.default_time,
                endtime=self.now,
                detail=f"Completed Build {i}"
            )

            database.add(_job)

        # 2 Jobs Completed in the Past
        for i in range(2):
            _job = Job(
                job_id=f"c.old{i}",
                image_id=1,
                status=JobStatus.Succeeded,
                starttime=self.default_time,
                endtime=self.default_time,
                detail=f"Completed Old Job {i}"
            )

            database.add(_job)

        # 3 Failed Builds in Last 24 Hours
        for i in range(3):
            _job = Job(
                job_id=f"f{i}",
                image_id=1,
                status=JobStatus.Failed,
                starttime=self.default_time,
                endtime=self.now,
                detail=f"Failed Build {i}"
            )

            database.add(_job)

        # 4 Jobs Failed in the Past
        for i in range(4):
            _job = Job(
                job_id=f"f.old{i}",
                image_id=1,
                status=JobStatus.Failed,
                starttime=self.default_time,
                endtime=self.default_time,
                detail=f"Failed Old Job {i}"
            )

            database.add(_job)

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

    # def test_get_images_for_user(self):
    #     # TODO
    #     ...

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
        assert data[0]["datetime"] == self.default_time.isoformat()

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
        assert data[0]["datetime"] == self.default_time.isoformat()

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
        assert data[0]["datetime"] == self.default_time.isoformat()

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
        assert data[0]["datetime"] == self.default_time.isoformat()

    def test_get_job_information(self):
        """test getting counts of jobs in various states

        Expects:
            {
                "jobs_queued": 7,
                "jobs_building_definition": 4,
                "jobs_pending_image_build": 2,
                "jobs_building_image": 8,
                "jobs_completed_last_24_hours": 5,
                "jobs_failed_last_24_hours": 3
            }
        """

        response = self.client.get("/jobs")
        assert response.status_code == 200
        assert response.json() == {
            "jobs_queued": 7,
            "jobs_building_definition": 4,
            "jobs_pending_image_build": 2,
            "jobs_building_image": 8,
            "jobs_completed_last_24_hours": 5,
            "jobs_failed_last_24_hours": 3
        }

    def test_get_job(self):
        """test getting job information

        Test Cases:
            - Request Job q1
            Expects:
                - Job Status: Queued
                - Image ID: 1
                - Start Time: Not Set
                - End Time: Not Set

            - Request Job bd1
            Expects:
                - Job Status: BuildingDefinition
                - Image ID: 1
                - Start Time: 2nd Jan 2006
                - End Time: Not Set

            - Request Job p1
            Expects:
                - Job Status: DefinitionMade
                - Image ID: 1
                - Start Time: 2nd Jan 2006
                - End Time: Not Set

            - Request Job bi1
            Expects:
                - Job Status: BuildingImage
                - Image ID: 1
                - Start Time: 2nd Jan 2006
                - End Time: Not Set

            - Request Job c1
            Expects:
                - Job Status: Succeeded
                - Image ID: 1
                - Start Time: 2nd Jan 2006
                - End Time: now
                - Detail: Completed Build 1

            - Request Job f1
            Expects:
                - Job Status: Failed
                - Image ID: 1
                - Start Time: 2nd Jan 2006
                - End Time: now
                - Detail: Failed Build 1

        """

        # Queued Job
        response = self.client.get("/jobs/q1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Queued"
        assert data["image_id"] == 1
        assert data["starttime"] is None
        assert data["endtime"] is None

        # BuildingDefinition Job
        response = self.client.get("/jobs/bd1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "BuildingDefinition"
        assert data["image_id"] == 1
        assert data["starttime"] == self.default_time.isoformat()
        assert data["endtime"] is None

        # DefinitionMade Job
        response = self.client.get("/jobs/p1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "DefinitionMade"
        assert data["image_id"] == 1
        assert data["starttime"] == self.default_time.isoformat()
        assert data["endtime"] is None

        # BuildingImage Job
        response = self.client.get("/jobs/bi1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "BuildingImage"
        assert data["image_id"] == 1
        assert data["starttime"] == self.default_time.isoformat()
        assert data["endtime"] is None

        # Succeeded Job
        response = self.client.get("/jobs/c1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Succeeded"
        assert data["image_id"] == 1
        assert data["starttime"] == self.default_time.isoformat()
        assert data["endtime"] == self.now.isoformat()
        assert data["detail"] == "Completed Build 1"

        # Failed Job
        response = self.client.get("/jobs/f1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Failed"
        assert data["image_id"] == 1
        assert data["starttime"] == self.default_time.isoformat()
        assert data["endtime"] == self.now.isoformat()
        assert data["detail"] == "Failed Build 1"

    def test_get_image_names(self):
        """test getting possible image name parts

        Expects:
            {
                "adjectives": [
                    "adj0",
                    "adj1",
                    "adj2",
                    "adj3",
                    "adj4"
                ],
                "names": [
                    "name0",
                    "name1",
                    "name2",
                    "name3",
                    "name4"
                ]
            }

        Note: although these are arrays, we don't care
            about the order
        """

        response = self.client.get("/names")
        assert response.status_code == 200
        data = response.json()

        assert "adjectives" in data
        assert "names" in data

        assert set(data["adjectives"]) == {
            "adj0", "adj1", "adj2", "adj3", "adj4"}
        assert set(data["names"]) == {
            "name0", "name1", "name2", "name3", "name4"}

    def tearDown(self) -> None:
        os.remove("_tmp_db.db")
