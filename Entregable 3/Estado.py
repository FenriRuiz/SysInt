import hashlib
import math

class Estado:
    def __init__(self, nodoActual, nodosPendientes):
        self.nodoActual = nodoActual
        self.listaPendientes = nodosPendientes
        self.identificador = self.serializar()

    def serializar(self):
        h = hashlib.md5() 
        h.update(self.nodoActual.encode())
        for nodo in self.listaPendientes:
            h.update(nodo.encode())
        return h.hexdigest()
    
