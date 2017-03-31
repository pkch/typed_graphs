from typing import (
    TypeVar, Generic, Set, List, Callable, Dict, Optional, DefaultDict, Iterator
)
from collections import defaultdict


NodeValue = TypeVar('NodeValue')


class Node(Generic[NodeValue]):
    # forward reference because Node isn't yet known to python runtime
    adj: 'Set[Node[NodeValue]]'

    def __init__(self, value: Optional[NodeValue] = None) -> None:
        self.value = value
        self.adj = set()

    def __repr__(self) -> str:
        return '<Node ' + str(self.value) + '>'


Graph = Set[Node[NodeValue]]


def read_graph(s: str, node_type: Callable[[str], NodeValue]) -> Graph[NodeValue]:
    g: Graph[NodeValue] = set()
    nodes: DefaultDict[int, Node[NodeValue]] = defaultdict(Node)
    for line in s.splitlines():
        node_id, value, *neighbor_ids = line.split()
        node = nodes[int(node_id)]
        g.add(node)
        node.value = node_type(value)
        neighbors = map(lambda neighbor_id: nodes[int(neighbor_id)], neighbor_ids)
        node.adj = set(neighbors)
    return g


def write_graph(g: Graph[NodeValue]) -> str:
    output: List[str] = []
    nodes = {node: node_id for node_id, node in enumerate(g)}
    for node, node_id in nodes.items():
        output.append(str(node_id))
        output.append(' ' + str(node.value))
        output.extend([' ' + str(nodes[neighbor]) for neighbor in node.adj])
        output.append('\n')
    return ''.join(output)


def labeled_graph_eq(g1: Graph[NodeValue], g2: Graph[NodeValue]) -> bool:
    '''
    Compares two labeled graphs for equality
    Labels have to be hashable and unique
    '''

    if len(g1) != len(g2):
        return False
    labels1 = {node.value: node for node in g1}
    labels2 = {node.value: node for node in g2}
    if set(labels1) != set(labels2):
        return False
    # if labels not unique, we don't know the answer
    if len(labels1) != len(g1):
        raise NotImplementedError

    for label in labels1:
        node1 = labels1[label]
        node2 = labels2[label]
        if {n.value for n in node1.adj} != {n.value for n in node2.adj}:
            return False

    return True


def get_test_graph() -> Graph[str]:
    a = Node('A')
    b = Node('B')
    c = Node('C')
    d = Node('D')
    a.adj = {a, b, c}
    c.adj = {b}
    return {a, b, c, d}


def test_labeled_eq() -> None:
    g1 = get_test_graph()
    g2 = get_test_graph()
    assert labeled_graph_eq(g1, g2)

    next(iter(g1)).value = 'Z'
    assert not labeled_graph_eq(g1, g2)


def test_serialization() -> None:
    g = get_test_graph()

    g_str = '''0 A 0 1 2
    1 B
    2 C 1
    3 D'''

    assert labeled_graph_eq(read_graph(g_str, str), g)
    assert labeled_graph_eq(read_graph(write_graph(g), str), g)