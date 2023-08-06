from Tkinters.Imports.VisualPythonBasicosImports import *
from Tkinters.ClasesUtiles.Tipos import TipoDeAnclaje
from Tkinters.ClasesUtiles.Tipos import TipoDeJustificacion
from Tkinters.ClasesUtiles.Tipos import TipoDeCursor
from Tkinters.ClasesUtiles.Componentes.Ventana import esVentana
from Tkinters.ClasesUtiles.CoordenadaGrid import CoordenadaGrid
from tkinter import StringVar
from Tkinters.ClasesUtiles.Interfaces.ComponenteConText import ComponenteConText
class ComponenteConAction(ComponenteConText):
	def iniVariables(self,superclase):
		super().iniVariables(superclase)
		self._listeners = []
		self._setAccion()
	def addAccion(self,accion):
		self._listeners.append(accion)
	def addAccionListener(self,listener):
		"""
		listener del tipo (self)
		:param listener:
		:return:
		"""
		self._listeners.append(lambda:listener(self) )
		return self
	def _LlamarActionListeners(self):
		for i in self._listeners:
			if i!= None:
				i()
	def _setAccion(self):
		self.config(command=self._LlamarActionListeners)
	def getListeners(self):
		return self._listeners