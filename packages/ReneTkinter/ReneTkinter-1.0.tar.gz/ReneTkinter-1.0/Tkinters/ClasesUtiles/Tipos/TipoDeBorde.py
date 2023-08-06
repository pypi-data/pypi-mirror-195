


class TipoDeBorde:
    def __init__(self,valor):
        self.valor=valor
    def getValor(self):
        return self.valor

GROOVE=TipoDeBorde("groove")
SUNKEN=TipoDeBorde("sunken")

values=(GROOVE,SUNKEN)
def esTipoDeBorde(a):
    return isinstance(a,TipoDeBorde)

"""
from Tkinters.ClasesUtiles.Ventana import Ventana
ven=Ventana()
ven.setTitle("Nueva")
ven.setSize(600,400)
ven.setBackgraundColor("red")
ven.setBorde(25,SUNKEN)
ven.show()
"""

