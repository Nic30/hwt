from typing import Generator


def _tarjan_head(index, lowlink, S, S_set, T, g, v):
    lowlink[v] = index[v] = len(index)
    S.append(v)
    S_set.add(v)
    it = iter(g.get(v, ()))
    T.append((it, False, v, None))


class StronglyConnectedComponentSearchTarjan():
    """
    Tarjan's strongly connected component search graph algorithm for DAGs
    
    based on https://github.com/bwesterb/py-tarjan
    """

    def __init__(self, g: dict):
        """
        :param g: graph represented as a dictionary { <vertex> : <successors of vertex> }.
        :note: vertex type does not matter but it has to be hashable (implement __eq__ and __hash__)
        """
        self.g = g

    def search_strongly_connected_components(self) -> Generator:
        """
        yields the strongly connected components of the graph in a topological order.
        """
        g = self.g # the graph
        S = [] # The main stack of the alg.
        S_set = set() # == set(S) for performance
        index = {} # { v : <index of v> }
        lowlink = {} # { v : <lowlink of v> }
        T = [] # stack to replace recursion
        main_iter = iter(g)
        for v in main_iter:
            if v not in index:
                _tarjan_head(index, lowlink, S, S_set, T, g, v)

            while T:
                it, inside, v, w = T.pop()
                if inside:
                    lowlink[v] = min(lowlink[w], lowlink[v])

                body_break = False
                for w in it:
                    if w not in index:
                        T.append((it, True, v, w))
                        _tarjan_head(index, lowlink, S, S_set, T, g, w)
                        body_break = True
                        break

                    if w in S_set:
                        lowlink[v] = min(lowlink[v], index[w])

                if body_break:
                    continue

                if lowlink[v] == index[v]:
                    scc = []
                    w = None
                    while v != w:
                        w = S.pop()
                        scc.append(w)
                        S_set.remove(w)

                    yield scc
