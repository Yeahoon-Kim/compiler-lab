import sys

class Parser:
    def __init__(self, fp_):
        self.m_lRules = []
        self.m_dFirst = {}
        self.m_dFollow = {}
        self.m_sStart = ""

        if (fp_ != 0):
            for line in fp_:
                elem = line[0:-1].split(" ")
                if (len(elem) == 1): elem.append("")

                self.m_lRules.append((elem[0], elem[1]))
                self.m_dFirst[elem[1]] = set()
                self.m_dFollow[elem[0]] = set()
                if (self.m_sStart == ""): self.m_sStart = elem[0]

    def getFirst(self, a_):
        r = set()

        # FIRST(e) = {e}
        if len(a_) == 0: r.add("")

        # FIRST(a) = {a}
        elif not a_[0].isupper(): r.add(a_[0])

        else:
            isEpsilonPossible = False

            for a in a_:
                isEpsilonPossible = False

                if not a.isupper(): r.add(a) # add FIRST(a) to FIRST(A)
                else:
                    for order in self.m_lRules:
                        if order[0] == a:
                            x = self.getFirst(order[1])
                            if "" not in x: r |= x
                            else:
                                isEpsilonPossible = True
                                r |= (x - {""})

                if not isEpsilonPossible: break
            if isEpsilonPossible: r.add("")
        return r


    def getFollow(self, a_):
        r = set()

        if a_ == self.m_sStart: r.add('$')

        for order in self.m_lRules:
            idx = order[1].find(a_)
            if idx == -1: continue

            beta = order[1][idx + 1:]
            firstBeta = self.getFirst(beta)
            if beta:
                r |= (firstBeta - {''})
                if "" in firstBeta and order[0] != a_:
                    r |= self.getFollow(order[0])
            elif order[0] != a_:
                r |= self.getFollow(order[0])

        return r

    def computeFirst(self):
        for k in self.m_dFirst:
            self.m_dFirst[k] = self.getFirst(k)

    def computeFollow(self):
        for k in self.m_dFollow:
            self.m_dFollow[k] = self.getFollow(k)

    def printRules(self):
        for r in self.m_lRules:
            print("%s=>%s" % (r[0], r[1]))

    def printFirst(self):
        for k in self.m_dFirst:
            print("First(%s) = {%s}" % (k, ",".join(self.m_dFirst[k])))

    def printFollow(self):
        for k in self.m_dFollow:
            print("Follow(%s) = {%s}" % (k, ",".join(self.m_dFollow[k])))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: python %s <input file>" % sys.argv[0])
    fp = open(sys.argv[1], "r")
    LL = Parser(fp)

    LL.computeFirst()
    LL.computeFollow()
    LL.printFirst()
    LL.printFollow()