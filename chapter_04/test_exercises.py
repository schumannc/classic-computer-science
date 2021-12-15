from graph import Graph
from digraph import DiGraph
from edge import Edge

def test_remove_vertex():
    g = Graph([0, 1, 2, 3])
    g.add_edge_by_vertices(0, 1)
    g.add_edge_by_vertices(2, 1)
    g.add_edge_by_vertices(3, 1)
    g.add_edge_by_vertices(2, 3) 
    g.add_edge_by_vertices(0, 2) 
    g.add_edge_by_vertices(0, 3) 
    g.remove_vertex(1)
    g.remove_vertex(0)
    assert g._vertices == [2, 3]
    assert g._edges == [[Edge(2, 3)], [Edge(3, 2)]]


def test_remove_edge():
    g = Graph([0, 1, 2, 3])
    g.add_edge_by_vertices(0, 1)
    g.add_edge_by_vertices(2, 1)
    g.add_edge_by_vertices(0, 2) 
    g.add_edge_by_vertices(0, 3) 
    g.remove_edge(Edge(0, 1))
    g.remove_edge(Edge(0, 2))
    assert g._vertices == [0, 1, 2, 3]
    assert g._edges == [[Edge(0, 3)], [Edge(1, 2)], [Edge(2, 1)], [Edge(3, 0)]]


def test_digraph():
    g = DiGraph([0, 1, 2, 3])
    g.add_edge_by_vertices(0, 1)
    g.add_edge_by_vertices(2, 1)
    assert g._edges == [[Edge(0, 1)], [], [Edge(2, 1)], []]
