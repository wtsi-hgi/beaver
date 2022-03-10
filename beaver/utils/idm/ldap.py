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

from typing import Set

import ldap

from .core import IdentityManager

SCOPE_SUBTREE = 2


class SangerLDAPIdentityManager(IdentityManager):
    """interfaces with the Sanger LDAP servers whilst providing
        an `IdentityManager` interface
    """

    def __init__(self, ldap_host: str, ldap_port: int) -> None:
        self.ldap_host = ldap_host
        self.ldap_port = ldap_port

    @property
    def _ldap_conn(self):
        conn = ldap.initialize(f"ldap://{self.ldap_host}:{self.ldap_port}")
        conn.bind("", "")
        return conn

    def get_groups_for_user(self, user_id: str) -> Set[str]:
        return set(x["cn"][0].decode("UTF-8") for _, x in self._ldap_conn.search_s(
            "dc=sanger,dc=ac,dc=uk",
            SCOPE_SUBTREE,
            f"(&(objectClass=groupOfNames)(member=uid={user_id},ou=people,dc=sanger,dc=ac,dc=uk))",
            ["cn"]
        ))
