import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()

        self.id_map = {}
        self.map_title = {}
        self._nodes = []
        self._edges = []

        self.set_ottimo = []
        self.soluzione_best = []

    def crea_grafo(self,soglia):
        self.G.clear()
        print(soglia)
        lista_album = DAO.get_album_durata()
        #print(lista_album)
        for album in lista_album:
            self.id_map[album.id] = album
            self.map_title[album.title] = album

        #print(lista_album_durata)
        for album in lista_album:
            if (album.durata) > soglia:
                self._nodes.append(album)
        self.G.add_nodes_from(self._nodes)

        lista_connessioni = DAO.album_connessi()
        #print(self._nodes)
        #print(lista_connessioni)
        for connessione in lista_connessioni:
            album1 = self.id_map[connessione.album1]
            album2 = self.id_map[connessione.album2]


            if album1 in self._nodes and album2 in self._nodes:
                self.G.add_edge(album1, album2)





    def componente_connessa(self, album):
        """Restituisce la componente connessa di un album"""
        if album not in self.G:
            return []
        tree = nx.bfs_tree(self.G, album)
        nodi_raggiungibili = list(tree.nodes())
        return nodi_raggiungibili


    def estrazione_set_album(self, start_album, max_duration):
        """Ricerca ricorsiva del set massimo di album nella componente connessa"""
        component = self.componente_connessa(start_album)
        self.soluzione_best = []
        self._ricorsione(component, [start_album], start_album.durata, max_duration)
        return self.soluzione_best


    def _ricorsione(self, albums, current_set, current_duration, max_duration):
        if len(current_set) > len(self.soluzione_best):
            self.soluzione_best = current_set.copy()

        for album in albums:
            if album in current_set:
                continue
            new_duration = current_duration + album.durata
            if new_duration <= max_duration:    #<=
                current_set.append(album)
                self._ricorsione(albums, current_set, new_duration, max_duration)
                current_set.pop()







