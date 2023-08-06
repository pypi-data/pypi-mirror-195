from Tkinters.Imports.VisualPythonBasicosImports import *
from Tkinters.ClasesUtiles.Tipos import TipoDeAnclaje
from Tkinters.ClasesUtiles.Tipos import TipoDeJustificacion
from Tkinters.ClasesUtiles.Componentes.Ventana import esVentana
from Tkinters.ClasesUtiles.CoordenadaGrid import CoordenadaGrid
#from Tkinters.ClasesUtiles.Interfaces.Componente import Componente
from Tkinters.ClasesUtiles.Interfaces.ComponenteConAction import ComponenteConAction
from tkinter import Button

class Boton(Button,ComponenteConAction):
    #def __init__(self,contenedor,texto,accion,X=None,Y=None):
    def __init__(self,contenedor,*args):
        """
        (contenedor)
        (contenedor,texto,accion)
        (contenedor,X,Y,texto,accion)

        :param args:
        """
        a = tuplaRectificada(args)
        leng = len(a)
        texto = None
        X = None
        Y = None
        accion=None
        if leng == 2 and esString(a[0]) and esFuncion(a[1]):
            texto = a[0]
            accion= a[1]
        elif leng == 4 and esString(a[2]) and esIntAll(a[0], a[1]) and esFuncion(a[3]):
            texto = a[2]
            X = a[0]
            Y = a[1]
            accion=a[3]

        self.inicializarComponente(super(), contenedor, X, Y)
        self.setText(texto)
        self.addAccion(accion)



def esBoton(a):
    return isinstance(a,Boton)
def new_Boton_Grid(contenedor,row,column,texto,*a):
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
    return Boton(contenedor, texto).setGrid(row, column, a)