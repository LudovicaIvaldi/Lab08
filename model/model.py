import copy

from database.DAO import DAO


class Model:
    def __init__(self):
        self.ore_totali = None
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self.maxPersone=-1




    def worstCase(self, nerc, maxY, maxH):
        self._solBest = []
        self.maxPersone=-1
        self.loadEvents(nerc)
        self.ricorsione([], maxY, maxH, self._listEvents)
        print (self._solBest, self.maxPersone, self.ore_totali)
        self._solBest.sort(key=lambda x: x.id)
        return self._solBest, self.maxPersone, self.ore_totali

    def is_admissible(self,parziale,e, maxY, maxH):
        #ritorna true se e può essere messo dentro alla lista parziale
        oreTotali=0
        for i in parziale:
            oreTotali += ((i.date_event_finished - i.date_event_began).total_seconds())/3600
        if (oreTotali+ (((e.date_event_finished - e.date_event_began).total_seconds())/3600)) > maxH:
            return False
        parziale.append(e)
        anni=[]
        for i in parziale:
            anni.append(i.date_event_finished.year)
        annomax= max(anni)
        annomin= min(anni)
        if annomax-annomin>maxY:
            parziale.remove(e)
            return False
        parziale.remove(e)
        return True


    def is_finish(self, parziale, listaEventi, maxY, maxH):
        #ritorna false se trova un evento e che puoi aggiungere nella lista parziale
        #ritorna true se è finito -> non puoi aggiunger nessun e dentro al parziale
        for e in listaEventi:
            if e not in parziale:
                if self.is_admissible(parziale,e,maxY,maxH):
                    return False
        return True


    def calcola_persone(self,parziale):
        tot=0
        for e in parziale:
            tot += e.customers_affected
        return tot

    def calcola_oreTotali(self,parziale):
        self.ore_totali=0
        for e in parziale:
            self.ore_totali += (e.date_event_finished-e.date_event_began).total_seconds()/3600


    def ricorsione(self, parziale, maxY, maxH, listaEventi):
        if self.is_finish(parziale,listaEventi,maxY, maxH):
            if self.calcola_persone(parziale)>self.maxPersone or self.maxPersone==-1:
                self._solBest=(copy.deepcopy(parziale))
                self.maxPersone=self.calcola_persone(parziale)
                self.calcola_oreTotali(parziale)
                #print(parziale)
                #print(self._solBest)
                #print(self.maxPersone)
        else:
            for e in listaEventi:
                if self.is_admissible(parziale, e, maxY, maxH) and e not in parziale:
                    parziale.append(e)
                    self.ricorsione(parziale, maxY, maxH, listaEventi)
                    parziale.pop()



    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()
        self._listNerc.sort(key=lambda x: x.value)


    @property
    def listNerc(self):
        return self._listNerc


