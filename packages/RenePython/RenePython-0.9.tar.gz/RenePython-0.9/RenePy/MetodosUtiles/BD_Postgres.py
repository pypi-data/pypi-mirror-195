from RenePy.MetodosUtiles.Imports.MetodosUtilesBasicos import *
from RenePy.MetodosUtiles import SQL

import psycopg2

def execute(sql,database,host="localhost",port="5432", user="postgres", password="postgres",sqlUtil=None):
    if sqlUtil is None:
        sqlUtil=SQL.SQLs_Postgres()
    res=None

    miConecion = psycopg2.connect(host=host,port=port, database=database, user=user, password=password)
    miCursor = miConecion.cursor()
    if sql!=None:
        # if filas!=None:
        #     miCursor.executemany(sql,filas)
        # else:
        miCursor.execute(sql)
        # print("ver vars(miCursor):")
        # print(vars(miCursor))
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