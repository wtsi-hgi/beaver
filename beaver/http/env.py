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


from dataclasses import dataclass

from beaver.utils.idm import IdentityManager
import beaver.utils.idm


@dataclass
class Env:
    """singleton instance of general things needed
    all around the place
    """

    _instance = None

    idm: IdentityManager

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Env, cls).__new__(cls)
        return cls._instance


# TODO: temporary until proper configuration sorted
Env.idm = beaver.utils.idm.SangerLDAPIdentityManager(
    "ldap-ro.internal.sanger.ac.uk", 389)
