from io import open
from io import TextIOWrapper
import pickle
#from RenePython.Utiles.MetodosUtiles import MetodosUtiles
#from RenePython.Utiles.MetodosUtiles.Imports.MetodosUtilesBasicos import *
from RenePy.MetodosUtiles import MetodosUtiles
from RenePy.MetodosUtiles.Imports.MetodosUtilesBasicos import *
from xml.etree.ElementTree import parse
import json
import zipfile
import tarfile
import csv
import os
from RenePy.ClasesUtiles.File import File
import shutil
from zipfile import ZipFile

def recorrerCarpetaYUtilizarSubCarpetas_BolContinuar(file,utilizar,esCarpetaPadre=True,profundidad=0):#,subRecorrido=None
    # utilizar (f,profundidad)
    file=File.castear(file)
    if file.existe():
        if not esCarpetaPadre:
            if not utilizar(file,profundidad):
                return False
        # else:
        #     if file.subDireccion == None:
        #         file.subDireccion = file.getName()
        #         file.subCarpeta=""
        if file.isDir():

            lf=file.listFiles()
            for f in lf:
                # i.subCarpeta="/"+file.subDireccion
                # i.subDireccion=i.subCarpeta
                # subRecorridoActual=subRecorrido+"/"+i.getName()
                if not recorrerCarpetaYUtilizarSubCarpetas_BolContinuar(f,utilizar,False,(profundidad+1)):#,subRecorridoActual
                    return False
        return True
    return False

def recorrerCarpetaYCrearSubCarpetasImagen_BoolContinuar(carpetaOriginal,carpetaSalida,utilizar):
    def accion(f: File):
        if f.isDir():
            pass
        else:
            destino = File(strg(carpetaSalida, f.getSubFile()))
            if not destino.getParentFile().existe():
                crearCarpeta(destino.getParentFile())
            if not utilizar(f,destino):
                return False
        return True

    recorrerCarpetaYUtilizarSubCarpetas_BolContinuar(carpetaOriginal, accion)

def extraerZip_BoolContinuar(urlZip,urlCarpetaSalida,metodoBool_AntesDeExtraer,metodoBool_GetProgreso):
    #metodoBool_AntesDeExtraer (nombreFile)->bool
    #metodoBool_GetProgreso (totalArchivos,indiceActual)->bool
    #f_carpeta_salida=File(urlCarpetaSalida)
    with ZipFile(urlZip, 'r') as obj_zip:
        FileNames = obj_zip.namelist()
        total=len(FileNames)
        indice=0
        for fileName in FileNames:
            if not metodoBool_AntesDeExtraer(fileName):
                return None
            #f_salida_elemento=File
            obj_zip.extract(fileName, urlCarpetaSalida)
            if not metodoBool_GetProgreso(total,indice):
                return None
            indice+=1



def getProfundidad(f):
    f=str(f).strip()
    p=len(f.replace("\\","/").split("/"))-1
    if f.endswith("/"):
        return p-1
    return p

    #f = File.castear(f)

def esZip(f):
    f=File.castear(f)
    return f.isFile() and f.getExtencion().lower()==".zip"
def recorrerCarpeta(file,utilizar):
    file=File.castear(file)
    if file.existe():
        if file.isDir():
            lf=file.listFiles()
            for i in lf:
                recorrerCarpeta(i,utilizar)
        else:
            utilizar(file)
def copiarContenidoCarpeta_BoolCopiarArchivo(fileCarpetaOriginal,fileCarpetaDestino,predicateCopiarArchivo):
    def accion(f):
        if predicateCopiarArchivo(f):
            destino = File(strg(fileCarpetaDestino, f.getSubFile()))
            if not destino.getParentFile().existe():
                crearCarpeta(destino.getParentFile())
            copiar(fuente=f
                   , destino=destino)
    recorrerCarpeta(fileCarpetaOriginal,accion)


def mover(fuente, destino):
    shutil.move(fuente, destino)
def copiar(fuente, destino):
    shutil.copyfile(str(fuente), str(destino))
