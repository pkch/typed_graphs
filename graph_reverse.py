# module graph_reverse.py
from typing import (
    TypeVar, Generic, Set, List, Dict, Optional, DefaultDict, Iterator,
    AbstractSet, Any
)
import pytest  # type: ignore
from igraph import IGraphMutable, INode
import graph
from graph_functions import generic_tests


class Node(graph.Node):
    _adj: 'Set[Node]'  # type: ignore
    _back: 'Set[Node]'

    def __init__(self, value: Any = None) -> None:
        self._back = set()
        super().__init__(value)

    def back(self) -> 'Iterator[Node]':
        return iter(self._back)


class ReversibleGraph(graph.Graph):
    _nodes: Set[Node]  # type: ignore

    def add_node(self, value: Any = None) -> Node:
        n = Node(value)
        self._nodes.add(n)
        return n

    def remove_node(self, node: Node) -> None:  # type: ignore
        # update _back adjacency sets
        for neighbor in node:
            # check not self (superclass takes care of that, doing it twice will raise)
            if neighbor is not node:
                neighbor._back.remove(node)
        super().remove_node(node)

    def add_edge(self, tail: Node, head: Node) -> None:  # type: ignore
        # update _back adjacency sets
        head._back.add(tail)
        super().add_edge(tail, head)

    def remove_edge(self, tail: Node, head: Node) -> None:  # type: ignore
        # update _back adjacency sets
        head._back.remove(tail)
        super().remove_edge(tail, head)


@pytest.mark.parametrize('test_func', generic_tests)
def test_graph(test_func):  # type: ignore
    test_func(ReversibleGraph)
