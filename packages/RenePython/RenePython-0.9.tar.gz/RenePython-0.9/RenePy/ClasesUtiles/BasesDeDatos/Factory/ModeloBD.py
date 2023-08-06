from RenePy.ClasesUtiles.BasesDeDatos.Factory.ColumnaDeModeloBD import ColumnaDeModeloBD
from RenePy.ClasesUtiles.Tipos.TipoDeDatoSQL import TipoDeDatoSQL
from RenePy.ClasesUtiles.Tipos.TipoDeClasificacionSQL import TipoDeClasificacionSQl
from RenePy.ClasesUtiles.Tipos.TipoDeOrdenamientoSQL import TipoDeOrdenamientoSQL
from RenePy.ClasesUtiles.BasesDeDatos.BDConexion import BDConexion
from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar
class ModeloBD:
    def __init__(self):
        self.Nombre:str=None
        self.Columnas:List[ColumnaDeModeloBD]=None
        self.SuscritaAUpdates:bool=None
    def addC(self,nombre:str,tipo:TipoDeDatoSQL=TipoDeDatoSQL.VARCHAR,tamaño:int=-1,clasificaciones:List[TipoDeClasificacionSQl]=None):
        c=ColumnaDeModeloBD(nombre=nombre
                            ,tipo=tipo
                            ,tamaño=tamaño
                            ,clasificaciones=clasificaciones)
        self.Columnas.append(c)
    def crearTabla(self,bd:BDConexion):
        args=[]
        for c in self.Columnas:
            args.append(c.Nombre)
            if c.Tipo!=TipoDeDatoSQL.VARCHAR or (c.Tamaño>0 and c.Tamaño!=256):
                args.append(c.Tipo)
            if c.Tamaño>0 and c.Tamaño!=256 and c.Tipo==TipoDeDatoSQL.VARCHAR:
                args.append(c.Tamaño)
            for cl in c.Clasificaciones:
                args.append(cl)

        bd.crearTablaYBorrarSiExiste(self.Nombre)
