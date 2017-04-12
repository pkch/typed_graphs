# module: igraph.py
from typing import AbstractSet, Any, Set
from abc import ABCMeta, abstractmethod


class INode:
    adj: 'AbstractSet[INode]'
    value: Any


class INodeMutable(INode):
    adj: 'Set[INodeMutable]'


class IGraph(metaclass=ABCMeta):
    nodes: AbstractSet[INode]


class IGraphMutable(IGraph):
    nodes: Set[INodeMutable]

    @abstractmethod
    def add_node(self, value: Any = None) -> INodeMutable:
        pass

    @abstractmethod
    def remove_node(self, node: INodeMutable) -> None:
        pass

    @abstractmethod
    def add_edge(self, tail: INodeMutable, head: INodeMutable) -> None:
        pass

    @abstractmethod
    def remove_edge(self, tail: INodeMutable, head: INodeMutable) -> None:
        pass
