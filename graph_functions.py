# module: graph_functions.py
from typing import (
    TypeVar, Generic, List, Set, Dict, Callable, DefaultDict, Iterable,
    Any, Type
)
from collections import defaultdict
from io import StringIO
from igraph import IGraph, IGraphMutable, INode, INodeMutable

G = TypeVar('G', bound=IGraphMutable)


def read_graph(cls: Type[G], s: Iterable[str], node_type: Callable[[str], Any]) -> G:
    g = cls()
    # we can't use Graph.Node instead of Graph.Node
    # because type aliases cannot be qualified
    nodes: DefaultDict[str, INodeMutable] = defaultdict(g.add_node)

    for line in s:
        print(line, end='')
        node_id, value, *neighbor_ids = line.split()
        nodes[node_id].value = node_type(value)
        for neighbor_id in neighbor_ids:
            g.add_edge(nodes[node_id], nodes[neighbor_id])
    return g


def write_graph(g: IGraph) -> str:
    output: List[str] = []
    nodes = {node: node_id for node_id, node in enumerate(g.nodes)}
    for node, node_id in nodes.items():
        output.append(str(node_id))
        output.append(' ' + str(node.value))
        output.extend([' ' + str(nodes[neighbor]) for neighbor in node.adj])
        output.append('\n')
    return ''.join(output)


def labeled_graph_eq(g1: IGraph, g2: IGraph) -> bool:
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
        if {n.value for n in node1.adj} != {n.value for n in node2.adj}:
            return False

    return True


def get_test_graph(cls: Type[G]) -> G:
    g = cls()
    a = g.add_node('A')
    b = g.add_node('B')
    c = g.add_node('C')
    g.add_node('D')
    g.add_edge(a, a)
    g.add_edge(a, b)
    g.add_edge(a, c)
    g.add_edge(c, b)
    return g


def generic_test_labeled_eq(cls: Type[G]) -> None:
    g1 = get_test_graph(cls)
    g2 = get_test_graph(cls)
    assert labeled_graph_eq(g1, g2)

    next(iter(g1.nodes)).value = 'Z'
    assert not labeled_graph_eq(g1, g2)


def generic_test_serialization(cls: Type[G]) -> None:
    g = get_test_graph(cls)

    g_str = StringIO('''0 A 0 1 2
    1 B
    2 C 1
    3 D''')
    assert labeled_graph_eq(read_graph(cls, g_str, str), g)
    assert labeled_graph_eq(read_graph(cls, StringIO(write_graph(g)), str), g)
