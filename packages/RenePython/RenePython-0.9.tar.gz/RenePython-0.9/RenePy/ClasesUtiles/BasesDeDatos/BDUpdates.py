from RenePy.MetodosUtiles.Imports.MetodosUtilesBasicos import *
from RenePy.ClasesUtiles.BasesDeDatos import BDConexion
from RenePy.ClasesUtiles.Date import Date,toDate


from RenePy.ClasesUtiles.Tipos.TipoDeConexion import TipoDeConexion
from RenePy.ClasesUtiles.Tipos.TipoDeClasificacionSQL import TipoDeClasificacionSQL
from RenePy.ClasesUtiles.Tipos.TipoDeDatoSQL import TipoDeDatoSQL
from RenePy.ClasesUtiles.Tipos.TipoDeOrdenamientoSQL import TipoDeOrdenamientoSQL

#from RenePy.MetodosUtiles.SQL import fromBlob,toBlob
from RenePy.MetodosUtiles import SQL
from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar
import re
#from re import Pattern
PATRON_BDUPDATE_COLUMNA_INFORMACION = re.compile(r"[<][{](.*)[}][>]=[<][{](.*)")

TIPO_DE_MOTIVO_NO_ESPECIFICADO="TIPO_DE_MOTIVO_NO_ESPECIFICADO"
TIPO_DE_MOTIVO_CREADO="TIPO_DE_MOTIVO_CREADO"
class BDUpdate_Model:
    def __init__(self,idKey_Tabla,nombreTabla,contenido,motivo=TIPO_DE_MOTIVO_NO_ESPECIFICADO,fecha=None,idKey=None):
        self.idKey_Tabla=idKey_Tabla
        self.nombreTabla = nombreTabla

        self.contenido = contenido
        self.__contenidoStr=None
        self.__contenidoDic=None
        self.motivo = motivo
        if fecha==None:
            fecha=Date()
        self.fecha = fecha
        self.idKey=idKey

        self.__rowObj = None

        self.sqlUtil=SQL.SQLs()

    def getContenidoStr(self):
        if self.__contenidoStr==None:
            self.__contenidoStr=self.sqlUtil.fromBlob(self.contenido)
        return self.__contenidoStr
    def getValorEnColumna(self,nombreColumna):
        if self.__contenidoDic==None:
            self.getRowObj()
        return self.__contenidoDic[nombreColumna]
    def getRowObj(self):
        if self.__rowObj==None:
            self.__rowObj=[]
            if self.idKey_Tabla != None:
                self.__rowObj.append(self.idKey_Tabla)

            self.__contenidoDic = {}
            lista = self.getContenidoStr().split("}> ")
            for t in lista:
                re = PATRON_BDUPDATE_COLUMNA_INFORMACION.findall(t)
                for l in re:
                    self.__contenidoDic[l[0]] = l[1]
                    self.__rowObj.append(l[1])
        return self.__rowObj
    def print(self):
        u=self
        print("BDUpdate_Model: idKey=",u.idKey," idKey_Tabla=",u.idKey_Tabla,"\ncontenido=",u.getContenidoStr(),"\nmotivo=",u.motivo," fecha=",u.fecha)



