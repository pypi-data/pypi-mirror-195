
class TipoDeConexion:
    SQLITE=None
    POSTGRE_SQL=None
    MY_SQL=None

    VALUES=None
    def __init__(self,valor):
        self.valor=valor
    def getValor(self):
        return self.valor
    @staticmethod
    def get(a):
        for i in TipoDeConexion.VALUES:
            if a == i.getValor():
                return i
        return None
    @staticmethod
    def esTipoDeConexion(a):
        return isinstance(a,TipoDeConexion)
    @staticmethod
    def pertenece(a):
        return TipoDeConexion.get(a) != None

TipoDeConexion.SQLITE=TipoDeConexion("sqlite")
TipoDeConexion.POSTGRE_SQL=TipoDeConexion("postgres")
TipoDeConexion.MY_SQL=TipoDeConexion("mysql")

#must be n, ne, e, se, s, sw, w, nw, or center
TipoDeConexion.VALUES=(TipoDeConexion.SQLITE,TipoDeConexion.POSTGRE_SQL,TipoDeConexion.MY_SQL)

# def esTipoDeConexion(a):
#     return isinstance(a,TipoDeConexion)

# def get(a):
#     for i in values:
#         if a==i.getValor():
#             return i
#     return None

# def pertenece(a):
#     return get(a)!=None