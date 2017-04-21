# module: igraph.py
from typing import AbstractSet, Any, Set, Iterator, Collection, TypeVar
from abc import ABCMeta, abstractmethod


T = TypeVar('T', bound='INode')


# used to report operations inconsistent with graph definition
class InvalidOperation(Exception): ...


class INode(Collection['INode']):
    _adj: 'AbstractSet[INode]'
    value: Any

    def __iter__(self: T) -> Iterator[T]:
        return iter(self._adj)  # type: ignore

    def __len__(self) -> int:
        return len(self._adj)

    def __contains__(self, item: object) -> bool:
        return item in self._adj


class INodeMutable(INode, Collection['INodeMutable']):
    _adj: 'Set[INodeMutable]'


class IGraph(metaclass=ABCMeta):
    nodes: AbstractSet[INode]
    allow_loops = True


class IGraphMutable(IGraph):
    nodes: Set[INodeMutable]

    @abstractmethod
    def add_node(self, value: Any = None) -> INodeMutable: ...

    @abstractmethod
    def remove_node(self, node: INodeMutable) -> None: ...

    @abstractmethod
    def add_edge(self, tail: INodeMutable, head: INodeMutable) -> None: ...

    @abstractmethod
    def remove_edge(self, tail: INodeMutable, head: INodeMutable) -> None: ...
