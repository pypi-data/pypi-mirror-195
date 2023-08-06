from Tkinters.Imports.VisualPythonBasicosImports import *
from Tkinters.ClasesUtiles.Tipos import TipoDeAnclaje
from Tkinters.ClasesUtiles.Tipos import TipoDeJustificacion
from Tkinters.ClasesUtiles.Componentes.Ventana import esVentana
from Tkinters.ClasesUtiles.CoordenadaGrid import CoordenadaGrid
from Tkinters.ClasesUtiles.Interfaces.Componente import Componente
from tkinter import Text
from tkinter import Scrollbar
from tkinter import END

class AreaDeTexto(Text,Componente):
    # def __init__(self,contenedor): usar setGrid
    #def __init__(self,contenedor,X,Y):
    def __init__(self, *a):
        """
        (contenedor)
        (contenedor,X,Y)
        :param a:
        """
        leng=len(a)
        if leng>0 and (esTk(a[0]) or esFrame(a[0])):
             contenedor=a[0]
             if esVentana(a[0]):
                 contenedor=a[0].getFrame()
             super().__init__(contenedor)
             self._scrollBar=Scrollbar(contenedor,command=super().yview)
             super().config(yscrollcommand=self._scrollBar.set)
        if leng==3 and esIntAll(a[1], a[2]):
            self.setPosition(a[1], a[2])
        self._textSize = 10
        self._textColor = "black"
        #self._texto =""
        self._verScrollBar=False
        self._coordenadaGrid=None

        self._superClase=super()
        self.iniVariables(super())
    #def setGrid(self,row,column):
    #def setGrid(self, row, column,anclaje=TipoDeAnclaje.CENTRO):
    def setGrid(self,row,column, *args):
        """
        ( row, column)
        ( row, column,anclaje)
        ( row, column,anclaje,pading)
        ( row, column,anclaje,padingX,padingY)
        ( row, column,pading)
        ( row, column,padingX,padingY)
        :param row:
        :param column:
        :param args:
        :return:
        """
        a=args
        leng=len(a)
      #  println("len ", leng)
        #println("tipe=",type(a)," es t=",esTupla(a)," es to=",isinstance(a,tuple))
        if leng==1 and esTupla(a[0]):
           a=a[0]
           leng = len(a)

        self._coordenadaGrid=CoordenadaGrid(row,column)
        if leng==0:
            super().grid(row=row, column=column)
        elif leng==1:
            if TipoDeAnclaje.esTipoDeAnclaje(a[0]):
                super().grid(row=row, column=column,sticky=a[0].getValor())
            elif esInt(a[0]):
                super().grid(row=row, column=column, padx=a[0],pady=a[0])
        elif leng==2:
            if TipoDeAnclaje.esTipoDeAnclaje(a[0]) and esInt(a[1]):
                super().grid(row=row, column=column,sticky=a[0].getValor(),padx=a[1],pady=a[1])
            elif esIntAll(a[0],a[1]):
                super().grid(row=row, column=column, padx=a[0],pady=a[1])
        elif leng==3 and TipoDeAnclaje.esTipoDeAnclaje(a[0]) and esIntAll(a[1],a[2]):
            super().grid(row=row, column=column, sticky=a[0].getValor(), padx=a[1], pady=a[2])

        self.actualizarScrollBar()
        return self
    def actualizarScrollBar(self):
        coor = self._coordenadaGrid
        if self._verScrollBar and coor != None:
            self._scrollBar.grid(row=coor.row, column=coor.column + 1,sticky="nsew")
    def setVerScrollBar(self,verlo):
        self._verScrollBar=verlo
        self.actualizarScrollBar()
        return self

    def getScrollBar(self):
        return self._scrollBar
    def append(self,texto):
        super().insert(END, texto)
        return self
    def setText(self, texto):
        self.clear()
        super().insert(1.0,texto)
        return self

    def getText(self):
        return super().get("1.0",END)

    def setPosition(self, X, Y):
        super().place(x=X, y=Y)
        self._coordenadaGrid=None
        return self

    def getX(self):
        return super().winfo_x()

    def getY(self):
        return super().winfo_y()

    def setX(self, x):
        self.setPosition(x, self.getY())

    def setY(self, y):
        self.setPosition(self.getX(), y)

    def setTextColor(self, color):
        self.config(fg=color)
        self._textColor = color
        return self

    def getTextColor(self):
        return self._textColor

    def setTextSize(self, tamaño):
        self.config(font=(tamaño))
        self._textSize = tamaño
        return self

    def getTextSize(self):
        return self._textSize

    def setTextFamili(self, familia):
        self.config(font=(familia, self.getTextSize()))
        return self

    def setFont(self, familia, tamaño):
        self.config(font=(familia, tamaño))
        self._textSize = tamaño
        return self

    def setTipoDeAnclaje(self, tipoDeAnclaje):
        if TipoDeAnclaje.esTipoDeAnclaje(tipoDeAnclaje):
            self.config(anchor=tipoDeAnclaje.getValor())
        return self

    def setWidth(self, width):
        self.config(width=width)
        return self

    def setHeight(self, height):
        self.config(height=height)
        return self

    def setSize(self, width, height):
        self.config(width=width, height=height)
        return self

    def setBackgraund(self, nombreColor):
        super().config(bg=nombreColor)
        return self

    def setJustificacion(self, tipoDeJustificacion):
        if TipoDeJustificacion.esTipoDeJustificacion(tipoDeJustificacion):
            super().config(justify=tipoDeJustificacion.getValor())
        return self
    def setTipoDeAnclaje_Grid(self,tipoDeAnclaje):
        if TipoDeAnclaje.esTipoDeAnclaje(tipoDeAnclaje):
            super().grid(sticky=tipoDeAnclaje.getValor())
        return self
    def setPading_Grid(self,*args):
        """
        (row,column)
        (rowYcolumn) un parametro row==column
        :param args:
        :return:
        """
        a=tuplaRectificada(args)
        leng =len(a)
        if leng==2 and esIntAll(a[0],a[1]):
            super().grid(padx=a[0],pady=a[1])
        elif leng==1 and esInt(a[0]):
            super().grid(padx=a[0], pady=a[0])
        return self
    def setTipoPassword(self,tipoPassword):
        if tipoPassword:
            super().config(show="*")
        else:
            super().config(show="")
        return self
    def clear(self):
        super().delete(1.0,END)
#------sobrescribiendo----------
    # def setTextVar(self,textVar):
    #     if esStringVar(textVar):
    #         #self.config(textvariable=textVar)
    #         #self.getSuperClase().config(textvariable=textVar)
    #         self._textVar=textVar
    #         self._texto=textVar.get()
    #     return self
    # def _setAccion(self):
    #     pass
    # def getText(self):
    #     text=super().get("1.0",END)
    #     self._textVar.set(text)
    #     return text
    # def setText(self, texto):
    #     if texto!=None:
    #         super().insert(1.0,texto)
    #         #self.config(text=texto)
    #         self._textVar.set(texto)
    #     return self
#-----------------------------------        

def new_AreaDeTexto_Grid(contenedor,row,column,*a):
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
    :param a:
    :return:
    """
    #println("len a=",len(a))
    return AreaDeTexto(contenedor).setGrid(row,column,a)

def esAreaDeTexto(a):
    return isinstance(a, AreaDeTexto)
