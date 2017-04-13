# module: graph.py
from typing import (
    Set, Dict, DefaultDict, Iterable,
    Any, Type
)
from collections import defaultdict
from io import StringIO
from igraph import IGraphMutable, INodeMutable, InvalidOperation
from graph_functions import generic_test_labeled_eq, generic_test_serialization


class Node(INodeMutable):
    def __init__(self, value: Any = None) -> None:
        self.value = value
        self.adj = set()

    def __repr__(self) -> str:
        return '<Node {}>'.format(self.value)


# this is a concrete implementation, using concrete Node class
class Graph(IGraphMutable):
    def __init__(self) -> None:
        self.nodes = set()

    # the return type must be the actual Node class, not the interface
    def add_node(self, value: Any = None) -> INodeMutable:
        '''
        Creates a new node that stores the provided value
        Adds the new node to the graph and returns it
        '''
        n = Node(value)
        self.nodes.add(n)
        return n

    def remove_node(self, node: INodeMutable) -> None:
        '''
        Removes the specified node and all edges to and from it
        Raises if node is not present
        '''
        for v in self.nodes:
            v.adj.discard(node)
        self.nodes.remove(node)

    def add_edge(self, tail: INodeMutable, head: INodeMutable) -> None:
        '''
        Adds the specified edge
        Raises if it's already present
        '''
        if head in tail.adj:
            raise InvalidOperation('Attempted to add a duplicate edge')
        tail.adj.add(head)

    def remove_edge(self, tail: INodeMutable, head: INodeMutable) -> None:
        '''
        Removes the specified edge
        Raises if it's not present
        '''
        tail.adj.remove(head)

    def __repr__(self) -> str:
        return '<Graph with {len(nodes)} nodes>\nNodes: {nodes}'.format(nodes=self.nodes)


def test_graph() -> None:
    generic_test_labeled_eq(Graph)
    generic_test_serialization(Graph)
