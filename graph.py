from typing import (
    TypeVar, Generic, Set, List, Dict, Callable, DefaultDict, Iterable, AbstractSet
)
from collections import defaultdict
from io import StringIO


NodeValue = TypeVar('NodeValue')
T = TypeVar('T')  # same intent as NodeValue, but syntax prohibits same name


class Graph(Generic[NodeValue]):
    class Node(Generic[T]):
        '''
        public API:
        * value attribute
        * adj property
        '''

        # type annotation for instance attribute
        _adj: 'Set[Graph.Node[T]]'

        # None default value automatically adds Optional to the argument type
        def __init__(self, value: T = None) -> None:
            self.value = value
            self._adj = set()

        # ensure users don't mutate the adjacency set
        @property
        def adj(self) -> 'AbstractSet[Graph.Node[T]]':
            return self._adj

        def __repr__(self) -> str:
            return f'<Node {self.value}>'

    NV = Node[NodeValue]
    nodes: Set[NV]

    def __init__(self) -> None:
        self.nodes = set()

    def add_node(self, value: NodeValue = None) -> NV:
        '''
        Creates a new node that stores the provided value
        Adds the new node to the graph and returns it
        '''
        n = Graph.Node(value)
        self.nodes.add(n)
        return n

    def remove_node(self, node: NV) -> None:
        '''
        Removes the specified node and all edges to and from it
        Raises if node is not present
        '''
        for v in self.nodes:
            v._adj.discard(node)
        self.nodes.remove(node)

    def add_edge(self, tail: NV, head: NV) -> None:
        '''
        Adds the specified edge
        Raises if it's already present
        '''
        if head in tail._adj:
            raise RuntimeError('Attempted to add a duplicate edge')
        tail._adj.add(head)

    def remove_edge(self, tail: NV, head: NV) -> None:
        '''
        Removes the specified edge
        Raises if it's not present
        '''
        tail._adj.remove(head)

    def __repr__(self) -> str:
        return f'<Graph with {len(self.nodes)} nodes>\nNodes: {self.nodes}'


def read_graph(s: Iterable[str], node_type: Callable[[str], NodeValue]) -> Graph[NodeValue]:
    g = Graph[NodeValue]()
    # we can't use Graph.NV instead of Graph.Node[NodeValue]
    # because type aliases cannot be qualified
    nodes: DefaultDict[str, Graph.Node[NodeValue]] = defaultdict(g.add_node)

    for line in s:
        print(line, end='')
        node_id, value, *neighbor_ids = line.split()
        nodes[node_id].value = node_type(value)
        for neighbor_id in neighbor_ids:
            g.add_edge(nodes[node_id], nodes[neighbor_id])
    return g


def write_graph(g: Graph[NodeValue]) -> str:
    output: List[str] = []
    nodes = {node: node_id for node_id, node in enumerate(g.nodes)}
    for node, node_id in nodes.items():
        output.append(str(node_id))
        output.append(' ' + str(node.value))
        output.extend([' ' + str(nodes[neighbor]) for neighbor in node._adj])
        output.append('\n')
    return ''.join(output)


def labeled_graph_eq(g1: Graph[NodeValue], g2: Graph[NodeValue]) -> bool:
    '''
    Compares two labeled graphs for equality
    Labels have to be hashable and unique
    '''

    if len(g1.nodes) != len(g2.nodes):
        return False
    labels1 = {node.value: node for node in g1.nodes}
    labels2 = {node.value: node for node in g2.nodes}
    if set(labels1) != set(labels2):
        return False
    # if labels not unique, we don't know the answer
    if len(labels1) != len(g1.nodes):
        raise NotImplementedError

    for label in labels1:
        node1 = labels1[label]
        node2 = labels2[label]
        if {n.value for n in node1._adj} != {n.value for n in node2._adj}:
            return False

    return True


def get_test_graph() -> Graph[str]:
    g = Graph[str]()
    a = g.add_node('A')
    b = g.add_node('B')
    c = g.add_node('C')
    g.add_node('D')
    g.add_edge(a, a)
    g.add_edge(a, b)
    g.add_edge(a, c)
    g.add_edge(c, b)
    return g


def test_labeled_eq() -> None:
    g1 = get_test_graph()
    g2 = get_test_graph()
    assert labeled_graph_eq(g1, g2)

    next(iter(g1.nodes)).value = 'Z'
    assert not labeled_graph_eq(g1, g2)


def test_serialization() -> None:
    g = get_test_graph()

    g_str = StringIO('''0 A 0 1 2
    1 B
    2 C 1
    3 D''')
    # annotated intermediate variable is needed to help type inference
    g1: Graph[str] = read_graph(g_str, str)
    assert labeled_graph_eq(g1, g)

    g1 = read_graph(StringIO(write_graph(g)), str)
    assert labeled_graph_eq(g1, g)
