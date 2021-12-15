from graph import Graph
from itertools import product

if __name__ == '__main__':
    # Euler observed that (except at the endpoints of the walk), 
    # whenever one enters a vertex by a bridge, one leaves the
    # vertex by a bridge. In other words, during any walk in 
    # the graph, the number of times one enters a non-terminal 
    # vertex equals the number of times one leaves it.
    print('Seven Bridges of Königsberg')
    
    g = Graph([0,1,2,3])
    g.add_edge_by_vertices(0, 1)
    g.add_edge_by_vertices(1, 0)
    g.add_edge_by_vertices(0, 2)
    g.add_edge_by_vertices(2, 0)
    g.add_edge_by_vertices(0, 3)
    g.add_edge_by_vertices(1, 3)
    g.add_edge_by_vertices(2, 3)

    sizes = [len(e) for e in g._edges]
    print('edges sizes:', sizes)
    even, odd = 0, 0
    for s in sizes:
        if s == 0: break # did not cross all bridges
        if s % 2 == 0:
            odd += 1
        else:
            even += 1

    if even == len(g._vertices) - 2:
        print(f'prof solution #odds {odd} #evens {even}')
    else:
        print('non prof solution')

    print('Simpler problem')
    g = Graph([0,1,2,3])
    g.add_edge_by_vertices(0, 1)
    g.add_edge_by_vertices(1, 0)
    g.add_edge_by_vertices(0, 2)
    g.add_edge_by_vertices(2, 0)
    g.add_edge_by_vertices(0, 3)
    
    sizes = [len(e) for e in g._edges]
    print('edges sizes:', sizes)
    even, odd = 0, 0
    for s in sizes:
        if s == 0: break # did not cross all bridges
        if s % 2 == 0:
            odd += 1
        else:
            even += 1
  
    if even == len(g._vertices) - 2:
        print(f'prof solution #odds {odd} #evens {even}')
    else:
        print('non prof solution')
    