from typing import (
    TypeVar, Generic, Set, List, Callable, Dict, Optional, DefaultDict
)
from collections import defaultdict

NodeValue = TypeVar('NodeValue')


class Node(Generic[NodeValue]):
    def __init__(self, value: Optional[NodeValue] = None) -> None:
        self.value = value

    def __repr__(self) -> str:
        return '<Node ' + str(self.value) + '>'


Graph = Dict[Node[NodeValue], Set[Node[NodeValue]]]


def read_graph(s: str, node_type: Callable[[str], NodeValue]) -> Graph[NodeValue]:
    '''
    Args:
    s: graph in serialized format
    one line per node: node_id node_value neighbor1_id neighbor2_id ...
    leading/trailing/repeated whitespace ignored
    node_id must be integers

    Returns:
    graph constructed from input if input is valid
    on bad input, may raise or return corrupt graph
    '''

    g: Graph[NodeValue] = {}
    nodes: DefaultDict[int, Node[NodeValue]] = defaultdict(Node)
    for line in s.splitlines():
        node_id, value, *neighbor_ids = line.split()
        node = nodes[int(node_id)]
        node.value = node_type(value)
        neighbors = map(lambda neighbor_id: nodes[int(neighbor_id)], neighbor_ids)
        g[node] = set(neighbors)
    return g


def write_graph(g: Graph[NodeValue]) -> str:
    output: List[str] = []
    nodes = {node: node_id for node_id, node in enumerate(g)}
    for node, node_id in nodes.items():
        output.append(str(node_id))
        output.append(' ' + str(node.value))
        output.extend([' ' + str(nodes[neighbor]) for neighbor in g[node]])
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
        if {n.value for n in g1[node1]} != {n.value for n in g2[node2]}:
            return False

    return True


def get_test_graph() -> Graph[str]:
    a = Node('A')
    b = Node('B')
    c = Node('C')
    d = Node('D')
    return {a: {a, b, c}, b: set(),
            c: {b}, d: set()}


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
