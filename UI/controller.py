import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        self._view.lista_visualizzazione_1.clean()
        try:
            durata = float(self._view.txt_durata.value)
            if durata < 0:
                self._view.show_alert("Durata non valida")
                return
            self._model.crea_grafo(durata)
            album = self._model.G.number_of_nodes()
            archi = self._model.G.number_of_edges()
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Grafo creato: {album} album, {archi} archi'))

            for nodo in self._model.G.nodes():
                    self._view.dd_album.options.append(ft.dropdown.Option(nodo.title))

            self._view.update()
        except ValueError:
            self._view.show_alert('Inserire una durata valida')

        self._view.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # TODO
        title = e.control.value
        self._selected_album = next((a for a in self._model.G.nodes() if a.title == title), None)

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        # TODO
        if not self._selected_album:
            self._view.show_alert("Selezionare un album")
            return

        self._view.lista_visualizzazione_2.clean()
        durata = 0
        lista_connessi = self._model.componente_connessa(self._selected_album)
        dimensione = len(lista_connessi)
        for album in lista_connessi:
            durata += album.durata

        print(f'{durata:.2f}')

        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Dimensione componente: {dimensione} \n'
                                                                   f'durata: {durata:.2f} minuti'))

        self._view.update()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO
        try:
            durataTot = float(self._view.txt_durata_totale.value)
            if durataTot < 0:
                self._view.show_alert("Durata non valida")
                return
            a1 = self._view.dd_album.value
            album = self._model.map_title[a1]
            lista = self._model.estrazione_set_album(album, durataTot)
            durata = sum(album.durata for album in lista)
            self._view.lista_visualizzazione_3.clean()
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f'Set trovato ({len(lista)} album, {durata:.2f} minuti):'))
            for a in lista:
                self._view.lista_visualizzazione_3.controls.append(ft.Text(f'-{a.title} ({a.durata:.2f} min)'))


            self._view.update()




        except ValueError:
            self._view.show_alert('Inserire una durata valida')