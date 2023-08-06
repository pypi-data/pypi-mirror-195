
class TipoDeClasificacionSQL:
    PRIMARY_KEY=None
    PRIMARY_KEY_AUTOINCREMENT=None
    UNIQUE=None
    NOT_NULL=None
    NULLABLE=None

    VALUES=None
    def __init__(self,valor):
        self.valor=valor
    def getValor(self):
        return self.valor
    @staticmethod
    def esTipoDeClasificacionSQl(a):
        return isinstance(a, TipoDeClasificacionSQL)
    @staticmethod
    def get(a):
        for i in TipoDeClasificacionSQL.VALUES:
            if a == i.getValor():
                return i
        return None
    @staticmethod
    def pertenece(a):
        return TipoDeClasificacionSQL.get(a) != None
    @staticmethod
    def esLlave(a):
        return a == TipoDeClasificacionSQL.PRIMARY_KEY or a == TipoDeClasificacionSQL.PRIMARY_KEY_AUTOINCREMENT

TipoDeClasificacionSQL.PRIMARY_KEY=TipoDeClasificacionSQL("PRIMARY KEY")
TipoDeClasificacionSQL.PRIMARY_KEY_AUTOINCREMENT=TipoDeClasificacionSQL("PRIMARY KEY AUTOINCREMENT")
TipoDeClasificacionSQL.UNIQUE=TipoDeClasificacionSQL("UNIQUE")
TipoDeClasificacionSQL.NOT_NULL=TipoDeClasificacionSQL("NOT NULL")
TipoDeClasificacionSQL.NULLABLE=TipoDeClasificacionSQL("NULLABLE")
#must be n, ne, e, se, s, sw, w, nw, or center
TipoDeClasificacionSQL.VALUES=(TipoDeClasificacionSQL.PRIMARY_KEY,TipoDeClasificacionSQL.PRIMARY_KEY_AUTOINCREMENT,TipoDeClasificacionSQL.UNIQUE,TipoDeClasificacionSQL.NOT_NULL,TipoDeClasificacionSQL.NULLABLE)







