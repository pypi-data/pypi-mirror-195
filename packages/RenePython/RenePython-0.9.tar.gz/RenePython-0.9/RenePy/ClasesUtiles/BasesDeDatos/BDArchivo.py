from RenePy.MetodosUtiles.Imports.MetodosUtilesBasicos import *
from RenePy.ClasesUtiles.BasesDeDatos import BDConexion
from RenePy.ClasesUtiles.Date import Date,toDate
from RenePy.MetodosUtiles import SQL,Archivo
from RenePy.ClasesUtiles.Tipos import TipoDeConexion,TipoDeClasificacionSQL,TipoDeDatoSQL

from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar
class BDArchivo_Model:
    def __init__(self, nombre, formato, contenido, descripcion=None, idkey=None):
        self.nombre = nombre
        self.formato = formato
        self.contenido = contenido
        self.descripcion = descripcion
        self.idkey = idkey
    def crearEn(self,url):
        return SQL.toBlob(fileABlob=url)
class BDArchivo:
    TABLA_ARCHIVO = "TABLA_ARCHIVO"
    COLUMNA_NOMBRE = "COLUMNA_NOMBRE"
    COLUMNA_FORMATO="COLUMNA_FORMATO"
    COLUMNA_CONTENIDO="COLUMNA_CONTENIDO"
    COLUMNA_DESCRIPCION = "COLUMNA_DESCRIPCION"
    def __init__(self,BD:BDConexion):
        self.__BD:BDConexion=BD
    def createTabla(self):
        self.__BD.crearTablaYBorrarSiExiste(self.TABLA_ARCHIVO,
                                          self.COLUMNA_NOMBRE,50,TipoDeClasificacionSQL.NOT_NULL,
                                          self.COLUMNA_FORMATO,25,TipoDeClasificacionSQL.NOT_NULL,
                                          self.COLUMNA_CONTENIDO,TipoDeDatoSQL.BLOB,TipoDeClasificacionSQL.NOT_NULL,
                                          self.COLUMNA_DESCRIPCION)



    def get_Args(self, listaArgumentos):
        return BDArchivo_Model(nombre=listaArgumentos[1]
                              , formato=listaArgumentos[2]
                              , contenido=listaArgumentos[3]
                              , descripcion=listaArgumentos[4]
                              , idkey=listaArgumentos[0])

    def get(self, id):
        O = self.__BD.select_forID(
            self.TABLA_ARCHIVO
            , id)
        if O == None:
            return None
        return self.get_Args(O)

    def insertar(self, archivo: BDArchivo_Model):
        if archivo.idkey != None:
            id = self.__BD.insertar(self.TABLA_ARCHIVO
                                    , archivo.nombre
                                    , archivo.formato
                                    , archivo.contenido
                                    , archivo.descripcion)
            return self.get(id)
        else:
            self.__BD.insertar_SinIdAutomatico(self.TABLA_ARCHIVO, archivo.idkey
                               , archivo.nombre
                               , archivo.formato
                               , archivo.contenido
                               , archivo.descripcion)
            return self.get(archivo.idkey)

    def cargar(self, url, descripcion=None):
        if Archivo.existe(url):
            bold = SQL.toBlob(fileABlob=url)
            extencion = Archivo.getExtencion(url)
            nombre = Archivo.getNombre(url)
            return BDArchivo_Model(nombre=nombre
                                  , formato=extencion
                                  , contenido=bold
                                  , descripcion=descripcion)
        return None

    def insertarDesdeUrl(self, url, descripcion=None):
        return self.insertar(self.cargar(url, descripcion))