def renombrarArchivosExternos(fileCarpeta,creador1Nombre):
    """
    creador1Nombre del tipo ("")->{""}
    """
    recorrerArchivosExternos(fileCarpeta,lambda f:f.rename(creador1Nombre(f.getName())))
def sustituirTextoEnArchivosExternos(fileCarpeta,textoOriginal,textoNuevo=None):
    if textoNuevo==None:
        textoNuevo=""
    recorrerArchivosExternos(fileCarpeta,lambda f:recorrerTextoYSustituir(f,textoOriginal,textoNuevo))

def recorrerTextoYSustituir(file,*a):
    utilizarLineYIndice=None
    leng=len(a)
    if leng==1:
        if esFuncion(a[0]):
            utilizarLineYIndice=a[0]
        elif esString(a[0]):
            def utilizarLineYIndice(line, indice):
                return line.replace(a[0], "")
    elif leng==2:
        #println("a[0]=",a[0])
        #println("a[1]=",a[1])
        #println("esListaAll(a[0],a[1])=", esListaAll(a[0],a[1]))
        if esLista(a[0]) and esString(a[1]):
            def utilizarLineYIndice(line, indice):
                for i in a[0]:
                    line=line.replace(i,a[1])
                return line
        elif esListaAll(a[0],a[1]):
            #println("fue utilizar")
            def utilizarLineYIndice(line, indice):
                for i in range(len(a[0])):
                    line=line.replace(a[0][i],a[1][i])
                return line
        elif esStringAll(a[0],a[1]):
            def utilizarLineYIndice(line, indice):
                return line.replace(a[0], a[1])
    recorrerTextoYSustituirBol(file,utilizarLineYIndice)

def recorrerCarpetaYUtilizar(file,utilizar):
    file=File.castear(file)
    if file.existe():
        if file.isDir():
            lf=file.listFiles()
            for i in lf:
                recorrerCarpetaYUtilizar(i,utilizar)
        else:
            utilizar(file)

def recorrerTextoYSustituirBol(file,utilizarLineYIndice):
    """
    utilizarLine del tipo ("",#i)->{"" o None si se quiere detener} pero aplica y detiene
    :param file:
    :param utilizarLine:
    :return:
    """
    f=File(file)
    if f.existe() and f.isFile():
        texto=leer(f)
        for i in range(len(texto)):
            res=utilizarLineYIndice(texto[i],i)
            if res!=None:
                seT(texto,i,res)
            else:
                break
        escribir(file,texto)

def getExtencion(dire):
    file = File.getFile(dire)
    name=file.getName()
    if contiene(name,"."):
        return name[name.rfind("."):len(name)]
    return ""
def getNombre(dire):
    file = File.getFile(dire)
    name = file.getName()
    if contiene(name, "."):
        indiceExtencion=name.rfind(".")
        return name[0:indiceExtencion]
    return name
def esFormatoTexto(file):
    #println("extencion=")
    return Or(getExtencion(file),".txt", ".java", ".html", ".xml", ".fxml", ".htm", ".js", ".xhtml")

def recorrerTextoEnArchivosExternos(file,utilizarFileYTexto):
    """
    utilizarFile del tipo (FileYTexto[])->{}
    :param file:
    :param utilizarTexto:
    :return:
    """
    def utilizarFile(f):
        if esFormatoTexto(f):
            #println("for=",f)
            utilizarFileYTexto(f,leer(f))

    recorrerArchivosExternos(file,utilizarFile)
def recorrerArchivosExternos(file,utilizarFile):
    """
    utilizarFile del tipo (File)->{}
    :param file:
    :param utilizarFile:
    :return:
    """
    file = File.getFile(file)
    if file.existe() and file.isDir():
        l=file.listFiles()
        leng=len(l)
        #for i in file.listFiles():
        for i in range(leng):
            e=l[i]
            if e.isFile():
                #println("f=",i)
                utilizarFile(e,i)
def recorrerArchivo(file,utilizarlineaYIndice):
    """
    utilizarlineaYIndice del tipo ("",indice)->{}
    :param file:
    :param utilizarlineaYIndice:
    :return:
    """
    file=File.getFile(file)
    if file.existe() and file.isFile():
        lineas=leer(file)
        #println("lee")
        for i in range(len(lineas)):
            utilizarlineaYIndice(lineas[i],i)

