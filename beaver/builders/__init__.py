"""OK, so here's a general overview

NOTE: THIS SHOULDN'T JUST BE HERE LIKE THIS
It needs wrapping in a function, and called from
something that polls the database

"""

from beaver.builders.definition import Definition
from beaver.builders.definition.core import DefinitionBuilder
from beaver.builders.definition.tmp import TempBuilder
from beaver.builders.image.core import ImageBuilder
from beaver.builders.image.tmp import TempImageBuilder
from beaver.db.packages import Package
from beaver.utils.repository.core import Repository
from beaver.utils.repository.tmp import TempRepository

# all of this comes from the configuration
_def_builder: DefinitionBuilder = TempBuilder()
_img_builder: ImageBuilder = TempImageBuilder()
_repo: Repository = TempRepository()

# First, we pass a load of packages to the definition builder
_packages = {Package(), Package(), Package()}
_definition: Definition = _def_builder.build(_packages)

# Then we'll add the definition to the repo
for obj in _definition.to_repo():
    _repo.add(obj)

# THEN IN A SECOND PROCESS
# Then we can pull it from the repo
# (this'll use i guess the name of the image from the job)
_definition: Definition = _def_builder.definition_type.from_repo(_repo.get("image_name"))
_img = _img_builder.build(_definition)

# Note - this would be a different repo
_repo.add(_img)
