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
from pathlib import Path
from typing import Set, Dict, List

import json

from .core import IdentityManager


class LocalJSONIdentityManager(IdentityManager):
    """implements an IdentityManager using a local JSON file

        useful for use in tests instead of an LDAP server
    """

    def __init__(self, file_path: Path, temp: bool = True) -> None:
        self.file_path = file_path
        self.temp = temp

    def get_groups_for_user(self, user_id: str) -> Set[str]:
        with open(self.file_path, encoding="UTF-8") as idm_file:
            _data = json.load(idm_file)

        groups: Set[str] = set()
        for group_name, members in _data.items():
            if user_id in members:
                groups.add(group_name)
        return groups

    def add_user_to_group(self, user_id: str, group_name: str) -> None:
        """add the user specified by `user_id` to the group
            specified by `group_name`
        """

        try:
            with open(self.file_path, encoding="UTF-8") as idm_file:
                _data = json.load(idm_file)
        except FileNotFoundError:
            _data: Dict[str, List[str]] = {}

        if group_name in _data:
            _data[group_name].append(user_id)
        else:
            _data[group_name] = [user_id]

        with open(self.file_path, "w", encoding="UTF-8") as idm_file:
            json.dump(_data, idm_file)

    def __del__(self):
        if self.temp:
            try:
                os.remove(self.file_path)
            except FileNotFoundError:
                pass
