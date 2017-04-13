# module graph_undirected.py
from typing import (
    TypeVar, Generic, Set, List, Dict, Optional, DefaultDict, Iterator,
    AbstractSet, Any
)
from igraph import IGraphMutable, INode, InvalidOperation
from graph import Graph, Node
from graph_functions import generic_test_labeled_eq, generic_test_serialization


class UndirectedGraph(Graph):
    nodes: Set[Node]  # type: ignore
    allow_loops = False

    def add_edge(self, tail: Node, head: Node) -> None:  # type: ignore
        if head is tail:
            raise InvalidOperation('Cannot create loops in UndirectedGraph')

        # it is quite common to add an edge twice in undirected graph, no need to raise
        try:
            super().add_edge(tail, head)
        except InvalidOperation:
            pass
        try:
            super().add_edge(head, tail)
        except InvalidOperation:
            pass

    def remove_edge(self, tail: Node, head: Node) -> None:  # type: ignore
        super().remove_edge(tail, head)
        super().remove_edge(head, tail)


def test_graph() -> None:
    generic_test_labeled_eq(UndirectedGraph)
    generic_test_serialization(UndirectedGraph)
