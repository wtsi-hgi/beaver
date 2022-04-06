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

from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from beaver.http.route_names import router as names_router
from beaver.http.route_images import router as images_router
from beaver.http.route_image_usage import router as image_usage_router
from beaver.http.route_packages import router as package_router
from beaver.http.route_jobs import router as jobs_router

import beaver.db.db
from beaver.db.db import get_db
import beaver.db.jobs
from beaver.models.jobs import BuildRequest, Job

from .env import load_config_from_file

load_config_from_file("beaver_config.yml")

beaver.db.db.create_connectors(
    "mysql+mysqlconnector://beaver:beaverPass@localhost/beaver")
app = FastAPI()


@app.get("/")
async def root():
    """test endpoint"""
    return {
        "message": "Hello World"
    }


@app.post("/build", response_model=Job)
async def submit_build_request(
    build: BuildRequest,
    database: Session = Depends(get_db)
) -> beaver.db.jobs.Job:
    """submit all the data for a build job to start
    required schema:
        {
            "image": {
                "image_name": "name of image" | null (will auto generate),
                "user_name": "username",
                "group_name": "groupname"
            },
            "packages": [
                ID
            ],
            "new_packages": [
                note these are very specific
                it means just nix stuff (for now)
                "nix_pkg_name"
            ]
        }

    it'll return a job object

    """

    try:
        return beaver.db.jobs.submit_job(database, build)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=err.args) from err

app.include_router(names_router)
app.include_router(images_router)
app.include_router(image_usage_router)
app.include_router(package_router)
app.include_router(jobs_router)
