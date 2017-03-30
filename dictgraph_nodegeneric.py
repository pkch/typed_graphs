from typing import TypeVar, Dict, Set, Callable, List

Node = TypeVar('Node')
Graph = Dict[Node, Set[Node]]


def read_graph(s: str, node_type: Callable[[str], Node]) -> Graph[Node]:
    g: Graph[Node] = {}
    for line in s.splitlines():
        node, *neighbors = map(node_type, line.split())
        g[node] = set(neighbors)
    return g


def write_graph(g: Graph[Node]) -> str:
    output: List[str] = []
    for node, neighbors in g.items():
        output.append(str(node))
        output.extend([' ' + str(neighbor) for neighbor in neighbors])
        output.append('\n')
    return ''.join(output)


def test_graph():
    graph: Graph[str] = {'A': {'A', 'B', 'C'}, 'B': set(),
                         'C': {'B'}, 'D': set()}

    g_str = '''A A B C
    B
    C B
    D'''

    assert read_graph(g_str, str) == graph
    assert read_graph(write_graph(graph), str) == graph
