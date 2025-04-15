import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()
        self.nerc=None

    def handleWorstCase(self, e):
        maxY=int(self._view._txtYears.value)
        maxH=int(self._view._txtHours.value)
        listaSol, persone, ore=self._model.worstCase(self.nerc,maxY, maxH)
        self._view._txtOut.controls.append(ft.Text(f"Persone affette: {persone}"))
        self._view._txtOut.controls.append(ft.Text(f"Ore: {ore}"))
        for i in listaSol:
            self._view._txtOut.controls.append(ft.Text(str(i)))
        self._view.update_page()

    def fillDD(self):
        nercList = self._model.listNerc
        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(key=n.value, data=n, on_click=self.salvaNerc))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v

    def salvaNerc(self,e):
        self.nerc=e.control.data
