from Tkinters.Imports.VisualPythonBasicosImports import *
from Tkinters.ClasesUtiles.Componentes.Ventana import esVentana
from tkinter import Menu
class Menur(Menu):
    def __init__(self,contenedor,titulo=None):
        super().__init__(contenedor)
        self._parent = None
        if esVentana(contenedor):
            contenedor.setMenu(self)
        elif esTk(contenedor):
            contenedor.config(menu=self)
        elif esMenu(contenedor):
            self._parent=contenedor
        self._subMenus=[]
        self._titulo=titulo

    def addSubMenu(self,titulo):
        sub=Menur(self,titulo)
        sub.config(tearoff=0)
        self._subMenus.append(sub)
        super().add_cascade(label=titulo,menu=sub)
        return sub
    def addItemAccion(self,titulo,accion):
        super().add_command(label=titulo,command=accion)
        return self
    def getSubMenus(self):
        return self._subMenus
    def getTitulo(self):
        return self._titulo
    def getParent(self):
        return self._parent
def esMenur(a):
    return isinstance(a,Menur)



