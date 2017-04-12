# module graph_reverse.py
from typing import (
    TypeVar, Generic, Set, List, Dict, Optional, DefaultDict, Iterator,
    AbstractSet, Any
)
from igraph import IGraphMutable, INode
import graph
from graph_functions import generic_test_labeled_eq, generic_test_serialization


class Node(graph.Node):
    adj: 'Set[Node]'  # type: ignore
    backward: 'Set[Node]'

    def __init__(self, value: Any = None) -> None:
        self.backward = set()
        super().__init__(value)


class ReversibleGraph(graph.Graph):
    nodes: Set[Node]  # type: ignore

    def add_node(self, value: Any = None) -> Node:
        n = Node(value)
        self.nodes.add(n)
        return n

    def remove_node(self, node: Node) -> None:  # type: ignore
        # update backward adjacency sets
        for neighbor in node.adj:
            neighbor.backward.remove(node)
        super().remove_node(node)

    def add_edge(self, tail: Node, head: Node) -> None:  # type: ignore
        # update backward adjacency sets
        tail.backward.add(head)
        super().add_edge(tail, head)

    def remove_edge(self, tail: Node, head: Node) -> None:  # type: ignore
        # update backward adjacency sets
        tail.backward.remove(head)
        super().remove_edge(tail, head)


def test_graph() -> None:
    generic_test_labeled_eq(ReversibleGraph)
    generic_test_serialization(ReversibleGraph)
