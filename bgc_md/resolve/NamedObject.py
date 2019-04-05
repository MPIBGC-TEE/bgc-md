from abc import ABC,abstractmethod
class NamedObject(ABC):
    """ 
    all descendants have to have a 'name' property
    This class mainly exist to be able to type hint 
    appropriate arguments for indexing containers
    that use the name(s) of the contained objects
    as index.
    """ 
    @property
    @abstractmethod
    def name(self):
        raise Exception("""
            This method has to be implemented
            in the child classes"""
        )

