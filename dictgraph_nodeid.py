from typing import (
    Dict, Set, List
)

Graph = Dict[int, Set[int]]


def read_graph(s: str) -> Graph:
    '''
    Args:
    s: graph in serialized format
    one line per node: node_id neighbor1_id neighbor2_id ...
    leading/trailing/repeated whitespace ignored

    Returns:
    graph constructed from input if input is valid
    on bad input, may raise or return corrupt graph
    '''

    g: Graph = {}
    for line in s.splitlines():
        node, *neighbors = map(int, line.split())
        g[node] = set(neighbors)
    return g


def write_graph(g: Graph) -> str:
    '''
    Serializes graph in the format described in read_graph
    '''

    # growing a string is quadratic runtime in string length
    # growing a list and join at the end is linear
    output: List[str] = []
    for node in range(len(g)):
        output.append(str(node))
        neighbors = g[node]
        output.extend([' ' + str(neighbor) for neighbor in neighbors])
        output.append('\n')
    return ''.join(output)


def test_serialization() -> None:
    graph: Graph = {0: {0, 1, 2}, 1: set(), 2: {1}, 3: set()}
    g_str = '''0 0 1 2
    1
    2 1
    3'''

    assert read_graph(g_str) == graph
    assert read_graph(write_graph(graph)) == graph
