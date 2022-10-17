from pydoc import doc
import sys


class Edge:
    def __init__(self, f_, t_, i_):
        self.m_nFrom = f_
        self.m_nTo = t_
        self.m_sInput = i_

    def print(self):
        print("%d,%d,%s" % (self.m_nFrom, self.m_nTo, self.m_sInput))


class Graph:
    def __init__(self, fp_=0):
        self.m_lEdges = []
        if (fp_ != 0):
            for line in fp_:
                elem = line[0:-1].split(',')
                self.m_lEdges.append(Edge(int(elem[0]), int(elem[1]), elem[2]))

    def getEClosureS(self, s_):
        r = set()
        r.add(s_)
        for e in self.m_lEdges:
            if (e.m_nFrom == s_ and e.m_sInput == ''):
                r.add(e.m_nTo)
                r |= self.getEClosureS(e.m_nTo)
        return r

    def getEClosureT(self, t_):
        r = set()
        for s in t_:
            r |= self.getEClosureS(s)
        return r

    def getMove(self, t_, a_):
        r = set()
        for s in t_:
            for e in self.m_lEdges:
                if (e.m_nFrom == s and e.m_sInput == a_):
                    r.add(e.m_nTo)
        return r

    def addEdge(self, f_, t_, i_):
        self.m_lEdges.append(Edge(f_, t_, i_))

    def print(self):
        for e in self.m_lEdges:
            e.print()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: python %s <input file>" % sys.argv[0])

    fp = open(sys.argv[1], "r")
    NFA = Graph(fp)
    DFA = Graph()
    Dstate = []
    T = 0

    Dstate.append(NFA.getEClosureS(0))
    # TODO
    sigma = {edge.m_sInput for edge in NFA.m_lEdges if edge.m_sInput}
    sigma = list(sigma)
    sigma.sort()

    for idx, oneState in enumerate(Dstate):
        T = idx

        for a in sigma:
            toDState = NFA.getEClosureT(NFA.getMove(oneState, a))

            if toDState not in Dstate:
                Dstate.append(toDState)
            DFA.addEdge(T, Dstate.index(toDState), a)

    DFA.print()