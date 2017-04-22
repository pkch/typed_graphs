# module: igraph.py
from typing import AbstractSet, Any, Set, Iterator, Collection, TypeVar
from abc import ABCMeta, abstractmethod


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


class INodeMutable(INode, Collection['INodeMutable']):
    _adj: 'Set[INodeMutable]'


class IGraph(metaclass=ABCMeta):
    nodes: Collection[INode]
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
