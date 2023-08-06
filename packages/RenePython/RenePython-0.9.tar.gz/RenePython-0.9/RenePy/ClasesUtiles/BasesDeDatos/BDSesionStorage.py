from RenePy.MetodosUtiles.Imports.MetodosUtilesBasicos import *
from RenePy.ClasesUtiles.BasesDeDatos import BDConexion
from RenePy.ClasesUtiles.Date import Date,toDate
from RenePy.MetodosUtiles import SQL,Archivo
#from RenePy.ClasesUtiles.Tipos import TipoDeConexion,TipoDeClasificacionSQL,TipoDeDatoSQL
from RenePy.ClasesUtiles.Tipos.TipoDeConexion import TipoDeConexion
from RenePy.ClasesUtiles.Tipos.TipoDeClasificacionSQL import TipoDeClasificacionSQL
from RenePy.ClasesUtiles.Tipos.TipoDeDatoSQL import TipoDeDatoSQL

from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar


class BDSesionStorage_Model:
    def __init__(self,sesion,propiedad,valor,idkey=None):
        self.sesion=sesion
        self.propiedad = propiedad
        self.valor = valor
        self.idkey=idkey
    def crearEn(self,url):
        return SQL.toBlob(fileABlob=url)



class BDSesionStorage:
    TABLA_SESION_STORAGE = "TABLA_SESION_STORAGE"
    COLUMNA_SESION = "COLUMNA_SESION"
    COLUMNA_PROPIEDAD="COLUMNA_PROPIEDAD"
    COLUMNA_VALOR="COLUMNA_VALOR"

    def __init__(self,BD:BDConexion):
        self.__BD:BDConexion=BD
    def createTabla(self):
        self.__BD.crearTablaYBorrarSiExiste(self.TABLA_SESION_STORAGE,
                                          self.COLUMNA_SESION,TipoDeClasificacionSQL.NOT_NULL,
                                          self.COLUMNA_PROPIEDAD,TipoDeClasificacionSQL.NOT_NULL,
                                          self.COLUMNA_VALOR,TipoDeDatoSQL.BLOB)

    def get_Args(self, listaArgumentos):
        return BDSesionStorage_Model(sesion=listaArgumentos[1]
                            , propiedad=listaArgumentos[2]
                            ,valor = listaArgumentos[3]
                            , idkey=listaArgumentos[0])

    def get_id(self, id):
        O = self.__BD.select_forID(
            self.TABLA_SESION_STORAGE
            , id)
        if O == None:
            return None
        return self.get_Args(O)
    def get(self, sesion,propiedad,valorDefault=None):
        O = self.__BD.select_Where_FirstResult(
            self.TABLA_SESION_STORAGE,self.COLUMNA_VALOR,self.COLUMNA_SESION,sesion,self.COLUMNA_PROPIEDAD,propiedad)
        if O == None:
            self.insertar(BDSesionStorage_Model(sesion=sesion
                                                ,propiedad=propiedad
                                                ,valor=valorDefault))
            return valorDefault
        return O
    def put(self, sesion,propiedad,valor):
        O = self.__BD.select_Where_FirstRow(
            self.TABLA_SESION_STORAGE, self.COLUMNA_SESION, sesion, self.COLUMNA_PROPIEDAD,propiedad)
        if O == None:
            self.insertar(BDSesionStorage_Model(sesion=sesion
                                                , propiedad=propiedad
                                                , valor=valor))
        else:
            storage=self.get_Args(O)
            self.__BD.update_Id(self.TABLA_SESION_STORAGE,storage.idkey,self.COLUMNA_VALOR,valor)
        return self
    def getInt(self, sesion,propiedad,valorDefault=None):
        return int(self.get(sesion,propiedad,valorDefault))
    def getFloat(self, sesion,propiedad,valorDefault=None):
        return float(self.get(sesion,propiedad,valorDefault))
    def getBool(self, sesion,propiedad,valorDefault=None):
        return toBool(self.get(sesion,propiedad,valorDefault))
    def getDate(self, sesion,propiedad,valorDefault=None):
        return toDate(self.get(sesion,propiedad,valorDefault))

    def insertar(self,storage:BDSesionStorage_Model):
        if storage.idkey==None:
            id=self.__BD.insertar(self.TABLA_SESION_STORAGE
                             , storage.sesion
                             , storage.propiedad
                             , storage.valor)
            return self.get_id(id)
        else:
            self.__BD.insertar_SinIdAutomatico(self.TABLA_SESION_STORAGE , storage.idkey
                               , storage.sesion
                               , storage.propiedad
                               , storage.valor)
            return self.get_id(storage.idkey)
