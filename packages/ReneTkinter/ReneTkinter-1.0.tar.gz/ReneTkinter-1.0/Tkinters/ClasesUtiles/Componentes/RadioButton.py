from tkinter import Radiobutton
from Tkinters.ClasesUtiles.Interfaces.ComponenteConAction import ComponenteConAction
from Tkinters.Imports.VisualPythonBasicosImports import *
from tkinter import IntVar
class _DatosDelGrupo():
    radios=[]
    listener=None
    intVar=None

class RadioButton(Radiobutton,ComponenteConAction):
    def __init__(self,contenedor,*args):
        """
        (contenedor)
        (contenedor,texto)
        (contenedor,X,Y,texto)
        (contenedor,X,Y)
        :param contenedor:
        :param args:
        """
        a=tuplaRectificada(args)
        leng=len(a)
        texto = None
        X=None
        Y=None
        if leng==1 and esString(a[0]):
            texto=a[0]
        elif leng==2 and esIntAll(a[0],a[1]):
            X=a[0]
            Y=a[1]
        elif leng == 3 and esString(a[2]) and esIntAll(a[0], a[1]):
            texto = a[2]
            X = a[0]
            Y = a[1]

        self.inicializarComponente(super(), contenedor, X, Y)
        if texto!=None:
            self.setText(texto)
        self.setGroupIntVar(IntVar(),1)
        self._onSelecionListener=None
        self.addAccion(self._llamarOnSelecionListener)
        self._datosDelGrupo=None


    def _llamarOnSelecionListener(self):
        if self._onSelecionListener != None:
            self._onSelecionListener(self, self._intVar.get(), self.isSelected())
    def setGroupIntVar(self,intVar,value=-1):
        self._intVar=intVar
        if value==-1:
            value=self._valueIntVar
        else:
            self._valueIntVar = value
        super().config(variable=intVar,value=value)

        return self
    def getIntVar(self):
        return self._intVar
    def getValeIntVar(self):
        return self._valueIntVar

    def getDatosDelGrupo(self):
        return self._datosDelGrupo
    def setDatosDelGrupo(self,datos):
        self._datosDelGrupo=datos
        return self
    def grupBy(self,radio):
        if esRadioButton(radio):
            if radio.getDatosDelGrupo()==None:
                if self._datosDelGrupo==None:
                    if (radio.getOnSelectionListener() != None):
                        self.setOnSelectionListener(radio.getOnSelectionListener())
                    elif self.getOnSelectionListener() != None:
                        radio.setOnSelectionListener(self.getOnSelectionListener())
                    self._datosDelGrupo=_DatosDelGrupo()
                    self._datosDelGrupo.listener=radio.getOnSelectionListener()
                    self._datosDelGrupo.radios=[radio,self]
                    self._datosDelGrupo.intVar=radio.getIntVar()
                    radio.setDatosDelGrupo(self._datosDelGrupo)

                    self.setGroupIntVar(radio.getIntVar(),2)

                else:
                    grup=self._datosDelGrupo
                    grup.radios.append(radio)
                    radio.setDatosDelGrupo(grup)
                    radio.setGroupIntVar(grup.intVar,len(grup.radios))
                    radio.setOnSelectionListener(grup.listener)
            else:
                grup = radio.getDatosDelGrupo()
                grup.radios.append(self)
                self.setDatosDelGrupo(grup)
                self.setGroupIntVar(grup.intVar, len(grup.radios))
                self.setOnSelectionListener(grup.listener)








            #self.setGroupIntVar(radio.getIntVar(),radio.getValeIntVar()+1)

        return self
    def isSelected(self):
        return self._intVar.get()==self._valueIntVar
    def setSelected(self):
        self._intVar.set(self._valueIntVar)
        return self
    def setOnSelectionListener(self,listener):
        """
        listener del tipo (self,volor#actual,isSelected)
        :param listener:
        :return:
        """
        self._onSelecionListener=listener
        #self.setAccion(lambda:listener(self,self._intVar.get(),self.isSelected()))

        return self
    def getOnSelectionListener(self):
        return self._onSelecionListener


def new_RadioButton_Grid(contenedor,row,column,*args):
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



    return RadioButton(contenedor,texto,a1).setGrid(row,column,a2)

def esRadioButton(a):
    return isinstance(a,RadioButton)