class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = []
        l = self.obtineDrum()
        # print(l)
        if l == []:
            print("Nu exista solutie")
        nod1 = l[0]
        # print(str(nod1.info))
        nod1 = nod1.info
        for nod in l:
            # print(str(nod.info),end=" ")
            i,j = cautaPozElemMatr(rows,str(nod1))
            ii,jj = cautaPozElemMatr(rows,str(nod.info))
            if i == ii:
                if j < jj:
                    if j == 1 or j == 3:
                        print('>>', end = " ")
                    else:
                        print('>',end = " ")
                elif j > jj:
                    if j == 4 or j == 2:
                        print('<<', end=" ")
                    else:
                        print('<', end = " ")
            elif j == jj:
                if i < ii:
                    print('v',end = " ")
                elif i > ii:
                    print('^',end = " ")
            print(str(nod.info), end=" ")
            nod1 = nod.info
        print()
        print("Cost: ", self.g)
        print("Lungime: ", len(l))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if infoNodNou == nodDrum.info:
                return True
            nodDrum = nodDrum.parinte
        return False


    def __str__(self):
        return self.info


//returnez linia si coloana pe care se afla un element in matrice
def cautaPozElemMatr(matr, elemCautat):
    for i, linie in enumerate(matr):
        for j, elem in enumerate(linie):
            if elem == elemCautat:
                return i, j
    return -1,-1



