import abc

from beaver.builders.definition import Definition
from beaver.builders.image import Image

class ImageBuilder(abc.ABC):
    @abc.abstractmethod
    def build(self, definition: Definition) -> Image:
        ...