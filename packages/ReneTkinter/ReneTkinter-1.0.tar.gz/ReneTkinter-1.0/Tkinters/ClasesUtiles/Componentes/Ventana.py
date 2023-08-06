from Tkinters.Imports.VisualPythonBasicosImports import *
from tkinter import Tk
#from Utiles.Utiles import *
from Tkinters.ClasesUtiles.Componentes.FrameVentana import FrameVentana



class Ventana(Tk):
	#def __init__(self,ancho,alto):
	#	self._frameVentana = FrameVentana(self,ancho,alto)
	#	self._frameVentana.pack(fill="both")
	def __init__(self,*args):
		"""
		(ancho,alto)
		()vacio
		:param args:
		"""
		super().__init__()
		leng = len(args)
		#print(leng)
		#print("a0=",args[0],"a1=", args[1])
		#print(esIntAll(args[0], args[1]))
		if (leng == 2 and esIntAll(args[0], args[1])):
			#print("u n o")
			self._frameVentana = FrameVentana(self,args[0], args[1])
		else:
			#print("d o s")
			self._frameVentana=FrameVentana()

		self._frameVentana.pack(fill="both")


	def setBackgraund(self,nombreColor):
		super().config(bg=nombreColor)
		self._frameVentana.setBackgraund(nombreColor)
		return self
	def setTitle(self,titulo):
		super().title(titulo)
		return self
	def setSize(self,width,height):
		#super().geometry(str(str(width)+"x"+str(height)))
		self._frameVentana.setSize(width,height)
		return self
	def setIcon(self,direccion):
		if esString(direccion):
			super().iconbitmap(direccion)
		return self
	def setResizable(self,permitido):
		super().resizable(permitido,permitido)
		return self
	def setTipoDeBorde(self,borde):
		self._frameVentana.setTipoDeBorde(borde)
		return self
	def setBordeWidth(self,ancho):
		self._frameVentana.setBordeWidth(ancho)
		return self
	def setBorde(self,ancho,tipoDeBorde):
		self._frameVentana.setBorde(ancho,tipoDeBorde)
		return self
	def setCursor(self,tipoDeCursor):
		self._frameVentana.setCursor(tipoDeCursor)
		return self
	def getFrame(self):
		return self._frameVentana
	def getTk(self):
		return super()
	def show(self):
		super().mainloop()
		return self
	def setMenu(self,menu):
		if esMenu(menu):
			super().config(menu=menu)
	def showDialogoSalir(self):
		showDialogoSalir(self)

def esVentana(a):
	return isinstance(a,Ventana)


""""
pip3 uninstall ReneTkinter
pip3 install ReneTkinter-1.0.tar.gz
 python setup.py sdist
 
"""
#def hola(*a):
#	print(len(a))

#hola()
#a=4==2 and 4==3


