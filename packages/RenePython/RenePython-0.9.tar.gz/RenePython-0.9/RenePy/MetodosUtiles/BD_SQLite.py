from RenePy.MetodosUtiles.Imports.MetodosUtilesBasicos import *
from RenePy.MetodosUtiles import SQL
import sqlite3

def crearDB(nombreBD):
    execute(nombreBD)

def crearTabla(nombreBD,NombreTabla,*nombre_tipos,sqlUtil=None):
    if sqlUtil is None:
        sqlUtil=SQL.SQLs()
    execute(nombreBD,sqlUtil.crearTabla(NombreTabla,tuplaRectificada(nombre_tipos)))

def execute(nombreBD,sql=None,filas=None,sqlUtil=None):
    if sqlUtil is None:
        sqlUtil=SQL.SQLs()
    res=None

    miConecion = sqlite3.connect(nombreBD)
    miCursor = miConecion.cursor()
    if sql!=None:
        if filas!=None:
            miCursor.executemany(sql,filas)
        else:
            miCursor.execute(sql)
            if sqlUtil.esInsertar(sql):
                res= miCursor.lastrowid
        if sqlUtil.esSelect(sql):
            res=miCursor.fetchall()
            #println("SQL.esSelectValor(sql)",SQL.esSelectValor(sql))
            if sqlUtil.esSelectValor(sql):
                res=res[0][0]

    miConecion.commit()
    miCursor.close()
    miConecion.close()
    return res


    """
    def executeMany(nombreBD, sql=None,filas=[]):
    res = None

    miConecion = sqlite3.connect(nombreBD)
    miCursor = miConecion.cursor()
    if sql != None:
        res = miCursor.executemany(sql,filas)
    miConecion.commit()
    miCursor.close()
    miConecion.close()
    return res
def _realizarEjecucion(nombreBD,listener=None):
    """
#    listener del tipo (sqlite3.Connection)
#    :param nombreBD:
#    :param listener:
#    :return:
    """
    miConecion = sqlite3.connect(nombreBD)
    if listener!=None:
        listener(miConecion)
    miConecion.close()
"""