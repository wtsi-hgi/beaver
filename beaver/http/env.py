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

from types import SimpleNamespace
from typing import Dict, Type

import yaml

from beaver.utils.idm import IdentityManager
import beaver.utils.idm


class Env(SimpleNamespace):
    """general things needed
    all around the place
    """

    idm: IdentityManager


str_to_idm: Dict[str, Type[IdentityManager]] = {
    "SangerLDAPIdentityManager": beaver.utils.idm.SangerLDAPIdentityManager,
    "LocalJSONIdentityManager": beaver.utils.idm.LocalJSONIdentityManager
}


def load_config_from_file(config_filepath: str):
    """load the information from a YAML config to the Env namespace"""

    with open(config_filepath, encoding="utf-8") as config_file:
        config = yaml.full_load(config_file)

    Env.idm = str_to_idm[config["idm"]["name"]](
        **{k: v for k, v in config["idm"].items() if k != "name"})
