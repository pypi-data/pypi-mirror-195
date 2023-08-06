
class TipoDeAnclaje:
    def __init__(self,valor):
        self.valor=valor
    def getValor(self):
        return self.valor

NORTE=TipoDeAnclaje("n")
SUR=TipoDeAnclaje("s")
ESTE=TipoDeAnclaje("e")
OESTE=TipoDeAnclaje("w")
CENTRO=TipoDeAnclaje("")#center
NOROESTE=TipoDeAnclaje("nw")
NORESTE=TipoDeAnclaje("ne")
SUROESTE=TipoDeAnclaje("sw")
SURESTE=TipoDeAnclaje("se")

DERECHA=ESTE
ISQUIERDA=OESTE

#must be n, ne, e, se, s, sw, w, nw, or center
values=(NORTE,SUR,ESTE,OESTE,CENTRO,NOROESTE,NORESTE,SUROESTE,SURESTE)

def esTipoDeAnclaje(a):
    return isinstance(a,TipoDeAnclaje)