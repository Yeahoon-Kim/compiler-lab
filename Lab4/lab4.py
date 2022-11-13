import sys

class Parser:
    def __init__(self, fp_):
        self.m_lRules = []
        self.m_dFirst = {}
        self.m_dFollow = {}
        self.m_sStart = ""
        self.m_dM = {}
        if(fp_ != 0):
            for line in fp_:
                elem = line[0:-1].split(" ")
                if(len(elem)==1):
                    elem.append("")
                self.m_lRules.append((elem[0], elem[1]))
                self.m_dFirst[elem[1]] = set()
                self.m_dFollow[elem[0]] = set()
                if(self.m_sStart == ""):
                    self.m_sStart = elem[0]
    def getFirst(self, a_):
        r = set()
        if(a_==""):
            r.add("")
        elif(not a_[0].isupper()):
            r.add(a_[0])
        elif(a_[0].isupper()):
            x = set()
            for l in self.m_lRules:
                if(l[0]==a_[0]):
                    x |= self.getFirst(l[1])
            r |= x
            if("" in x):
                r.remove("")
                if(len(a_)>1):
                    r |= self.getFirst(a_[1:])
                else:
                    r.add("")
        return r
    def getFollow(self, a_):
        r = set()
        if(a_ == self.m_sStart):
            r.add("$")
        for l in self.m_lRules:
            for i in range(len(l[1])):
                if(l[1][i]==a_):
                    if(i<(len(l[1])-1)):
                        t = self.getFirst(l[1][i+1:])
                        if("" in t):
                            t.remove("")
                            if(l[0] != a_):
                                r |= self.getFollow(l[0])
                        r |= t
                    else:
                        if(l[0] != a_):
                            r |= self.getFollow(l[0])
        return r
    def computeFirst(self):
        for k in self.m_dFirst:
            self.m_dFirst[k] = self.getFirst(k)
    def computeFollow(self):
        for k in self.m_dFollow:
            self.m_dFollow[k] = self.getFollow(k)
    def initTable(self):
        for l in self.m_lRules: self.m_dM[l[0]] = {}

        for [A, alpha] in self.m_lRules:
            first = self.m_dFirst[alpha]

            for a in first:
                if a != '': self.m_dM[A][a] = (A, alpha)

            if '' in first:
                follow = self.m_dFollow[A]

                for b in follow:
                    if b != '':
                        self.m_dM[A][b] = (A, alpha)

        return
    def printRules(self):
        for r in self.m_lRules:
            print("%s=>%s" % (r[0], r[1]))
    def printFirst(self):
        for k in self.m_dFirst:
            print("First(%s) = {%s}" % (k, ",".join(self.m_dFirst[k])))
    def printFollow(self):
        for k in self.m_dFollow:
            print("Follow(%s) = {%s}" % (k, ",".join(self.m_dFollow[k])))
    def printTable(self):
        for n in self.m_dM:
            for s in self.m_dM[n]:
                print("M[%s][%s] = %s=>%s" % (n, s, self.m_dM[n][s][0], self.m_dM[n][s][1]))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("Usage: python %s <input file>" % sys.argv[0])
    fp = open(sys.argv[1], "r")
    LL = Parser(fp)

    LL.computeFirst()
    LL.computeFollow()
    LL.initTable()
    LL.printTable()