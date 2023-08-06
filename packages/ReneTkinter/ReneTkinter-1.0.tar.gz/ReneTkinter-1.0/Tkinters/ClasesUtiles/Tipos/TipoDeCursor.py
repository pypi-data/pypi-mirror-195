class TipoDeCursor:
    def __init__(self,valor):
        self.valor=valor
    def getValor(self):
        return self.valor
MANO=TipoDeCursor("hand2")
PIRATE=TipoDeCursor("pirate")
CIRCULO=TipoDeCursor("circle")
CRUZ=TipoDeCursor("cross")
values=(MANO,PIRATE)

def esTipoDeCursor(a):
    return isinstance(a,TipoDeCursor)