class Graph:
    def __init__(self,nume_fisier):
        f = open(nume_fisier, "r")
        continut_fisier = f.read()

        lines = continut_fisier.split("suparati")
        r = lines[0].split("\n")

        # pun in lista self.randuri numele elevilor citite din fisier, fiecare rand in cate o lista
        randuri = []
        for i in r:
            if i != '':
                randuri.append(i.split(" "))
        #print("Randuri: ", randuri)

        lines = continut_fisier.split("mesaj:")
        mesaj = lines[1].split("->")
        suparati = []
        s = continut_fisier.split("suparati")
        s = s[1].split("\n")
        s.pop()
        for i in s:
            if i != '':
                suparati.append(i.split(" "))
        # print(mesaj)
        #print("Suparati: ", suparati)
        lastRow = len(randuri) - 1
        self.start = mesaj[0].strip()
        #print(self.start)
        #print(mesaj)
        self.mesaj = mesaj
        self.scop = mesaj[1].strip()
        self.randuri = randuri
        self.suparati = suparati
        #print("Mesajul trebuie sa ajunga de la",mesaj[0],"la",mesaj[1])


    def testeaza_scop(self,nodCurent):
        return nodCurent.info == self.scop

    def genereazaSuccesori(self,nodCurent,tip_euristica):
        listaSuccesori = []

        for i in range(len(self.randuri)):
            for j in range(6):
                if str(nodCurent) == self.randuri[i][j]:
                    coloana = j
                    rand = i
                    break

        if coloana == 0 or coloana == 2 or coloana == 4:
            if self.randuri[rand][coloana + 1] != 'liber':
                    nod_nou = NodParcurgere(
                        info = self.randuri[rand][coloana + 1],
                        parinte = nodCurent,
                        cost = nodCurent.g + 1,
                        h = self.calculeaza_h(self.randuri[rand][coloana + 1], tip_euristica)
                    )


                    if not nodCurent.contineInDrum(nod_nou.info):
                        listaSuccesori.append(nod_nou)


        elif coloana == 1 or coloana == 3 or coloana == 5:
            if self.randuri[rand][coloana - 1] != 'liber':
                    nod_nou = NodParcurgere(
                        self.randuri[rand][coloana - 1],
                        nodCurent,
                        nodCurent.g + 1,
                        h = self.calculeaza_h(self.randuri[rand][coloana - 1], tip_euristica)
                    )


                    if not nodCurent.contineInDrum(nod_nou.info):
                        listaSuccesori.append(nod_nou)
        if rand > 0:
            if self.randuri[rand - 1][coloana] != 'liber':
                    nod_nou = NodParcurgere(
                        self.randuri[rand - 1][coloana],
                        nodCurent,
                        nodCurent.g + 1,
                        h = self.calculeaza_h(self.randuri[rand - 1][coloana], tip_euristica)
                    )


                    if not nodCurent.contineInDrum(nod_nou.info):
                        listaSuccesori.append(nod_nou)
        lastRow = len(self.randuri) - 1
        if rand < lastRow:
            if self.randuri[rand + 1][coloana] != 'liber':
                    nod_nou = NodParcurgere(
                        self.randuri[rand + 1][coloana],
                        nodCurent,
                        nodCurent.g + 1,
                        h=self.calculeaza_h(self.randuri[rand + 1][coloana], tip_euristica)
                    )


                    if not nodCurent.contineInDrum(nod_nou.info):
                        listaSuccesori.append(nod_nou)

        if rand == lastRow or rand == lastRow - 1:
            if coloana == 1 or coloana == 3:
                if self.randuri[rand][coloana + 1] != 'liber':
                        nod_nou = NodParcurgere(
                            self.randuri[rand][coloana + 1],
                            nodCurent,
                            nodCurent.g + 1,
                            h=self.calculeaza_h(self.randuri[rand][coloana + 1], tip_euristica)
                        )

                        if not nodCurent.contineInDrum(nod_nou.info):
                            listaSuccesori.append(nod_nou)

        if rand == lastRow or rand == lastRow - 1:
            if coloana == 2 or coloana == 4:
                        nod_nou = NodParcurgere(
                            self.randuri[rand][coloana - 1],
                            nodCurent,
                            nodCurent.g + 1,
                            h=self.calculeaza_h(self.randuri[rand][coloana - 1], tip_euristica)
                        )

                        if not nodCurent.contineInDrum(nod_nou.info):
                            listaSuccesori.append(nod_nou)
        l = []
        for i in listaSuccesori:
            if [str(i.info),str(nodCurent)] not in self.suparati and [str(nodCurent),str(i.info)] not in self.suparati:
                l.append(i)
        return l


    def calculeaza_h(self, infoNod, tip_euristica):
        if tip_euristica == "euristica_banala":
            return self.euristica_banala(infoNod, tip_euristica)
        elif tip_euristica == "euristica_admisibila_1":
            return self.euristica_admisibila_1(infoNod, tip_euristica)
        elif tip_euristica == "euristica_admisibila_2":
            return self.euristica_admisibila_2(infoNod, tip_euristica)
        else:
            raise Exception("Aceasta euristica nu este definita")

    def euristica_banala(self, infoNod, tip_euristica):
        return 0 if infoNod == self.scop else 1



    def euristica_admisibila_1(self, infoNod, tip_euristica):
        if infoNod == self.scop:
            return 0
        iinfonod,jinfonod = cautaPozElemMatr(self.randuri,infoNod)
        iscop, jscop = cautaPozElemMatr(self.randuri, self.scop)
        # returnez maximul dintre numarul de linii de la nodul curent pana la nodul scop si numarul de coloane de la nodul curent pana la nodul scop
        return max(abs(iscop - iinfonod),abs(jscop - jinfonod))

    def euristica_neadmisibila(self,infoNod,tip_euristica):
        if infoNod == self.scop:
            return 0
        iscop,jscop = cautaPozElemMatr(self.randuri,self.scop)
        iinfoNod,jinfonod = cautaPozElemMatr(self.randuri,infoNod)
        nrRanduri = len(self.randuri) - 1
        return abs(nrRanduri - iinfoNod) + abs(jscop - jinfonod) + abs(nrRanduri - iscop)


    def euristica_admisibila_2(self, infoNod, tip_euristica):
        if infoNod == self.scop:
            return 0
        iscop,jscop = cautaPozElemMatr(self.randuri,self.scop)
        iinfoNod,jinfonod = cautaPozElemMatr(self.randuri,infoNod)
        return abs(iscop - iinfoNod) + abs(jscop - jinfonod) - 1





def a_star_optimizat(gr, tip_euristica):
    if verificareDate(gr.randuri,gr.mesaj,gr.suparati) == 0:
        print("date incorecte")
    else:
        c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica))]
        closed = []

        while len(c) > 0:
            nodCurent = c.pop(0)
            closed.append(nodCurent)

            if gr.testeaza_scop(nodCurent):
                print("Solutie: ")
                nodCurent.afisDrum(afisLung=True, afisCost=True)
                print("\n--------------------\n")
                return

            lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
            lSuccesoriCopy = lSuccesori.copy()
            for s in lSuccesoriCopy:
                gasitOpen = False
                for elem in c:
                    if s.info == elem.info:
                        gasitOpen = True
                        if s.f < elem.f:
                            c.remove(elem)
                        else:
                            lSuccesori.remove(s)
                        break
                if not gasitOpen:
                    for elem in closed:
                        if s.info == elem.info:
                            if s.f < elem.f:
                                closed.remove(elem)
                            else:
                                lSuccesori.remove(s)
                            break

            for s in lSuccesori:
                i = 0
                while i < len(c):
                    if c[i].f >= s.f:
                        break
                    i += 1
                c.insert(i, s)
            if c == []:
                print("Nu exista solutii!")

