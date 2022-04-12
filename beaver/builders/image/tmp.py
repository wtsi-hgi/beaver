from beaver.builders.definition import Definition
from beaver.builders.definition.tmp import TmpDefinition
from beaver.builders.image import Image
from beaver.builders.image.core import ImageBuilder

class TmpImage(Image):
    ...

class TempImageBuilder(ImageBuilder):
    def build(self, definition: Definition) -> TmpImage:
        if not isinstance(definition, TmpDefinition):
            raise TypeError
        return TmpImage()