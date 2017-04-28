# module graph_undirected.py
from typing import (
    TypeVar, Generic, Set, List, Dict, Optional, DefaultDict, Iterator,
    AbstractSet, Any, ClassVar
)
import pytest  # type: ignore
from igraph import IGraphMutable, INode, InvalidOperation, INodeMutable
from graph import Graph, Node
from graph_functions import generic_tests


class UndirectedGraph(Graph):
    allow_loops: ClassVar[bool] = False

    def add_edge(self, tail: Node, head: Node) -> None:  # type: ignore
        if head is tail:
            raise InvalidOperation('Cannot create loops in UndirectedGraph')
        super().add_edge(tail, head)
        super().add_edge(head, tail)

    def remove_edge(self, tail: Node, head: Node) -> None:  # type: ignore
        super().remove_edge(tail, head)
        super().remove_edge(head, tail)


@pytest.mark.parametrize('test_func', generic_tests)
def test_graph(test_func):  # type: ignore
    test_func(UndirectedGraph)


def test_loop() -> None:
    g = UndirectedGraph()
    node = g.add_node()
    with pytest.raises(InvalidOperation):
        g.add_edge(node, node)
