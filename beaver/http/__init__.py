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

from fastapi import FastAPI

from beaver.http.route_names import router as names_router
from beaver.http.route_images import router as images_router
from beaver.http.route_image_usage import router as image_usage_router
from beaver.http.route_packages import router as package_router
from beaver.http.route_jobs import router as jobs_router
import beaver.db.db

beaver.db.db.create_connectors(
    "mysql+mysqlconnector://beaver:beaverPass@localhost/beaver")
app = FastAPI()


@app.get("/")
async def root():
    """test endpoint"""
    return {
        "message": "Hello World"
    }

app.include_router(names_router)
app.include_router(images_router)
app.include_router(image_usage_router)
app.include_router(package_router)
app.include_router(jobs_router)
