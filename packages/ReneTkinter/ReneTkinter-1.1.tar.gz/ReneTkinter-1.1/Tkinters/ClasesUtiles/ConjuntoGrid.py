from hmac import new

from Tkinters.Imports.VisualPythonBasicosImports import *
from Tkinters.ClasesUtiles.Componentes.CuadroDeTexto import CuadroDeTexto
from Tkinters.ClasesUtiles.Componentes.CuadroDeTexto import new_PasswordField
from Tkinters.ClasesUtiles.Componentes.Labelr import Labelr
from Tkinters.ClasesUtiles.Componentes.Boton import Boton
from Tkinters.ClasesUtiles.Componentes.AreaDeTexto import AreaDeTexto
from Tkinters.ClasesUtiles.Componentes.RadioButton import RadioButton
from Tkinters.ClasesUtiles.Componentes.CheckBox import CheckBox
from Tkinters.ClasesUtiles.Componentes.ListBox import ListBox
from Tkinters.ClasesUtiles.Interfaces.Componente import Componente
from Tkinters.ClasesUtiles.Interfaces.Componente import esComponente

class _ConfiguracionDeColumna():
    padX=None
    padY=None
    anclaje=None
class _ConfiguracionDeFila(_ConfiguracionDeColumna):
    pass


class ConjuntoGrid():
    def __init__(self,contenedor,columns):
        self.contendor=contenedor
        self.clumns=columns
        self.rows=[]
        self.configuracionesDeColumnas=[]
        self.configuracionesDeFilas=[]
        for i in range(columns):
            self.configuracionesDeColumnas.append(_ConfiguracionDeColumna())
    def actualizar(self):
        for i in range(self.clumns):
            column=self.getColumn(i)
            leng=len(column)
            #println("i=",i," colu=",column)
            for j in range(leng):
                elem=column[j]#self.rows[i][j]
                if elem!=None :
                    conf=self.configuracionesDeColumnas[i]
                    confFila=self.configuracionesDeFilas[j]
                    if conf.padX!=None and confFila.padX==None:
                        elem.grid(padx=conf.padX)
                    if conf.padY != None and confFila.padY==None:
                        elem.grid(pady=conf.padY)
                    if conf.anclaje != None and confFila.anclaje==None:
                        elem.grid(sticky=conf.anclaje.getValor())
        leng=len(self.rows)#range(leng)
        for i in range(leng):
            conf = self.configuracionesDeFilas[i]
            if conf.padX != None or conf.padY != None or conf.anclaje != None:
                for j in self.rows[i]:
                    elem=j
                    if elem != None:
                        if conf.padX != None :
                            elem.grid(padx=conf.padX)
                        if conf.padY != None :
                            elem.grid(pady=conf.padY)
                        if conf.anclaje != None :
                            elem.grid(sticky=conf.anclaje.getValor())


        return self
    def getColumn(self,indice):
        column=[]
        for i in self.rows:
            if indice<len(i):
                column.append(i[indice])
            else:
                column.append(None)
        return column
    def get(self,X,Y):
        return self.rows[X][Y]
    def setPadingColumn(self,columnIndice,padX,padY=None):
        if padY==None:
            padY=padX
        self.configuracionesDeColumnas[columnIndice].padX=padX
        self.configuracionesDeColumnas[columnIndice].padY = padY
        return self
    def setPadingColumn_Actualizar(self,columnIndice,padX,padY=None):
        self.setPadingColumn(columnIndice,padX,padY)
        self.actualizar()
        return self
    def setPadingXColumn(self,columnIndice,padX):
        self.configuracionesDeColumnas[columnIndice].padX=padX
        return self
    def setPadingXColumn_Actualizar(self,columnIndice,padX):
        self.setPadingXColumn(columnIndice,padX)
        self.actualizar()
        return self
    def setPading(self,padX,padY=None):
        if padY==None:
            padY=padX
        for i in self.configuracionesDeColumnas:
            i.padX=padX
            i.padY=padY
        return self
    def setPadingYColumn(self, columnIndice, padY):
        self.configuracionesDeColumnas[columnIndice].padY = padY
        return self

    def setPadingYColumn_Actualizar(self, columnIndice, padY):
        self.setPadingYColumn(columnIndice, padY)
        self.actualizar()
        return self
    def setAnclaje(self,columnIndice,anclaje):
        self.configuracionesDeColumnas[columnIndice].anclaje=anclaje
        return self
    def setAnclaje_Actualizar(self,columnIndice,anclaje):
        self.setAnclaje(columnIndice,anclaje)
        self.actualizar()
        return self
    #def actualizarColumna(self,indiceColumna):

    
    def addRow(self,*hijos):
        #println("hijos=",hijos)
        row=list(tuplaRectificada(hijos))
        #println("row=" , row)
        self.rows.append(row)
        leng=len(row)
        #println("leng=" , leng)
        fila=len(self.rows)-1
        for i in range(leng):
            #println("i=" , i)
            if esComponente(row[i]):
                row[i].setGrid(fila,i)
            else:
                #println("row[i]=" , row[i])
                row[i].grid(row=fila, column=i)
        self.configuracionesDeFilas.append(_ConfiguracionDeFila())
        return self
    def addRow_Actualizar(self,*hijos):
        self.addRow(tuplaRectificada(hijos))
        self.actualizar()
        return self
    def setPadingFila(self,fila,padX,padY=None):
        if padY==None:
            padY=padX
        self.configuracionesDeFilas[fila].padX=padX
        self.configuracionesDeFilas[fila].padY = padX
        return self
    def setPadingFilaX(self,fila,padX):
        self.configuracionesDeFilas[fila].padX=padX
        return self
    def setPadingFilaY(self,fila,padY):
        self.configuracionesDeFilas[fila].padY=padY
        return self
    def setPadingFila_Actual(self,padX,padY=None):
        return self.setPadingFila(len(self.rows)-1,padX,padY)
    def setPadingFilaX_Actual(self,fila,padX):
        return self.setPadingFilaX(len(self.rows)-1,padX)
    def setPadingFilaY_Actual(self,fila,padY):
        return self.setPadingFilaY(len(self.rows)-1,padY)

    # new ++++++++++++++++++++++++++++++
    def new_CuadroDeTexto(self,textColor=None):
        ent=CuadroDeTexto(self.contendor)
        if textColor!=None:
            ent.setTextColor(textColor)
        return ent
    def new_PasswordField(self):
        return new_PasswordField(self.contendor)
    def new_Labelr(self,texto,background=None,textColor=None):
        lab=Labelr(self.contendor,texto)
        if background!=None:
            lab.setBackgraund(background)
            if textColor!=None:
                lab.setTextColor(textColor)
        return lab
    def new_AreaDeTexto(self):
        return AreaDeTexto(self.contendor)
    def new_Boton(self,texto,accion):
        return Boton(self.contendor,texto,accion)
    def new_RadioButton(self,texto=None):
        return RadioButton(self.contendor,texto)
    def new_CheckBox(self,*a):
        return CheckBox(self.contendor,*a)
    def new_ListBox(self):
        return ListBox(self.contenedor)