def recorrerCarpetaYCrearSubCarpetasImagen(carpetaOriginal,carpetaSalida,utilizar):
    def accion(f: File):
        if f.isDir():
            pass
        else:
            destino = File(strg(carpetaSalida, f.getSubFile()))
            if not destino.getParentFile().existe():
                crearCarpeta(destino.getParentFile())
            utilizar(f,destino)

    recorrerCarpetaYUtilizarSubCarpetas_BolEntrar(carpetaOriginal, accion)


def recorrerCarpetaYUtilizarSubCarpetas(file,utilizar,esCarpetaPadre=True):
    file=File.castear(file)
    if file.existe():
        if file.isDir():
            lf=file.listFiles()
            for i in lf:
                recorrerCarpetaYUtilizarSubCarpetas(i,utilizar,False)
        if not esCarpetaPadre:
            utilizar(file)





def recorrerCarpetaYUtilizarSubCarpetas_BolEntrar(file,utilizar,esCarpetaPadre=True,profundidad=0):#,subRecorrido=None
    # utilizar (f,profundidad)
    file=File.castear(file)
    if file.existe():
        if not esCarpetaPadre:
            if utilizar(file,profundidad)==False:
                return None
        # else:
        #     if file.subDireccion == None:
        #         file.subDireccion = file.getName()
        #         file.subCarpeta=""
        if file.isDir():

            lf=file.listFiles()
            for f in lf:
                # i.subCarpeta="/"+file.subDireccion
                # i.subDireccion=i.subCarpeta
                # subRecorridoActual=subRecorrido+"/"+i.getName()
                recorrerCarpetaYUtilizarSubCarpetas_BolEntrar(f,utilizar,False,(profundidad+1))#,subRecorridoActual

def recorrerCarpetaYUtilizarSubCarpetas_BolContinuar(file,utilizar,esCarpetaPadre=True,profundidad=0):#,subRecorrido=None
    # utilizar (f,profundidad)
    file=File.castear(file)
    if file.existe():
        if not esCarpetaPadre:
            if utilizar(file,profundidad)==False:
                return False
        # else:
        #     if file.subDireccion == None:
        #         file.subDireccion = file.getName()
        #         file.subCarpeta=""
        if file.isDir():

            lf=file.listFiles()
            for f in lf:
                # i.subCarpeta="/"+file.subDireccion
                # i.subDireccion=i.subCarpeta
                # subRecorridoActual=subRecorrido+"/"+i.getName()
                if not recorrerCarpetaYUtilizarSubCarpetas_BolEntrar(f,utilizar,False,(profundidad+1)):#,subRecorridoActual
                    return False
        return True
    return False


def delete(direccion):
    file=File.castear(direccion)
    if file.isDir():
        def eliminar(fil):
            println("delete: ",fil)
            if fil.isFile():
                os.remove(str(fil))
            else:
                os.rmdir(str(fil))
        recorrerCarpetaYUtilizarSubCarpetas(file, eliminar)
        println("delete final: ", file)
        os.rmdir(str(file))
        #os.removedirs(str(file))
    else:
        os.remove(str(file))
def existe(direccion):

    return os.path.exists(direccion)
def crearCarpeta(direccion):
    File(direccion).mkdirs()
def crearCSV(direccion,contenido):
    if  not endsWithOR(direccion,".csv"):
        direccion+=".csv"
    doc=open(direccion,"w")
    doc_csv_w = csv.writer(doc)
    if esMatrisLista(contenido):
        doc_csv_w.writerows(contenido)
    doc.close()

def crearTAR(direccion,*contenido):
    if  not endsWithOR(direccion,".tar.gz"):
        direccion+=".tar.gz"
    var=tarfile.open(direccion,"w:gz")
    #print(var)
    #print(type(var))
    for i in contenido:
        var.add(i)
    var.close()
