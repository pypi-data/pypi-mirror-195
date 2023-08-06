from Tkinters.Imports.VisualPythonBasicosImports import *
from Tkinters.ClasesUtiles.Tipos import TipoDeAnclaje
from Tkinters.ClasesUtiles.Tipos import TipoDeJustificacion
from Tkinters.ClasesUtiles.Componentes.Ventana import esVentana
from Tkinters.ClasesUtiles.CoordenadaGrid import CoordenadaGrid
from Tkinters.ClasesUtiles.Interfaces.Componente import Componente
from tkinter import Listbox
from tkinter import END

class ListBox(Listbox,Componente):
    def __init__(self,contenedor,*args):
        """
        (contenedor) (contenedor,X,Y)
        """
        a = tuplaRectificada(args)
        leng = len(a)
        texto = None
        X = None
        Y = None
        if leng == 2 and esIntAll(a[0], a[1]):
            X = a[0]
            Y= a[1]
        self.inicializarComponente(super(), contenedor, X, Y)
    def add(self,a):
        super().insert(END, a)
        return self


def esListBox(a):
    return isinstance(a,ListBox)
def new_ListBox_Grid(contenedor,row,column,*a):
    """
    (contenedor, row, column)
    (contenedor, row, column,anclaje)
    (contenedor, row, column,anclaje,pading)
    (contenedor, row, column,anclaje,padingX,padingY)
    (contenedor, row, column,pading)
    (contenedor, row, column,padingX,padingY)
    :param contenedor:
    :param row:
    :param column:
    :param texto:
    :param a:
    :return:
    """
    return ListBox(contenedor).setGrid(row, column, *a)

