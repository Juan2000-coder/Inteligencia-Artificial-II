#nodos
class Nodos:
    def _init_( self, _info, _coords):
        self.info = _info
        self.coords = _coords
        self.vecinos = []
        self.costo = 0
        self.heur = 0

    def get_vecinos(self):
        return self.vecinos
    
    def get_coords(self):
        return self.coords
    
    def set_vecinos(self,_vecinos):
        self.vecinos = _vecinos

    def set_costo(self,_costo):
        self.costo = _costo

    def set_heur(self,_heur):
        self.heur = _heur
    