#def descomprimirZip(direccion,direccionDeSalida):
    #var = zipfile.ZipFile(direccion, "w")
    #print(var)
    #var.extractall(direccionDeSalida)
#	return var
def crearZIP(direccion,*contenido):
    if  not endsWithOR(direccion,".zip"):
        direccion+=".zip"
    var = zipfile.ZipFile(direccion, "w")
    for i in contenido:
        var.write(i)
    return var
def leerJSON_Texto(direccion):
    """
    retorna un diccionario
    :param direccion:
    :return:
    """
    if  not endsWithOR(direccion,".json"):
        direccion+=".json"
    return json.load(open(direccion))
def leerXML_Etiqueta(direccion,etiqueta):
    """
    return un [] con los textos
    :param direccion:
    :param etiqueta:
    :return:
    """
    res=[]
    if  not endsWithOR(direccion,".xml"):
        direccion+=".xml"
    xml_doc=parse(direccion)
    for ele in xml_doc.findall(etiqueta):
        res.append(ele.text)
    return res


def esTextIOWrapper(archivo_texto):
    return isinstance(archivo_texto,TextIOWrapper)

def crear(direccion):
    return open(direccion,"w")

def abrirLectura(direccion):
    #print(direccion)
    #print(type(direccion))

    #println("existe=",File(direccion).existe())
    return open(direccion,"r")#r

def abrir(direccion):
    return open(direccion,"r+")

def escribir(direccion,contenido):
    #println("di=",direccion," contenido=",contenido)
    direccion=str(direccion)
    archivo_texto=crear(direccion)
    if esString(contenido):
        archivo_texto.write(contenido)
    elif esLista(contenido):
        #println("dire=",direccion)
        #println("exits=",File(direccion).existe())
        for x in contenido:
            archivo_texto.write(lne(x))#archivo_texto.write(str(str(x)+"\n"))
    archivo_texto.close()
    return archivo_texto

def append(archivo_texto,contenido):
    if esTextIOWrapper(archivo_texto):
        if esString(contenido):
            archivo_texto.write(ln(contenido))
        elif esLista(contenido):
            for x in contenido:
                archivo_texto.write(lne(x))
        #archivo_texto.write(ln(contenido))#archivo_texto.write(str("\n"+str(contenido)))
    elif esString(archivo_texto):
        archivo=open(archivo_texto,"a")
        append(archivo,contenido)
        archivo.close()


def leerConLn(archivo_texto):
    """
    [lineas] pero con linea +ln
    :param archivo_texto:
    :return:
    """
    archivo_texto = File.getStr(archivo_texto)
    if esString(archivo_texto):
        return leerConLn(abrirLectura(archivo_texto))#return leer(open(archivo_texto,"r"))
    elif esTextIOWrapper(archivo_texto):
        contenido=archivo_texto.read()
        archivo_texto.close()
        return contenido


def leer(archivo_texto):
    """
    [lineas]
    :param archivo_texto:
    :return:
    """
    archivo_texto=File.getStr(archivo_texto)
    #print(archivo_texto)
    #print(type(archivo_texto))
    if esString(archivo_texto):
        #println("archivo_texto=",archivo_texto)
        var=abrirLectura(archivo_texto)
        #println("var=", var)
        #println("type var=", type(var))
        var2=leer(var)
        return var2
    elif esTextIOWrapper(archivo_texto):
        contenido=MetodosUtiles.elminarLn(archivo_texto.readlines())
        archivo_texto.close()
        return contenido
def leerStr(archivo_texto):
    lista=leer(archivo_texto)
    res = ""
    for l in lista:
        res += str(l)+"\n"
    return res
def crearBinario(direccion,contenido):
    if esString(direccion):
        fichero_binario=open(direccion,"wb")
        pickle.dump(contenido,fichero_binario)
        fichero_binario.close()

def leerBinario(direccion):
    fichero=open(direccion,"rb")
    salida=pickle.load(fichero)
    fichero.close()
    return salida

def readBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData
def writeBinaryData(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

def readBinaryDataToHex(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData.hex()

def writeBinaryDataFromHex(hexStr, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(bytes.fromhex(hexStr))

