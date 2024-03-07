#nodos
class Nodos:
    def _init_( self, _info, _coords, _costo, _heur):
        self.info = _info
        self.coords = _coords
        self.vecinos = []
        self.costo = _costo
        self.heur = _heur

    def get_vecinos(self):
        return self.vecinos
    
    def set_vecinos(self,_vecinos):
        self.vecinos = _vecinos
    