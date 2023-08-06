from tkinter import Frame
from tkinter import Tk
from tkinter import StringVar
from tkinter import Menu
from tkinter import messagebox
from tkinter import filedialog
from Utiles.Utiles import *
#from Tkinters.ClasesUtiles.Ventana import esVentana

def esFrame(a):
    return isinstance(a,Frame)
def esTk(a):
    return isinstance(a,Tk)
def esStringVar(a):
    return isinstance(a,StringVar)
def append(a,text):
    if esStringVar(a):
        a.set(a.get()+text)
def esMenu(a):
    return isinstance(a,Menu)



def responderException(ex):
    mensaje="error de codigo interno"
    messagebox.showerror("Error", mensaje)
def showDialogoSalir(ventana):
    if esTk(ventana) and messagebox.askquestion("Salir","Desea cerrar la ventana")=="yes":
        ventana.destroy()
def showInfo(mensaje):
    messagebox.showinfo("Informacion",mensaje)
def showAdvertencia(mensaje):
    messagebox.showwarning("Advertencia",mensaje)
def showError(mensaje):
    messagebox.showerror("Error",mensaje)
def showAceptarCancelarInf(titulo,mensaje):
    return messagebox.askquestion(titulo,mensaje)=="yes"
def showAceptarCancelarAdvertencia(titulo,mensaje):
    return messagebox.askretrycancel(titulo,mensaje)
def showFileChoser(fileDefault="C:",*extenciones):
    a=tuplaRectificada(extenciones)

    if esString(fileDefault):
        leng2=len(fileDefault)
        if leng2==1:
            fileDefault=fileDefault.upper()+":"
        elif leng2<7 and (fileDefault.startswith(".") or fileDefault.startswith("*")):
            l=list(a)
            l.insert(0,fileDefault)
            a=tuple(l)
            fileDefault="C:"
    leng = len(a)
    fileType=None
    if leng>0:
        fileType=[]
        for i in a:
            if not i.startswith("*"):
                i=str("*")+i
            fileType.append((i,i))
        fileType=tuple(fileType)
    if fileType==None:
        fileType=(("todos","*.*"))
        #return filedialog.askopenfilename(title="titulo",initialdir=fileDefault)
    return filedialog.askopenfilename(title="Buscar archivos",initialdir=fileDefault,filetypes=fileType)
def showDirectoryChoser(fileDefault="C:"):
    return filedialog.askdirectory(title="Buscar carpetas",initialdir=fileDefault)
