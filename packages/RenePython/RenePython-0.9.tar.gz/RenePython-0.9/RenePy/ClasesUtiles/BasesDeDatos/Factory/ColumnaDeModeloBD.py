from RenePy.MetodosUtiles.Imports.MetodosUtilesBasicos import *
from RenePy.ClasesUtiles.Tipos.TipoDeDatoSQL import TipoDeDatoSQL
from RenePy.ClasesUtiles.Tipos.TipoDeClasificacionSQL import TipoDeClasificacionSQl
from RenePy.ClasesUtiles.Tipos.TipoDeOrdenamientoSQL import TipoDeOrdenamientoSQL
from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar
class ColumnaDeModeloBD:
    def __init__(self,nombre:str,tipo:TipoDeDatoSQL=TipoDeDatoSQL.VARCHAR,tamaño:int=-1,clasificaciones:List[TipoDeClasificacionSQl]=None):
        self.Nombre:str=nombre
        self.Tipo:TipoDeDatoSQL=tipo
        self.Tamaño:int=tamaño
        if clasificaciones is None:
            clasificaciones=[]
        self.Clasificaciones:List[TipoDeClasificacionSQl]=clasificaciones

        self.ReferenciaID=None#Tipo ModeloBD
        self.ValorDefault=None

    def EsPrimaryKey(self)->bool:
        return contieneOR(self.Clasificaciones,TipoDeClasificacionSQl.PRIMARY_KEY,TipoDeClasificacionSQl.PRIMARY_KEY_AUTOINCREMENT)
