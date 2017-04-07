from typing import (
    TypeVar, Dict, Set, Callable, List, NamedTuple, Generic, DefaultDict
)

from collections import defaultdict

Node = TypeVar('Node')


# mypy type checker doesn't support generic NamedTuple yet, so we need our own class
# all good, this way we have even greater control over the API
class Adjacency(Generic[Node]):
    forward: Set[Node]
    backward: Set[Node]

    # there's no point adding forward/backward args to constructor
    # normally we create all the nodes first, and only then add edges, since
    # some of the edges lead to or from nodes that weren't created yet
    def __init__(self) -> None:
        self.forward = set()
        self.backward = set()

    # we need this to compare graphs
    def __eq__(self, rhs: object) -> bool:
        return (isinstance(rhs, Adjacency) and
                self.backward == rhs.backward and
                self.forward == rhs.forward)

    # for debugging only
    def __repr__(self) -> str:
        return ('forward: ' + repr(self.forward) +
                '; backward: ' + repr(self.backward))


Graph = Dict[Node, Adjacency[Node]]


def add_edge(g: Graph[Node], tail: Node, head: Node) -> None:
    g[tail].forward.add(head)
    g[head].backward.add(tail)


def remove_edge(g: Graph[Node], tail: Node, head: Node) -> None:
    g[tail].forward.remove(head)
    g[head].backward.remove(tail)


def read_graph(s: str, node_type: Callable[[str], Node]) -> Graph[Node]:
    g: Graph[Node] = defaultdict(Adjacency)
    for line in s.splitlines():
        node, *neighbors = map(node_type, line.split())
        g[node]  # to add a node in case it has no edges
        for neighbor in neighbors:
            add_edge(g, node, neighbor)
    g.default_factory = None  # type: ignore
    return g


def write_graph(g: Graph[Node]) -> str:
    output: List[str] = []
    for node, adjacency in g.items():
        output.append(str(node))
        output.extend([' ' + str(neighbor) for neighbor in adjacency.forward])
        output.append('\n')
    return ''.join(output)


def test_serialization() -> None:
    graph: Graph[str] = {'A': Adjacency(), 'B': Adjacency(),
                         'C': Adjacency(), 'D': Adjacency()}
    graph['A'].forward = {'A', 'B', 'C'}
    graph['A'].backward = {'A'}
    graph['B'].backward = {'A', 'C'}
    graph['C'].forward = {'B'}
    graph['C'].backward = {'A'}

    g_str = '''A A B C
    B
    C B
    D'''

    assert read_graph(g_str, str) == graph
    assert read_graph(write_graph(graph), str) == graph
