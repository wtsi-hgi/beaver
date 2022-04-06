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

import abc
from typing import Set


class IdentityManager(abc.ABC):
    """provides an abstract class for an identity manager
        which will manage users and their group memberships
    """

    def __init__(self, **_) -> None:
        pass

    @abc.abstractmethod
    def get_groups_for_user(self, user_id: str) -> Set[str]:
        """get groups user `user_id` is a part of"""
