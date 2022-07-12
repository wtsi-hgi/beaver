"""OK, so here's a general overview"""

from beaver.builders.definition import Definition
from beaver.builders.definition.core import DefinitionBuilder
from beaver.builders.definition.tmp import TempBuilder
from beaver.builders.image.core import ImageBuilder
from beaver.builders.image.tmp import TempImageBuilder
from beaver.db.packages import Package
from beaver.utils.repository.core import Repository
from beaver.utils.repository.tmp import TempRepository

# all of this comes from the configuration
def_builder: DefinitionBuilder = TempBuilder()
img_builder: ImageBuilder = TempImageBuilder()
repo: Repository = TempRepository()

# First, we pass a load of packages to the definition builder
packages = {Package(), Package(), Package()}
definition: Definition = def_builder.build(packages)

# Then we'll add the definition to the repo
for obj in definition.to_repo():
    repo.add(obj)

# THEN IN A SECOND PROCESS
# Then we can pull it from the repo
# (this'll use i guess the name of the image from the job)
definition: Definition = def_builder.definition_type.from_repo(
    repo.get("image_name"))
img = img_builder.build(definition)

# Note - this would be a different repo
repo.add(img)
