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

import random

from sqlalchemy import Column, String
from sqlalchemy.orm import Session

from beaver.db.images import Image
from beaver.db.db import Base
from beaver.models.names import ImageNameElements


class ImageNameAdjective(Base):
    """class models adjectives for image names"""

    __tablename__ = "image_name_adjectives"
    adjective = Column(String, primary_key=True)


class ImageNameName(Base):
    """class models names for image names"""

    __tablename__ = "image_name_names"
    name = Column(String, primary_key=True)


def get_names(database: Session) -> ImageNameElements:
    """returns all the elements that could make up an image name"""
    return ImageNameElements(
        adjectives=[str(x.adjective) for x in database.query(
            ImageNameAdjective).all()],
        names=[str(x.name) for x in database.query(
            ImageNameName).all()]
    )


def create_names(database: Session, item: ImageNameElements) -> ImageNameElements:
    """adds elements to the lists of possible image name elements"""
    for adj in item.adjectives:
        db_adj_item = ImageNameAdjective(adjective=adj)
        database.add(db_adj_item)

    for name in item.names:
        db_name_item = ImageNameName(name=name)
        database.add(db_name_item)

    database.commit()
    return item


def check_image_name(database: Session, name: str) -> bool:
    """checks if a given image name is already in the database being
    used by a different image

    Args:
        - database: Session - the database session to use
        - name: str - the iamge name to check

    Returns: bool - True if the image isn't in use

    """

    return database.query(Image).filter(Image.image_name == name).count() == 0


def generate_random_image_name(database: Session, user: str, group: str) -> str:
    """generate a name for an image

    this will use the adjectives and names in the DB, along with the username
    and group name to produce one

    Args:
        - database: Session - the database session to use
        - user: str - the username
        - group: str - the group name

    Returns: str - the newly created image name

    """

    _elements = get_names(database)
    _adj = random.choice(_elements.adjectives)
    _name = random.choice(_elements.names)

    # we need to make sure this isn't already in the DB
    # yes, this can go into an infinite loop if every
    # possibility is already used

    # TODO: can we not have infinite loop?
    while True:
        candidate: str = f"{user}-{group}-{_adj}-{_name}"
        if check_image_name(database, candidate):
            return candidate
