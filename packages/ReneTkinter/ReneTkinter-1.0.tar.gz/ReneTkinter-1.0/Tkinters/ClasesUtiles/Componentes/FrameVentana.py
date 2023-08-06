from tkinter import Frame
from Tkinters.ClasesUtiles.Tipos import TipoDeBorde
from Tkinters.ClasesUtiles.Tipos import TipoDeCursor
from Tkinters.Imports.VisualPythonBasicosImports import *

from Utiles.Utiles import *


#from Include.Tkinters.ClasesUtiles.Tipos import TipoDeBorde
#from Include.Tkinters.ClasesUtiles.Tipos import TipoDeCursor

#from Include.Tkinters.Imports.VisualPythonImports import *


#from Tipos import TipoDeBordeas
#from Tipos import TipoDeCursor

class FrameVentana(Frame):
	# def __init__(self, contenedor, ancho, alto):

	def __init__(self,*args):
		"""
		(contenedor, ancho, alto)
		()
		:param args:
		"""
		leng = len(args)
		#println("len=",leng)
		#println("a0 ",args[0]," a1",args[1]," a2",args[2])
		#println("es tk=",esTk(args[0])," es int ",esIntAll(args[1],args[2]))
		#println("leng == 3 & esTk(args[0]) and esIntAll(args[1],args[2])=",leng == 3 & esTk(args[0]) & esIntAll(args[1],args[2]))
		if leng == 3 and esTk(args[0]) and esIntAll(args[1],args[2]):
			#print("uno")
			super().__init__(args[0],width=args[1],height=args[2])
		else:
			#print("dos")
			super().__init__()
	def setSize(self,Width,Height):
		super().config(width=Width,height=Height)
		return self
	def setBackgraund(self,nombreColor):
		super().config(bg=nombreColor)
		return self
	def setTipoDeBorde(self,borde):
		if TipoDeBorde.esTipoDeBorde(borde):
			super().config(relief=borde.getValor())
		return self
	def setBordeWidth(self,ancho):
		super().config(bd=ancho)
		return self
	def setBorde(self,ancho,tipoDeBorde):
		self.setTipoDeBorde(tipoDeBorde)
		self.setBordeWidth(ancho)
		return self
	def setCursor(self,tipoDeCursor):
		if TipoDeCursor.esTipoDeCursor(tipoDeCursor):
			super().config(cursor=tipoDeCursor.getValor())

		return self
def esFrameVentana(a):
	return isinstance(a,FrameVentana)

def new_FrameVentana():
	return FrameVentana()


"""
pip3 uninstall ReneTkinter
pip3 install ReneTkinter-1.0.tar.gz
 python setup.py sdist
 
"""