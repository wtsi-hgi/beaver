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

from __future__ import annotations

import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty

from beaver.db.db import Base


class PackageType(enum.Enum):
    """types of package"""
    std = enum.auto()  # standard/custom made nix derivations pylint: disable=invalid-name
    R = enum.auto()  # R packages
    py = enum.auto()  # python packages pylint: disable=invalid-name


class Package(Base):
    """represents a single package/derivation"""

    __tablename__ = "packages"
    package_id = Column(Integer, primary_key=True)
    package_name = Column(String)
    package_version = Column(String)
    commonly_used = Column(Boolean)
    package_type = Column(Enum(PackageType))
    github_filename = Column(String)


class GitHubPackage(Base):
    """represents a package being pulled from GitHub"""

    __tablename__ = "github_packages"
    _dummy = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey("packages.package_id"))
    github_user = Column(String)
    repository_name = Column(String)
    commit_hash = Column(String)

    package: RelationshipProperty[Package] = relationship(
        "Package", back_populates="github_package")


class PackageDependency(Base):
    """links to packages as a dependency"""

    __tablename__ = "package_dependencies"
    _dummy = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey("packages.package_id"))
    dependency_id = Column(Integer, ForeignKey("packages.package_id"))

    package: RelationshipProperty[Package] = relationship("Package")
    dependency: RelationshipProperty[Package] = relationship("Package")
