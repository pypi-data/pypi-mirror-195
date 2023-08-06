from Tkinters.Imports.VisualPythonBasicosImports import *
from Tkinters.ClasesUtiles.Tipos import TipoDeAnclaje
from Tkinters.ClasesUtiles.Tipos import TipoDeJustificacion
from Tkinters.ClasesUtiles.Tipos import TipoDeCursor
from Tkinters.ClasesUtiles.Componentes.Ventana import esVentana
from Tkinters.ClasesUtiles.CoordenadaGrid import CoordenadaGrid
from tkinter import StringVar
from Tkinters.ClasesUtiles.Interfaces.Componente import Componente
class ComponenteConText(Componente):
	def iniVariables(self,superclase):
		super().iniVariables(superclase)
		self.setTextVar(StringVar())
	def setText(self, texto):
		#println("text=",texto)
		if texto!=None:
			self._textVar.set(texto)
			#self.config(text=texto)
		return self
	def getText(self):
		return self._textVar.get()
	def setTextVar(self,textVar):
		if esStringVar(textVar):
			self.getSuperClase().config(textvariable=textVar)
			self._textVar=textVar
			self._texto=textVar.get()
		return self
	def getTextVar(self):
		return self._textVar
	def ligar(self,elemento):
		if Componente.esComponente(elemento):
			self.setTextVar(elemento.getTextVar())
		elif esStringVar(elemento):
			self.setTextVar(elemento)
		return self
