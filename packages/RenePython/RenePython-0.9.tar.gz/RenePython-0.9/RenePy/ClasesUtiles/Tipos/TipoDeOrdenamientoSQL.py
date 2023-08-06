class TipoDeOrdenamientoSQL:
    ASC=None
    DESC=None

    VALUES=None
    def __init__(self,valor):
        self.valor=valor
    def getValor(self):
        return self.valor
    @staticmethod
    def esTipoDeOrdenamientoSQL(a):
        return isinstance(a, TipoDeOrdenamientoSQL)
    @staticmethod
    def get(a):
        for i in TipoDeOrdenamientoSQL.VALUES:
            if a == i.getValor():
                return i
        return None
    @staticmethod
    def pertenece(a):
        return TipoDeOrdenamientoSQL.get(a) != None


TipoDeOrdenamientoSQL.ASC=TipoDeOrdenamientoSQL("ASC")
TipoDeOrdenamientoSQL.DESC=TipoDeOrdenamientoSQL("DESC")
TipoDeOrdenamientoSQL.VALUES=(TipoDeOrdenamientoSQL.ASC,TipoDeOrdenamientoSQL.DESC)



