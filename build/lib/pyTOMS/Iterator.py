from typing import List, TypeVar, Generic

T = TypeVar("T")

class Iterator(Generic[T]):
    __iter = 0
    def __init__(self, objects: List[T]) -> None:
        self.__objects = objects
        return
    
    def __iter__(self) -> T:
        return self.__objects[self.__iter]
    
    def __next__(self) -> T:
        self.__iter += 1
        if self.__iter >= len(self.__objects):
            raise StopIteration()
        return self.__objects[self.__iter]
        