class BDUpdates:
    TABLA_UPDATES = "TABLA_UPDATES"
    COLUMNA_ID_TABLA = "COLUMNA_ID_TABLA"
    COLUMNA_NOMBRE_TABLA = "COLUMNA_NOMBRE_TABLA"
    COLUMNA_CONTENIDO = "COLUMNA_CONTENIDO"
    COLUMNA_MOTIVO = "COLUMNA_MOTIVO"
    COLUMNA_FECHA="COLUMNA_FECHA"
    def __init__(self,BD:BDConexion):
        self.__BD:BDConexion=BD
    def createTabla(self):
        self.__BD.crearTablaYBorrarSiExiste(self.TABLA_UPDATES,
                                          self.COLUMNA_ID_TABLA,TipoDeClasificacionSQL.NOT_NULL,
                                          self.COLUMNA_NOMBRE_TABLA,50,TipoDeClasificacionSQL.NOT_NULL,
                                          self.COLUMNA_CONTENIDO,TipoDeDatoSQL.BLOB,TipoDeClasificacionSQL.NOT_NULL,
                                          self.COLUMNA_MOTIVO,50,TipoDeClasificacionSQL.NOT_NULL,
                                          self.COLUMNA_FECHA,TipoDeClasificacionSQL.NOT_NULL)
    def __get_Args(self,lista):
        bdum=BDUpdate_Model(idKey_Tabla=lista[1]
                               ,nombreTabla=lista[2]
                               ,contenido=lista[3]
                               ,motivo=lista[4]
                               ,fecha=toDate(lista[5])
                               ,idKey=lista[0])
        bdum.sqlUtil=self.__BD.sqlUtil
        return bdum
    def get(self,nombreTabla,idTabla,fecha):
        return self.__get_Args(self.__BD.select_Where_FirstRow(self.TABLA_UPDATES,
                                                               self.COLUMNA_NOMBRE_TABLA,nombreTabla,
                                                               self.COLUMNA_ID_TABLA,idTabla,
                                                               self.COLUMNA_FECHA,fecha))

    def addM(self, idKey_Tabla,nombreTabla,contenido,motivo=None,fecha=None):
        if motivo==None:
            motivo=TIPO_DE_MOTIVO_NO_ESPECIFICADO
        if esLista(contenido):
            c=""
            for l in contenido:
                c+=strg("<{",l[0],"}>=<{",l[1],"}> ")
            contenido=c
        contenido=self.__BD.sqlUtil.toBlob(contenido)
        bdum=BDUpdate_Model(idKey_Tabla, nombreTabla, contenido, motivo, fecha)
        bdum.sqlUtil = self.__BD.sqlUtil
        return self.__add(bdum)
    def __add(self,update:BDUpdate_Model):
        if update.idKey==None:
            self.__BD.insertar(self.TABLA_UPDATES,update.idKey_Tabla,
                               update.nombreTabla,update.contenido,
                               update.motivo,update.fecha)
        else:
            self.__BD.insertar(self.TABLA_UPDATES,update.idKey, update.idKey_Tabla,
                               update.nombreTabla, update.contenido,
                               update.motivo, update.fecha)
        return self.get(update.nombreTabla,update.idKey_Tabla,update.fecha)

    def getAll(self):
        O = self.__BD.select_Todo(self.TABLA_UPDATES)
        return [self.__get_Args(l) for l in O]
    def getInstanciasDesc_id(self,nombreTabla,id,creador_Args):
        O=self.__BD.select_Where_ORDER_BY(self.TABLA_UPDATES
                                          ,[self.COLUMNA_NOMBRE_TABLA,nombreTabla
                                          ,self.COLUMNA_ID_TABLA,id]
                                          ,self.COLUMNA_FECHA,TipoDeOrdenamientoSQL.DESC)
        return [creador_Args(self.__get_Args(l).getRowObj()) for l in O]
    def getLastUpdate(self,nombreTabla,id):
        O=self.__BD.select_FirstRow_Where_ValorMaximo(self.TABLA_UPDATES,self.COLUMNA_FECHA
                                             ,self.COLUMNA_NOMBRE_TABLA,nombreTabla
                                          ,self.COLUMNA_ID_TABLA,id)
        return self.__get_Args(O)
    def getLastInstancia(self,nombreTabla,id,creador_Args):
        return creador_Args(self.getLastUpdate(nombreTabla,id).getRowObj())
    def getInstancia(self,idUpdate,creador_Args):
        O=self.__BD.select_forID(self.TABLA_UPDATES,idUpdate)
        if O==None:
            return None
        return creador_Args(self.__get_Args(O).getRowObj())

