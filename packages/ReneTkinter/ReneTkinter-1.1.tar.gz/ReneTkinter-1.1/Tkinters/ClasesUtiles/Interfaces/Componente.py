from Tkinters.Imports.VisualPythonBasicosImports import *
from Tkinters.ClasesUtiles.Tipos import TipoDeAnclaje
from Tkinters.ClasesUtiles.Tipos import TipoDeJustificacion
from Tkinters.ClasesUtiles.Tipos import TipoDeCursor
from Tkinters.ClasesUtiles.Componentes.Ventana import esVentana
from Tkinters.ClasesUtiles.CoordenadaGrid import CoordenadaGrid
from tkinter import StringVar

class Componente():

    def inicializarComponente(self,superclase,contenedor,X=None,Y=None):
        #println("super=",superclase)
        #println("conte=",contenedor)
        self._superClase=superclase
        if contenedor!=None and (esTk(contenedor) or esFrame(contenedor)):
            if esVentana(contenedor):
                contenedor = contenedor.getFrame()

            superclase.__init__(contenedor)

        self._contenedor=contenedor
        #self._texto = None

        if X!=None and Y!=None:
            self.setPosition(X,Y)

        self.iniVariables(superclase)
        return self
    def getSuperClase(self):
        return self._superClase
    def iniVariables(self,superclase):
        self._superClase=superclase
        self._textSize = 10
        self._textColor = "black"
        self._coordenadaGrid = None
        #self.setTextVar(StringVar())
        #self._listeners = []
        #self._setAccion()
    def setGrid(self, row, column, *args):
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
        a = args
        leng = len(a)
        #println("len ", leng)
        # println("tipe=",type(a)," es t=",esTupla(a)," es to=",isinstance(a,tuple))
        if leng == 1 and esTupla(a[0]):
            a = a[0]
            leng = len(a)
        self._coordenadaGrid = CoordenadaGrid(row, column)
        if leng == 0:
            self.grid(row=row, column=column)
        elif leng == 1:
            if TipoDeAnclaje.esTipoDeAnclaje(a[0]):
                self.grid(row=row, column=column, sticky=a[0].getValor())
            elif esInt(a[0]):
                self.grid(row=row, column=column, padx=a[0], pady=a[0])
        elif leng == 2:
            if TipoDeAnclaje.esTipoDeAnclaje(a[0]) and esInt(a[1]):
                self.grid(row=row, column=column, sticky=a[0].getValor(), padx=a[1], pady=a[1])
            elif esIntAll(a[0], a[1]):
                self.grid(row=row, column=column, padx=a[0], pady=a[1])
        elif leng == 3 and TipoDeAnclaje.esTipoDeAnclaje(a[0]) and esIntAll(a[1], a[2]):
            self.grid(row=row, column=column, sticky=a[0].getValor(), padx=a[1], pady=a[2])
        return self

    #def setText(self, texto):
    #    if texto!=None:
    #        self.config(text=texto)
    #        self._textVar.set(texto)
    #    return self

    #def getText(self):
    #    return self._textVar.get()

    def setPosition(self, X, Y):
        self.place(x=X, y=Y)
        self._coordenadaGrid = None
        return self

    def getX(self):
        return self.winfo_x()

    def getY(self):
        return self.winfo_y()

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
        #super().config(bg=nombreColor)
        self.config(bg=nombreColor)
        return self

    def setJustificacion(self, tipoDeJustificacion):
        if TipoDeJustificacion.esTipoDeJustificacion(tipoDeJustificacion):
            self.config(justify=tipoDeJustificacion.getValor())
        return self
    def setTipoDeAnclaje_Grid(self,tipoDeAnclaje):
        if TipoDeAnclaje.esTipoDeAnclaje(tipoDeAnclaje):
            self.grid(sticky=tipoDeAnclaje.getValor())
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
            self.grid(padx=a[0],pady=a[1])
        elif leng==1 and esInt(a[0]):
            self.grid(padx=a[0], pady=a[0])
        return self
    #Nuevos Metodos
    
    def setColumnSpan_Grid(self,span):
        self.grid(columnspan=span)
        return self
    def setRowSpan_Grid(self,span):
        self.grid(rowspan=span)
        return self

    # def addAccion(self,accion):
    #     self._listeners.append(accion)
    # def addAccionListener(self,listener):
    #     """
    #     listener del tipo (self)
    #     :param listener:
    #     :return:
    #     """
    #     #self._accion=accion
    #     #super().config(command=accion)
    #     self._listeners.append(lambda:listener(self) )
    #     return self
    # def _LlamarActionListeners(self):
    #     #print("se llama")
    #     #a=0
    #     for i in self._listeners:
    #         if i!= None:
    #             i()
    #         #println("a=",a)
    #         #a += 1

    # def _setAccion(self):
    #     self.config(command=self._LlamarActionListeners)
    # def getListeners(self):
    #     return self._listeners
    def setCursor(self,tipoDeCursor):
        if TipoDeCursor.esTipoDeCursor(tipoDeCursor):
            self.config(cursor=tipoDeCursor.getValor())

        return self


def esComponente(a):
    return isinstance(a,Componente)
