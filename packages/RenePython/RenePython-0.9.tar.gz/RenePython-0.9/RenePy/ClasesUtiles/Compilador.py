from RenePy.MetodosUtiles.Imports.MetodosUtilesBasicos import *
from RenePy.ClasesUtiles.File import File
from RenePy.MetodosUtiles import Archivo
import py_compile
import re


NOMBRE_CARPETA_COMPILADOS="__pycache__"
AGREGADO_COMPILADO=".cpython-"
EXTENCION_COMPILADO=".pyc"
EXTENCION_SIN_COMPILAR=".py"
NOMBRE_SETUP="setup.py"


class __CreadorDeSetup:
    __TIPO_DE_UBICACION_SUPERIOR="TIPO_DE_UBICACION_SUPERIOR"
    __TIPO_DE_UBICACION_INFERIOR = "TIPO_DE_UBICACION_INFERIOR"
    __TIPO_DE_UBICACION_DENTRO_DEL_SETUP = "TIPO_DE_UBICACION_DENTRO_DEL_SETUP"
    __PATRON_PAQUETES=re.compile(r"(?:(?:(?![\d_])\w)|[.])+")
    __PATRON_COMIENZO_PAQUETES=re.compile(r"packages[ ]*[=][ ]*[[]")
    def __init__(self):
        self.__lineasSuperiores=[]
        self.__paquetes=[]
        self.__lineasInferiores=[]
        #self.__yaCargoUnSetup=False
        self.isEmpty=True

    def add(self,url):
        url=str(url)
        lineas=Archivo.leer(url)
        #ubicacion=self.__TIPO_DE_UBICACION_SUPERIOR
        class Cu:
            def __init__(self,ubicacion):
                self.ubicacion=ubicacion
        cu=Cu(self.__TIPO_DE_UBICACION_SUPERIOR)
        def buscarNombresPaquete(li):
            find = re.findall(self.__PATRON_PAQUETES, li[m.end():])
            if find != None and len(find) > 0:
                for pa in find:
                    self.__paquetes.append(pa)
                if contiene(li, "]"):
                    cu.ubicacion = self.__TIPO_DE_UBICACION_INFERIOR
            else:
                cu.ubicacion = self.__TIPO_DE_UBICACION_INFERIOR

        for li in lineas:
            if cu.ubicacion==self.__TIPO_DE_UBICACION_SUPERIOR:
                m=re.search(self.__PATRON_COMIENZO_PAQUETES,li)
                if m!=None:
                    cu.ubicacion=self.__TIPO_DE_UBICACION_DENTRO_DEL_SETUP
                    buscarNombresPaquete(li)
                    continue
                if self.isEmpty:
                    self.__lineasSuperiores.append(li)
            elif cu.ubicacion==self.__TIPO_DE_UBICACION_DENTRO_DEL_SETUP:
                buscarNombresPaquete(li)
            elif cu.ubicacion==self.__TIPO_DE_UBICACION_INFERIOR:
                if self.isEmpty:
                    self.__lineasInferiores.append(li)
        self.isEmpty=False
    def crear(self,urlCarpetaSalida):
        urlCarpetaSalida=str(urlCarpetaSalida)
        lineas=[]
        lineas.extend(self.__lineasSuperiores)
        lineas.append("\tpackages=[")
        for pa in self.__paquetes:
            lineas.append(strg("\t\"",pa,"\""))
        lineas.append("\t],")
        lineas.extend(self.__lineasInferiores)
        Archivo.escribir(urlCarpetaSalida+"/"+NOMBRE_SETUP,lineas)



def compilarPy(url):
    py_compile.compile(str(url))

def compilarAllPy(urlProyectoACompilar,urlCarpetaSalida,vercionPy="310"):
    if not Archivo.existe(urlCarpetaSalida):
        Archivo.crearCarpeta(urlCarpetaSalida)
    c = __CreadorDeSetup()
    def accion(f:File):
        #f=File(file)
        if f.isDir():
            if f.getName()==NOMBRE_CARPETA_COMPILADOS:
                return False

        else:
            if f.getName()=="setup.py":
                c.add(f)
            elif Archivo.getExtencion(f)==EXTENCION_SIN_COMPILAR:
                compilarPy(f)
                carpetaCompilados=f.getParent()+"/"+NOMBRE_CARPETA_COMPILADOS
                archivoCompilado=carpetaCompilados+"/"+Archivo.getNombre(f)+AGREGADO_COMPILADO+vercionPy+EXTENCION_COMPILADO
                destino=File(strg(urlCarpetaSalida,f.getSubFile()).replace(EXTENCION_SIN_COMPILAR,EXTENCION_COMPILADO))
                if not destino.getParentFile().existe():
                    Archivo.crearCarpeta(destino.getParentFile())
                Archivo.copiar(fuente=archivoCompilado
                               ,destino=str(destino))

    if esLista(urlProyectoACompilar):
        for url in urlProyectoACompilar:
            Archivo.recorrerCarpetaYUtilizarSubCarpetas_BolEntrar(url, accion)
    else:
        Archivo.recorrerCarpetaYUtilizarSubCarpetas_BolEntrar(urlProyectoACompilar,accion)
    if not c.isEmpty:
        c.crear(urlCarpetaSalida)


# c=__CreadorDeSetup()
# c.add(r"D:\_Cosas\Programacion\Proyectos\Python\Paquetes\para compilar\PruebaAConectar\setup.py")
# c.add(r"D:\_Cosas\Programacion\Proyectos\Python\Paquetes\para compilar\RenePython\setup.py")
# c.crear(r"C:\Users\Rene\Desktop\Nueva carpeta\Nueva carpeta (13)\salida2")
# print("Termino")
# compilarAllPy(urlProyectoACompilar=[
#     r"D:\_Cosas\Programacion\Proyectos\Python\Paquetes\para compilar\PruebaAConectar"
#     ,r"D:\_Cosas\Programacion\Proyectos\Python\Paquetes\para compilar\RenePython"]
#               ,urlCarpetaSalida=r"C:\Users\Rene\Desktop\Nueva carpeta\Nueva carpeta (13)\Destino")
# print("Termino")
# compilarPy(File("D:\_Cosas\Programacion\Proyectos\Python\Paquetes\para compilar\PruebaAConectar\PruebaC\pruebaP.py"))
#
#class Compilador:

#Archivo.crear(str(File("D:\_Cosas\Programacion\Proyectos\Python\Paquetes\para compilar\PruebaAConectar\PruebaC\hola.txt")))

# Archivo.copiar(fuente=r"C:\Users\Rene\Desktop\Nueva carpeta\Nueva carpeta (13)\a.txt"
#                ,destino=r"C:\Users\Rene\Desktop\Nueva carpeta\Nueva carpeta (13)\b.txt")
# print("Termino")

# print(File(r"C:\Users\Rene\Desktop\Nueva carpeta\Nueva carpeta (13)\a.txt").getName())
#print(File().getParent())
#print(File("/"))
# f=File(r"C:\Users\Rene\Desktop\Nueva carpeta")
# lf=f.listFiles()
# for i in lf:
#     if i.isDir():
#         lf2=i.listFiles()
#         for j in lf2:
#             print("j=", j)
#             print("sf=", j.getSubFile())
#
#     print("i=",i)
#     print("sf=",i.getSubFile())