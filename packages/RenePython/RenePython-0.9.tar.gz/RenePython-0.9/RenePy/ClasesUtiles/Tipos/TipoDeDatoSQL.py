from RenePy.MetodosUtiles.MetodosUtiles import *
from datetime import datetime,date
class TipoDeDatoSQL:
    INTEGER=None
    VARCHAR=None
    REAL=None
    DATE=None
    TIME=None
    POINT=None
    BOOLEAN=None
    DOUBLE_PRECISION=None
    BLOB=None
    SERIAL=None
    VALUES=None
    def __init__(self,valor,default):
        self._valor=valor
        self._default=default
    def getValor(self):
        return self._valor
    def getDefault(self):
        return self._default
    @staticmethod
    def esTipoDeDatoSQL(a):
        return isinstance(a, TipoDeDatoSQL)
    @staticmethod
    def get(a):
        for i in TipoDeDatoSQL.VALUES:
            if a == i.getValor():
                return i
        return None
    @staticmethod
    def pertenece(a):
        return TipoDeDatoSQL.get(a) != None
    @staticmethod
    def getTipoDeDatoSQL(a):
        if esString(a):
            return TipoDeDatoSQL.VARCHAR
        elif esBool(a):
            return TipoDeDatoSQL.BOOLEAN
        elif esInt(a):
            return TipoDeDatoSQL.INTEGER
        elif esFloat(a):
            return TipoDeDatoSQL.DOUBLE_PRECISION
        return None

TipoDeDatoSQL.INTEGER=TipoDeDatoSQL("INTEGER",0)
TipoDeDatoSQL.VARCHAR=TipoDeDatoSQL("VARCHAR","")
TipoDeDatoSQL.REAL=TipoDeDatoSQL("REAL",0)
TipoDeDatoSQL.DATE=TipoDeDatoSQL("DATE",None)
TipoDeDatoSQL.TIME=TipoDeDatoSQL("TIME",None)
TipoDeDatoSQL.POINT=TipoDeDatoSQL("POINT",(0,0))
TipoDeDatoSQL.BOOLEAN=TipoDeDatoSQL("BOOLEAN",False)
TipoDeDatoSQL.DOUBLE_PRECISION=TipoDeDatoSQL("DOUBLE PRECISION",0)
TipoDeDatoSQL.SERIAL=TipoDeDatoSQL("SERIAL",None)
TipoDeDatoSQL.BLOB=TipoDeDatoSQL("BLOB",None)

#must be n, ne, e, se, s, sw, w, nw, or center
TipoDeDatoSQL.VALUES=(TipoDeDatoSQL.INTEGER,TipoDeDatoSQL.VARCHAR,TipoDeDatoSQL.REAL,TipoDeDatoSQL.DATE,TipoDeDatoSQL.TIME,TipoDeDatoSQL.POINT,TipoDeDatoSQL.BOOLEAN,TipoDeDatoSQL.DOUBLE_PRECISION,TipoDeDatoSQL.BLOB,TipoDeDatoSQL.SERIAL)






