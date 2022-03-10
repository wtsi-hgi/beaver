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
import sqlite3

import beaver.db.db


def set_up_database():
    """create a testing SQLite database"""
    try:
        os.remove("_tmp_db.db")
    except FileNotFoundError:
        pass

    sqlite3.connect("_tmp_db.db")

    beaver.db.db.create_connectors("sqlite:///./_tmp_db.db")
    beaver.db.db.create_db()
