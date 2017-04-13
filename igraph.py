# module: igraph.py
from typing import AbstractSet, Any, Set
from abc import ABCMeta, abstractmethod


# used to report operations inconsistent with graph definition
class InvalidOperation(Exception): ...


class INode:
    adj: 'AbstractSet[INode]'
    value: Any


class INodeMutable(INode):
    adj: 'Set[INodeMutable]'


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