def uniform_cost(gr, nrSolutiiCautate,tip_euristica):
    if verificareDate(gr.randuri,gr.mesaj,gr.suparati) == 0:
        print("date incorecte")
    else:
        # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
        c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica))]

        while len(c) > 0:
            nodCurent = c.pop(0)

            if gr.testeaza_scop(nodCurent):
                print("Solutie: ")
                nodCurent.afisDrum()
                print("\n----------------\n")
                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return
            lSuccesori = gr.genereazaSuccesori(nodCurent,tip_euristica)
            for s in lSuccesori:
                i = 0
                gasit_loc = False
                for i in range(len(c)):
                    # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                    if c[i].g > s.g:
                        gasit_loc = True
                        break
                if gasit_loc:
                    c.insert(i, s)
                else:
                    c.append(s)
            if c == []:
                print("Nu exista solutii!")

def a_star(gr, nrSolutiiCautate,tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    if verificareDate(gr.randuri,gr.mesaj,gr.suparati) == 0:
        print("date incorecte")
    else:
        c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica))]
        while len(c) > 0:
            nodCurent = c.pop(0)

            if gr.testeaza_scop(nodCurent):
                print("Solutie: ")
                nodCurent.afisDrum()
                print("\n----------------\n")
                nrSolutiiCautate -= 1
                if nrSolutiiCautate == 0:
                    return
            lSuccesori = gr.genereazaSuccesori(nodCurent,tip_euristica)
            for s in lSuccesori:
                i = 0
                while i < len(c):
                    # diferenta fata de UCS e ca ordonez dupa f
                    if c[i].f >= s.f:
                        break
                    i += 1
                c.insert(i, s)
            if c == []:
                print("Nu exista solutii!")
def ida_star(gr, nrSolutiiCautate,tip_euristica):
    if verificareDate(gr.randuri,gr.mesaj,gr.suparati) == 0:
        print("date incorecte")
    else:
        limita = gr.calculeaza_h(gr.start,tip_euristica)
        nodStart = NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start, tip_euristica))
        while True:

            # print("Limita de pornire: ", limita)
            nrSolutiiCautate, rez = construieste_drum(
                gr, nodStart, limita, nrSolutiiCautate,tip_euristica
            )
            if rez == "gata":
                break
            if rez == float("inf"):
                print("Nu exista solutii!")
                break
            limita = rez
            # print(">>> Limita noua: ", limita)


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate,tip_euristica):
    # print("A ajuns la: ", nodCurent)
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f
    if gr.testeaza_scop(nodCurent) and nodCurent.f == limita:
        print("Solutie: ")
        nodCurent.afisDrum()
        print(limita)
        print("\n----------------\n")
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate, "gata"
    lSuccesori = gr.genereazaSuccesori(nodCurent,tip_euristica)
    minim = float("inf")
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate,tip_euristica)
        if rez == "gata":
            return nrSolutiiCautate, "gata"
        # print("Compara ", rez, " cu ", minim)
        if rez < minim:
            minim = rez
            # print("Noul minim: ", minim)
    return nrSolutiiCautate, minim




# Verific daca sunt cate 6 nume pe fiecare rand, daca in lista de suparati sunt trecuti cate 2 elevi si daca in lista mesaj sunt exact 2 nume (elevul de
# la care pleaca mesajul si elevul la care trebuie sa ajunga.)
def verificareDate(randuri,mesaj,suparati):
    for i in randuri:
        if len(i) != 6:
            return 0
    if len(mesaj) != 2:
        return 0
    for i in suparati:
        if len(i) != 2:
            return 0
    return 1

# print(verificareDate(rows))


gr = Graph("input3.txt")
rows = gr.randuri
gr2 = Graph("input3.txt")


a_star_optimizat(gr2,"euristica_banala")
uniform_cost(gr,10,"euristica_banala")
a_star(gr,2,"euristica_banala")
ida_star(gr,5,"euristica_banala")

a_star_optimizat(gr2,"euristica_admisibila_1")
uniform_cost(gr,10,"euristica_admisibila_1")
a_star(gr,2,"euristica_admisibila_1")
ida_star(gr,5,"euristica_admisibila_1")

a_star_optimizat(gr2,"euristica_admisibila_2")
uniform_cost(gr,10,"euristica_admisibila_2")
a_star(gr,2,"euristica_admisibila_2")
ida_star(gr,5,"euristica_admisibila_2")

g1 = open("output1.txt","w")
g2 = open("output2.txt","w")
g3 = open("output3.txt","w")
g4 = open("output4.txt","w")







