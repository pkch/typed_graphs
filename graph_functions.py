# module: graph_functions.py
from typing import (
    TypeVar, Generic, List, Set, Dict, Callable, DefaultDict, Iterable,
    Any, Type
)
from collections import defaultdict
from io import StringIO
import re
import pytest  # type: ignore
from igraph import IGraph, IGraphMutable, INode, INodeMutable, InvalidOperation

G = TypeVar('G', bound=IGraphMutable)


def read_graph(cls: Type[G], s: Iterable[str], node_type: Callable[[str], Any]) -> G:
    g = cls()
    nodes: DefaultDict[str, INodeMutable] = defaultdict(g.add_node)

    for line in s:
        node_id, value, *neighbor_ids = line.split()
        nodes[node_id].value = node_type(value)
        for neighbor_id in neighbor_ids:
            try:
                g.add_edge(nodes[node_id], nodes[neighbor_id])
            except InvalidOperation:
                pass  # ignore duplicate edges (common in undirected graphs)
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
    if cls.allow_loops:
        g.add_edge(a, a)
    g.add_edge(a, b)
    g.add_edge(a, c)
    try:
        g.add_edge(c, a)
    except InvalidOperation:
        # only add reverse edge to directed graphs
        pass
    g.add_edge(c, b)

    return g


def get_test_serialized_graph(cls: Type[G]) -> StringIO:
    s = '0 A 0 1 2\n' if cls.allow_loops else '0 A 1 2\n'
    s += '''1 B
    2 C 0 1
    3 D'''
    return StringIO(s)


def generic_test_basic_functions(cls: Type[G]) -> None:
    g = cls()
    v = g.add_node()
    w = g.add_node()
    g.add_edge(v, w)
    with pytest.raises(InvalidOperation):
        g.add_edge(v, w)

    g = get_test_graph(cls)
    assert str(g).startswith('<Graph with 4 nodes>\n')

    node_str = {re.sub(r' at \d+', '', str(node)) for node in g.nodes}
    assert node_str == {'<Node A>', '<Node B>', '<Node C>', '<Node D>'}
    for v in list(g.nodes):  # need list(), otherwise set changes during iteration
        g.remove_node(v)
    assert len(g.nodes) == 0

    g = get_test_graph(cls)
    for v in g.nodes:
        for w in list(v.adj):
            g.remove_edge(v, w)
    for v in g.nodes:
        assert len(list(v.adj)) == 0


def generic_test_labeled_eq(cls: Type[G]) -> None:
    g1 = get_test_graph(cls)
    g2 = get_test_graph(cls)
    assert labeled_graph_eq(g1, g2)

    nodes = sorted(g1.nodes, key=lambda node: len(node.adj))
    # ensure we swap non-equivalent nodes
    # works for both directed and undirected graphs,
    # since our test graph has one node with 0 degree
    nodes[0].value, nodes[-1].value = nodes[-1].value, nodes[0].value
    assert not labeled_graph_eq(g1, g2)

    g1 = get_test_graph(cls)
    nodes = list(g1.nodes)
    nodes[0].value = 'Z'
    assert not labeled_graph_eq(g1, g2)

    for node in g1.nodes:
        node.value = 'Z'
    for node in g2.nodes:
        node.value = 'Z'
    with pytest.raises(NotImplementedError):
        labeled_graph_eq(g1, g2)

    g1.remove_node(nodes[0])
    assert not labeled_graph_eq(g1, g2)


def generic_test_serialization(cls: Type[G]) -> None:
    g = get_test_graph(cls)
    g_str = get_test_serialized_graph(cls)
    assert labeled_graph_eq(read_graph(cls, g_str, str), g)
    assert labeled_graph_eq(read_graph(cls, StringIO(write_graph(g)), str), g)


generic_tests = [generic_test_basic_functions, generic_test_labeled_eq,
                 generic_test_serialization]
