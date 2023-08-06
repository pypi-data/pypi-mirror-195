import ctypes
from datetime import datetime,date,time,timedelta
from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar
import random
import traceback

# def crearAletoriedad(cantidadDeCaracteres):
#     #

def separadorDePalabrasEnTextoUnido(palabra:str):
    listaDePalabras=[]
    #palabraActual = ""
    p=[""]
    def appenC(c):
        p[0]+=c


    def agregarPalabra():
        if len(p[0])>0:
            listaDePalabras.append(p[0])
            p[0]=""

    elAnteriorFueNumero=False
    for c in palabra:
        if c.isnumeric():
            if not elAnteriorFueNumero:
                agregarPalabra()
            appenC(c)
            elAnteriorFueNumero=True
            continue
        else:
            elAnteriorFueNumero=False
        if c.isupper():
            agregarPalabra()
            appenC(c)
        elif c=="_" or c.isspace():
            agregarPalabra()
        elif c.isalpha():
            appenC(c)
    agregarPalabra()
    return  listaDePalabras
def getKward(nombreParametro,**kwargs):
    return kwargs.pop(nombreParametro)

def appenDic(dic=None,dicNew=None):
    if dicNew is not None:
        for k in dicNew.keys():
            dic[k] = dicNew[k]
    return dic


def isNoneAll(*a):
    for e in a:
        if e is not None:
            return False
    return True
def isNoneOR(*a):
    for e in a:
        if e is None:
            return True
    return False

def replaceAll(palabra:str,*a):
    pos=0
    old=""
    for p in a:
        if pos==0:
            old=p
        elif pos==1:
            palabra=palabra.replace(old,p)
        pos = (pos + 1) % 2
    return palabra

def toInt(a):
    if a==None:
        return None
    return int(a)
def toFloat(a):
    if a==None:
        return None
    return float(a)



def toBool(a):
    return eval(str(a).capitalize())
def strLista(lista):
    salida = "[ "
    for i in range(len(lista)):
        if i != 0:
            salida += " , "
        salida += str(lista[i])
    salida += " ]"
    return salida
def verLista(lista:List):
    salida=strLista(lista)
    println(salida)
    return salida


def verDicionario(diccionario:Dict):
    keys=diccionario.keys()
    for k in keys:
        print(str(k)+" : "+verLista(diccionario[k]))

def strg(*a):
    sal = ""
    for i in a:
        if i==None:
            sal+="None"
        else:
            sal += str(i)
    return sal

def println(*a):
    sal=""
    for i in range(len(a)):
        e=a[i]
        sal+=str(e)
    print(sal)

def esInt(a):
    if esBool(a):
        return False
    return isinstance(a, int)
def esFloat(a):
    return isinstance(a, float)
def esBool(a):
    return isinstance(a,bool)

def esIntOR(*a):
    for i in a:
        if(esInt(i)):
            return True
    return False
def esBoolOR(*a):
    for i in a:
        if(esBool(i)):
            return True
    return False
def esFloatOR(*a):
    for i in a:
        if(esFloat(i)):
            return True
    return False
def esStringOR(*a):
    for i in a:
        if(esString(i)):
            return True
    return False



def esIntAll(*a):
    for i in a:
        if not esInt(i):
            return False
    return True
def esBoolAll(*a):
    for i in a:
        if not esBool(i):
            return False
    return True
def esFloatAll(*a):
    for i in a:
        if not esFloat(i):
            return False
    return True
def esStringAll(*a):
    for i in a:
        if not esString(i):
            return False
    return True

def ln(a):
    return str("\n"+str(a))

def lne(a):
    return str(str(a)+"\n")

def esString(a):
    return isinstance(a,str)

def esFuncion(a):
    tipoStr=str(type(a))
    return tipoStr=="<class 'function'>" or tipoStr=="<type 'function'>"

def esLista(a):
    return isinstance(a,list)
def esListaAll(*a):
    for i in a:
        if not esLista(i):
            return False
    return True
def esTupla(a):
    return isinstance(a,tuple)
def esSet(a):
    return isinstance(a,set)
def esMap(a):
    return isinstance(a,dict)
def elminarLn(lista):
    if esLista(lista):
        listaSalida=[]
        for x in lista:
            listaSalida.append(x.replace("\n",""))
        else:
            return listaSalida
    
def addLneSiEsNecesario(lista):
    if esLista(lista):
        listaSalida=[]
        for x in lista:
            line=""
            if x.endswith("\n"):
                line=x
            else:
                line=lne(x)
            listaSalida.append(line)
        else:
            return listaSalida
def addSiNoContiene(l,valor):
    if not contiene(l,valor):
        l.append(valor)



def contiene(palabra,subContenido):
    if subContenido is None:
        return False
    if esString(palabra):
        return palabra.find(subContenido)!=-1
    if esSet(palabra):
        palabra=list(palabra)
    if esLista(palabra) or esTupla(palabra):
        try:
            return palabra.index(subContenido) != -1
        except:
            return False
    if esMap(palabra):
        listakeys=list(palabra.keys())
        return contiene(listakeys,subContenido)
def contieneOR(palabra,*subContenido):
    if len(subContenido)==1 and esLista(subContenido[0]):
        subContenido=subContenido[0]
    for i in subContenido:
        if contiene(palabra,i):
            return True
    return False


def tuplaRectificada(a):
    if esTupla(a) and len(a)==1 and esTupla(a[0]):
        return a[0]
    return a

def endsWithOR(a,*args):
    """
    args son las terminaciones
    :param a:
    :param args:
    :return:
    """
    b=tuplaRectificada(args)
    for i in b:
        if a.endswith(i):
            return True
    return False
def starWithOR(a,*b):
    """
    args son las terminaciones
    :param a:
    :param b:
    :return:
    """
    for i in b:
        if a.startswith(i):
            return True
    return False
def isEmpty(a):
    if esString(a) or esLista(a) or esTupla(a):
        return len(a)==0
def esMatrisLista(a):
    return esLista(a) and len(a)>0 and esLista(a[0])
def getScreenSize():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    anchoPantalla, altoPantalla = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return (anchoPantalla,altoPantalla)
def Or(a,*b):
    for i in b:
        if i==a:
            return True
    return False
def And(a,*b):
    for i in b:
        if i!=a:
            return False
    return True
def esDatepy(a):
    return isinstance(a,date)
def esDatetimepy(a):
    return isinstance(a,datetime)
def esTimepy(a):
    return isinstance(a,time)
def esTimedelta(a):
    return isinstance(a,timedelta)
def seT(a=[],indice=None,objeto=None):
    if esLista(a):
        res= a.pop(indice)
        a.insert(indice,objeto)
        return res
    if esTupla(a):
        a=list(a)
        seT(a)
        return a
def getExceptionStr():
    return traceback.format_exc()
def verException():
    print(getExceptionStr())