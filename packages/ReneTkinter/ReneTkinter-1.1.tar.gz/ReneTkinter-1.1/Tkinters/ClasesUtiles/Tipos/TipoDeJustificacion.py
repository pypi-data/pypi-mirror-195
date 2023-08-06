class TipoDeJustificacion:
    def __init__(self,valor):
        self.valor=valor
    def getValor(self):
        return self.valor

DERECHA=TipoDeJustificacion("right")
ISQUIERDA=TipoDeJustificacion("left")
CENTRO=TipoDeJustificacion("center")



values=(DERECHA,ISQUIERDA,CENTRO)

def esTipoDeJustificacion(a):
    return isinstance(a,TipoDeJustificacion)