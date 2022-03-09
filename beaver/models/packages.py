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

import enum

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class GitHubPackage(BaseModel):
    """represents a package derived from github"""
    package_id: int
    github_user: str
    repository_name: str
    commit_hash: str | None

    class Config:
        """orm config"""
        orm_mode = True


class PackageType(enum.Enum):
    """types of package"""
    std = enum.auto()  # standard/custom made nix derivations pylint: disable=invalid-name
    R = enum.auto()  # R packages
    py = enum.auto()  # python packages pylint: disable=invalid-name


class PackageBase(BaseModel):
    """base representation of a package"""
    package_name: str
    package_version: str | None
    commonly_used: bool
    package_type: PackageType
    github_filename: str | None


class Package(PackageBase):
    """full representation of a package"""
    package_id: int
    github_package: GitHubPackage | None

    class Config:
        """orm config"""
        orm_mode = True
