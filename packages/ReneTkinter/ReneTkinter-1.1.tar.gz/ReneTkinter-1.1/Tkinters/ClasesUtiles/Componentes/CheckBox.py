from Tkinters.ClasesUtiles.Interfaces.ComponenteConAction import ComponenteConAction
from Tkinters.Imports.VisualPythonBasicosImports import *
from tkinter import Checkbutton
from tkinter import BooleanVar

class CheckBox(Checkbutton,ComponenteConAction):
    def __init__(self,contenedor,*args):
        """
        (contenedor)
        (contenedor,texto)
        (contenedor,X,Y,texto)
        (contenedor,X,Y)
        (contenedor,texto,bacground)
        :param contenedor:
        :param args:
        """
        a=tuplaRectificada(args)
        leng=len(a)
        texto = None
        X=None
        Y=None
        fondo=None
        if leng==1 and esString(a[0]):
            texto=a[0]
        elif leng==2:
            if esIntAll(a[0],a[1]):
                X=a[0]
                Y=a[1]
            elif esStringAll(a[0],a[1]):
                texto=a[0]
                fondo=a[1]
        elif leng==3 and esString(a[2]) and esIntAll(a[0],a[1]):
            texto=a[2]
            X = a[0]
            Y = a[1]

        self.inicializarComponente(super(), contenedor, X, Y)
        if texto!=None:
            self.setText(texto)
        self._booleanVar=BooleanVar();
        self.config(variable=self._booleanVar,onvalue=True,offvalue=False)
        if fondo!=None:
            self.setBackgraund(fondo)
    def setSelected(self,selected):
        self._booleanVar.set(selected)
        return self
    def isSelected(self):
        return self._booleanVar.get()
    def addSelectionListener(self,listener):
        """
        listener del tipo (self,isSelected)
        :param listener:
        :return:
        """
        self.getListeners().append(lambda:listener(self,self.isSelected()))
        return self


def new_CheckBox_Grid(contenedor,row,column,*args):
    """
    (contenedor, row, column,texto)
    (contenedor, row, column,texto,anclaje)
    (contenedor, row, column,texto,anclaje,pading)
    (contenedor, row, column,texto,anclaje,padingX,padingY)
    (contenedor, row, column,texto,pading)
    (contenedor, row, column,texto,padingX,padingY)
    (contenedor, row, column)
    (contenedor, row, column,anclaje)
    (contenedor, row, column,anclaje,pading)
    (contenedor, row, column,anclaje,padingX,padingY)
    (contenedor, row, column,pading)
    (contenedor, row, column,padingX,padingY)
    :param contenedor:
    :param row:
    :param column:
    :param args:
    :return:
    """
    a = tuplaRectificada(args)
    leng = len(a)
    texto = None
    iniSegundaTupla=0
    if leng>0:
        if esString(a[0]):
            texto=a[0]
            iniSegundaTupla=1
    al=list(a)
    if iniSegundaTupla!=0 and leng!=0:
        a1=tuple(al[:iniSegundaTupla])
        if iniSegundaTupla!=leng:
            a2 = tuple(al[iniSegundaTupla:])
        else:
            a2=()
    else:
        a1=()
        a2=a



    return CheckBox(contenedor,texto,a1).setGrid(row,column,a2)


def esCheckBox(a):
    return isinstance(a,CheckBox)
