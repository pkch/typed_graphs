# module: igraph.py
from typing import AbstractSet, Any, Set, Iterator, Collection, TypeVar, Generic, ClassVar
from abc import abstractmethod


T = TypeVar('T', bound='INode')


# used to report operations inconsistent with graph definition
class InvalidOperation(Exception): ...


class INode(Collection['INode']):
    value: Any

    @abstractmethod
    def __iter__(self: T) -> Iterator[T]: ...

    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def __contains__(self, item: object) -> bool: ...


class INodeMutable(INode, Collection['INodeMutable']): ...


class IGraph(Collection[INode]):
    allow_loops: ClassVar[bool] = True


# we can't derive from Collection[IMutableNode] because of type system limitations
# so we won't be able to use this class' instances where `Iterable[IMutableNode]` is expected
# however, for loops will still produce the correct type based on `__iter__` signature
class IGraphMutable(IGraph):
    @abstractmethod
    def __iter__(self) -> Iterator[INodeMutable]: ...

    @abstractmethod
    def add_node(self, value: Any = None) -> INodeMutable: ...

    @abstractmethod
    def remove_node(self, node: INodeMutable) -> None: ...

    @abstractmethod
    def add_edge(self, tail: INodeMutable, head: INodeMutable) -> None: ...

    @abstractmethod
    def remove_edge(self, tail: INodeMutable, head: INodeMutable) -> None: ...
