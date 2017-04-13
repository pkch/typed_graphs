from typing import (
    TypeVar, Generic, Set, List, Dict, Callable, DefaultDict, Iterable, AbstractSet
)
from collections import defaultdict
from io import StringIO
import pytest  # type: ignore
from graph_functions import generic_tests, InvalidOperation


T = TypeVar('T')  # represents value type provided by user, and wrapped into Node


class Node(Generic[T]):
    '''
    public API:
    * value attribute
    * adj property
    '''

    # type annotation for instance attribute
    adj: 'Set[Node[T]]'

    # None default value automatically adds Optional to the argument type
    def __init__(self, value: T = None) -> None:
        self.value = value
        self.adj = set()

    def __repr__(self) -> str:
        return '<Node {}>'.format(self.value)


class Graph(Generic[T]):

    allow_loops = True
    nodes: Set[Node[T]]

    def __init__(self) -> None:
        self.nodes = set()

    def add_node(self, value: T = None) -> Node[T]:
        '''
        Creates a new node that stores the provided value
        Adds the new node to the graph and returns it
        '''
        n = Node(value)
        self.nodes.add(n)
        return n

    def remove_node(self, node: Node[T]) -> None:
        '''
        Removes the specified node and all edges to and from it
        Raises if node is not present
        '''
        for v in self.nodes:
            v.adj.discard(node)
        self.nodes.remove(node)

    def add_edge(self, tail: Node[T], head: Node[T]) -> None:
        '''
        Adds the specified edge
        Raises if it's already present
        '''
        if head in tail.adj:
            raise InvalidOperation('Attempted to add a duplicate edge')
        tail.adj.add(head)

    def remove_edge(self, tail: Node[T], head: Node[T]) -> None:
        '''
        Removes the specified edge
        Raises if it's not present
        '''
        tail.adj.remove(head)

    def __repr__(self) -> str:
        return f'<Graph with {len(self.nodes)} nodes>\nNodes: {self.nodes}'


@pytest.mark.parametrize('test_func', generic_tests)
def test_graph(test_func):  # type: ignore
    test_func(Graph)
