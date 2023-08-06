from builtins import list

from setuptools._vendor.pyparsing import White
#esTipoDeDatoSQ
from RenePy.MetodosUtiles.Imports.MetodosUtilesBasicos import *
#from RenePy.ClasesUtiles.Tipos import TipoDeDatoSQL
from RenePy.ClasesUtiles.Tipos.TipoDeDatoSQL import TipoDeDatoSQL
from RenePy.ClasesUtiles.Tipos.TipoDeClasificacionSQL import TipoDeClasificacionSQL

from RenePy.ClasesUtiles.Tipos.TipoDeOrdenamientoSQL import TipoDeOrdenamientoSQL

from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar

from io import open


class Configuracion_De_Columnas:

    def __init__(self):
        self.nombreTablas = []
        self.columnasSeleccionadas = [[]]

    def addSiNoContiene(self, t, c):
        addSiNoContiene(self.nombreTablas, t)
        i = self.nombreTablas.index(t)
        if len(self.columnasSeleccionadas) == i:
            self.columnasSeleccionadas.append([])
        addSiNoContiene(self.columnasSeleccionadas[i], c)

    def getParTC_siSeEncuentra(self, c):  # admitirContiene
        b = str(c)
        leng3 = len(self.nombreTablas)
        for i in range(leng3):
            # if b.startswith(nombreTablas[i] + ".") or (admitirContiene and contiene(columnasSeleccionadas[i], b)):
            if b.startswith(self.nombreTablas[i] + ".") or contiene(self.columnasSeleccionadas[i], b):
                return str(self.nombreTablas[i]) + "." + str(c)
        return str(c)  # -1;

    def getC_T(self, l, i):
        t = str(l[i][0])
        if len(l[i]) == 1:
            c = "id"
        else:
            c = str(l[i][1])
        self.addSiNoContiene(t, c)
        return t + "." + c


class SQLs:
    CREATE="CREATE"
    TABLE="TABLE"
    CREATE_TABLE=CREATE+" "+TABLE
    PRIMARY_KEY="PRIMARY KEY"
    INSERT="INSERT"
    INTO="INTO"
    INSERT_INTO=INSERT+" "+INTO
    VALUES="VALUES"
    SELECT="SELECT"
    MAX="MAX"
    MIN="MIN"
    AVG="AVG"
    SELECT_MAX=SELECT+" "+MAX
    SELECT_MIN=SELECT+" "+MIN
    SELECT_AVG=SELECT+" "+AVG
    FROM="FROM"
    DROP="DROP"
    DROP_TABLE=DROP+" "+TABLE
    COPY="COPY"
    WHERE="WHERE"
    ORDER_BY="ORDER BY"
    DISTINCT="DISTINCT"
    SELECT_DISTINCT=SELECT+" "+DISTINCT
    INNER_JOIN="INNER JOIN"
    ON="ON"
    GROUP_BY="GROUP BY"
    HAVING="HAVING"
    COUNT="COUNT"
    SUM="SUM"
    SELECT_COUNT="SELECT COUNT"
    SELECT_SUM="SELECT SUM"
    UPDATE="UPDATE"
    SET="SET"
    DELETE="DELETE"
    DROP="DROP"
    #DROP_TABLE="DROP TABLE"
    IF_EXISTS="IF EXISTS"
    DROP_TABLE_IF_EXISTS=DROP_TABLE+" "+IF_EXISTS
    AUTOINCREMENT="AUTOINCREMENT"
    IF_NOT_EXISTS = "IF NOT EXISTS"
    CREATE_TABLE_IF_NOT_EXISTS = CREATE_TABLE + " " + IF_NOT_EXISTS
    ALTER="ALTER"
    ALTER_TABLE=ALTER+" "+TABLE
    COLUMN="COLUMN"
    DROP_COLUMN=DROP+" "+COLUMN
    CASCADE="CASCADE"
    RENAME="RENAME"
    RENAME_COLUMN=RENAME+" "+COLUMN
    TO="TO"
    ADD="ADD"
    ADD_COLUMN=ADD+" "+COLUMN
    DEFAULT="DEFAULT"
    NOT_NULL="NOT NULL"
    SERIAL="SERIAL"


    def toBlob(self,cadenaABlob=None,fileABlob=None):
        if cadenaABlob!=None:
            return cadenaABlob.encode("utf-16").hex()
        with open(fileABlob, 'rb') as file:
            blobData = file.read()
        return blobData.hex()
    def fromBlob(self,blobStr,fileACrear=None):
        if fileACrear==None:
            return bytes.fromhex(blobStr).decode("utf-16")
        with open(fileACrear, 'wb') as file:
            file.write(bytes.fromhex(blobStr))



    def __getStr_ORDER_BY(self,*a,inicioDeColumnas=0):
        sql=""
        leng=len(a)
        for i in range(inicioDeColumnas,leng):
            esOrdenamiento=TipoDeOrdenamientoSQL.esTipoDeOrdenamientoSQL(a[i])
            if esOrdenamiento:
                sql += " "+a[i].getValor()
            else:
                if i!=inicioDeColumnas:
                    sql+=" , "
                if esLista(a[i]):
                    t = str(a[i][0])
                    if not len(a[i]) > 1:
                        c = "id"
                    else:
                        c = str(a[i][1])
                    sql += t + "." + c
                else:
                    sql+=str(a[i])
        if sql=="":
            return ""
        return " "+SQLs.ORDER_BY+" "+sql

    def __getStr_Where(self,*paresColumnaValor,cnf:Configuracion_De_Columnas=None,inicioDePares=0):#principio
        a = paresColumnaValor
        sqlWhere = ""
        leng = len(a)
        if inicioDePares==None:
            inicioDePares=0
        if cnf==None:
            cnf=Configuracion_De_Columnas()

        pos = 0
        for i in range(inicioDePares, leng):
            if i != inicioDePares and pos == 0:
                sqlWhere += " AND "
            if pos == 0:
                if esLista(a[i]):
                    t = str(a[i][0])
                    if not len(a[i]) > 1:
                        c = "id"
                    else:
                        c = str(a[i][1])
                    if cnf!=None and cnf.addSiNoContiene!=None:
                        cnf.addSiNoContiene(t, c)
                    sqlWhere += t + "." + c
                else:
                    if cnf!=None and cnf.getParTC_siSeEncuentra!=None:
                        sqlWhere += cnf.getParTC_siSeEncuentra(str(a[i]))
                    else:
                        sqlWhere +=str(a[i])

            elif pos == 1:
                sqlWhere += " = "
                if esLista(a[i]):
                    t = str(a[i][0])
                    if not len(a[i]) > 1:
                        c = "id"
                    else:
                        c = str(a[i][1])
                    if cnf != None and cnf.addSiNoContiene != None:
                        cnf.addSiNoContiene(t, c)
                    sqlWhere += t + "." + c
                elif str(a[i]).startswith("(") and str(a[i]).endswith(")") and self.esSelect(str(a[i])[1:-1]):
                    sqlWhere += str(a[i])
                else:
                    sqlWhere += "'" + str(a[i]) + "'"
            pos = (pos + 1) % 2
        if sqlWhere != "":
            sqlWhere = " " + SQLs.WHERE + " " + sqlWhere
        return sqlWhere


    def __getFrom_Inner_Join_Where_ORDER_BY(self,select,*args):
        cnf = Configuracion_De_Columnas()
        tw=tuple(args[1])
        return self.__getFrom_Inner_Join(select,*args,cnf=cnf) +self.__getStr_Where(*tw,cnf=cnf,inicioDePares=0)+self.__getStr_ORDER_BY(*args,inicioDeColumnas=2)
    def __getFrom_Inner_Join_Where(self,select,*args):
        cnf = Configuracion_De_Columnas()
        return self.__getFrom_Inner_Join(select,*args,cnf=cnf) +self.__getStr_Where(*args,cnf=cnf,inicioDePares=1)
    def __getFrom_Inner_Join(self,select,*args,cnf:Configuracion_De_Columnas=None):
        """
            ELEMENTO RELACIONES ENTRE TABLAS (ON): siempre son [Pares]
                plq la lista de ellos es ejemplo:
                    [ [1 [T],[T,CID],[T,CID],[T] ] , [2 [T,CID],[T] ] , [3 [T,CID],[T,CID] ] ]
                recordar que siempre la un T en uno de los i tiene que aparecer en el siguiente(i+1) pq
                es un recorrido

            TABLA.CULUMNA_REFERENCIA_A_ID == a
                [T] ,[T,CID]  a TABLA.COLUMNA_NOMBRE_PERSONALIZADO_ID

                [T,CID],[T]  a TABLA.ID el default dado de automatico

                [T,CID],[T,CID]





            PAR COLUMNA VALOR
                [T,C],[T,C]

                [T,C],V

                C,[T,C]

                C,V

                [T],[T,C]   la [T] es [T,"id"]

                [T],V       la [T] es [T,"id"]

                C,[T]       la [T] es [T,"id"]



            (listaDe ELEMENTO RELACIONES ENTRE TABLAS,paresColumnaValor)

            ([TABLA,COLUMNA_REFERENCIA_ID],paresColumnaValor)

            :param nombreTabla:
            :param columna:
            :param args:
            :return:
            """
        if cnf==None:
            cnf=Configuracion_De_Columnas()
        a = args
        leng = len(a[0])
        sqlOn=""
        lSqlOn = []
        if leng > 0:
            if esString(a[0][0]):  # esto no sirve
                pass
            else:
                tabla1inerjoin = None  # la que se encuentra tambien en a[0][1]
                tablaFrom = None
                pos = 0
                len2 = len(a[0])
                for i in range(len2):
                    l = a[0][i]
                    sqlOn = ""
                    leng = len(l)
                    for j in range(leng):
                        if j != 0 and pos == 0:
                            sqlOn += " AND "
                        if pos == 0:
                            sqlOn += cnf.getC_T(l, j)
                        if pos == 1:
                            sqlOn += " = " + cnf.getC_T(l, j)
                        pos = (pos + 1) % 2
                        if i == 1 and tabla1inerjoin == None and l[j][0] == cnf.nombreTablas[1]:
                            tabla1inerjoin = cnf.nombreTablas[1]
                            tablaFrom = cnf.nombreTablas[0]
                    lSqlOn.append(sqlOn)
                if tabla1inerjoin == None:
                    tabla1inerjoin = cnf.nombreTablas[0]
                    tablaFrom = cnf.nombreTablas[1]
                sqlOn = SQLs.FROM + " " + tablaFrom + " " + SQLs.INNER_JOIN + " " + tabla1inerjoin
                len2 = len(lSqlOn)
                for i in range(len2):
                    if i != 0:
                        sqlOn += " " + SQLs.INNER_JOIN + " " + cnf.nombreTablas[i + 1]
                    sqlOn += " " + SQLs.ON + " " + lSqlOn[i]
        return select + sqlOn



    def addColumn(self,nombreTabla,Columna,tipo=TipoDeDatoSQL.VARCHAR,default=None,clasificacion=None):
        if default==None:
            default=tipo.getDefault()
        if clasificacion==None:
            clasificacion=""
        elif TipoDeClasificacionSQL.esTipoDeClasificacionSQl(clasificacion):
            clasificacion="  "+clasificacion.getValor()
        return SQLs.ALTER_TABLE+" "+nombreTabla+" "+SQLs.ADD_COLUMN+" "+Columna+" "+tipo.getValor()+" "+SQLs.DEFAULT+" "+default+clasificacion
    def renombrarColumna(self,nombreTabla,Columna,NuevoNombre):
        return SQLs.ALTER_TABLE+" "+nombreTabla+" "+SQLs.RENAME_COLUMN+" "+Columna+" "+SQLs.TO+" "+NuevoNombre

    def eliminarColumna(self,nombreTabla,Columna):
        return SQLs.ALTER_TABLE+" "+nombreTabla+" "+SQLs.DROP_COLUMN+" "+Columna+" "+SQLs.CASCADE
    def esSelect(self,sql=""):
        return sql.strip().upper().startswith(SQLs.SELECT+" ")
    def esInsertar(self,sql:str):
        return sql.strip().upper().startswith(SQLs.INSERT_INTO+" ")
    def esSelectValor(self,sql=""):
        sub=sql.strip().upper()[len(SQLs.SELECT + " "):]
        #println("sub="+sub)
        return starWithOR(sub, SQLs.MAX, SQLs.MIN, SQLs.AVG, SQLs.COUNT, SQLs.SUM)

    def crearTablaSiNoExiste(self,nombreTabla,*a):
        """
        (nombre,.. nombreColumna,TipoDeDatoSQL,capacidad#,isKeyPrimary o tipoDeClasificacionSQL)<br/>
     *  (nombre,.. nombreColumna,TipoDeDatoSQL,capacidad#)<br/> asumo que no es llave primaria
        (nombre,.. nombreColumna,capacidad#) asumo que es VARCHAR <br/>
        (nombre,.. nombreColumna) asumo que es VARCHAR(255)<br/>
        si el siguiente a nombreColumna no es un TipoDeDatoSQL asumo que es VARCHAR(255) <br/>
        si el siguiente a TipoDeDatoSQL no es un # asumo que es VARCHAR(255)  <br/>
        :param nombreTabla:
        :param a:
        :return:
        """
        return self.crearTabla(nombreTabla,*a).replace(SQLs.CREATE_TABLE, SQLs.CREATE_TABLE_IF_NOT_EXISTS, 1)
    def drop_table_if_exist(self,nombreTabla):
        return SQLs.DROP_TABLE_IF_EXISTS+" "+nombreTabla
    def delete_id(self,nombreTabla,id):
        return self.delete(self,nombreTabla,"id",id)
    def delete(self,nombreTabla,*args):
        """
        (nombreTabla,,whereColumna1,whereValor1,whereColumna2,whereValor2,...)
        :param nombreTabla:
        :param args:
        :return:
        """
        a = tuplaRectificada(args)
        leng = len(a)
        sqlWhere=""
        pos = 0
        for i in range(leng):
            if pos == 0:
                if not isEmpty(sqlWhere):
                    sqlWhere += " AND "
                sqlWhere += str(a[i])
            elif pos == 1:
                sqlWhere += "='" + str(a[i]) + "'"
            pos = (pos + 1) % 2
        return SQLs.DELETE+" "+SQLs.FROM+" "+nombreTabla+" "+SQLs.WHERE+" "+sqlWhere
    def update_Id(self,nombreTabla,id,*args):
        """
        (nombreTabla,id#,columna,setValor1,columna2,setValor2,... )
        :param nombreTabla:
        :param id:
        :param args:
        :return:
        """
        a = tuplaRectificada(args)
        leng = len(a)
        paresColumnaValor=[]
        for i in a:
            paresColumnaValor.append(i)
        return self.update(nombreTabla,paresColumnaValor,"id",id)
    def update(self,nombreTabla,paresColumnaValor,*args):
        """
        (nombreTabla,[columna,setValor1,columna2,setValor2,... ],whereColumna1,whereValor1,whereColumna2,whereValor2,...)
        :param nombreTabla:
        :param paresColumnaValor:
        :param args:
        :return:
        """
        a = tuplaRectificada(args)
        leng = len(a)
        sqlSet = ""
        sqlWhere=""

        leng2=len(paresColumnaValor)
        pos=0
        for i in range(leng2):
            if pos==0:
                if not isEmpty(sqlSet):
                    sqlSet+=" , "
                sqlSet+=str(paresColumnaValor[i])
            elif pos==1:
                sqlSet+="='"+str(paresColumnaValor[i])+"'"
            pos=(pos+1)%2
        pos=0
        for i in range(leng):
            if pos==0:
                if not isEmpty(sqlWhere):
                    sqlWhere+=" AND "
                sqlWhere+=str(a[i])
            elif pos==1:
                sqlWhere+="='"+str(a[i])+"'"
            pos = (pos + 1) % 2
            #print("nombreTabla=",nombreTabla)
        return SQLs.UPDATE+" "+nombreTabla+" "+SQLs.SET+" "+sqlSet+" "+SQLs.WHERE+" "+sqlWhere


    def select_Distinct_Group_By_By_Having(self,nombreTabla,columnas,grupBy,heavinColumna,heavinValor):
        return self.select_Group_By_Having(nombreTabla,columnas,grupBy,heavinColumna,heavinValor).replace(SQLs.SELECT + " ", SQLs.SELECT_DISTINCT + " ", 1)
    def select_Group_By_Having(self,nombreTabla,columnas,grupBy,heavinColumna,heavinValor):
        return self.select_Group_By(self,nombreTabla,columnas,grupBy)+" "+SQLs.HAVING+" "+heavinColumna+"="+heavinValor
    def select_Distinct_Group_By(self,nombreTabla,columnas,grupBy):
        return self.select_Group_By(self,nombreTabla,columnas,grupBy).replace(SQLs.SELECT + " ", SQLs.SELECT_DISTINCT + " ", 1)
    def select_Group_By(self,nombreTabla,columnas,grupBy):
        """
        (nombreTabla,[]columnas,grupBy)
        :param nombreTabla:
        :param args:
        :return:
        """
        return self.select(nombreTabla,tuple(columnas))+" "+SQLs.GROUP_BY+" "+grupBy

    def select_Where_Inner_Join_TodoDeTabla(self,nombreTabla,*args):#_Todo
        """
        (nombreTabla,listaDe ELEMENTO RELACIONES ENTRE TABLAS,paresColumnaValor)

        (nombreTabla,[TABLA,COLUMNA_REFERENCIA_ID],paresColumnaValor)

        ELEMENTO RELACIONES ENTRE TABLAS (ON): siempre son [Pares]
                plq la lista de ellos es ejemplo:
                    [ [1 [T],[T,CID],[T,CID],[T] ] , [2 [T,CID],[T] ] , [3 [T,CID],[T,CID] ] ]
                recordar que siempre la un T en uno de los i tiene que aparecer en el siguiente(i+1) pq
                es un recorrido

            TABLA.CULUMNA_REFERENCIA_A_ID == a
                [T] ,[T,CID]  a TABLA.COLUMNA_NOMBRE_PERSONALIZADO_ID

                [T,CID],[T]  a TABLA.ID el default dado de automatico

                [T,CID],[T,CID]





            PAR COLUMNA VALOR
                [T,C],[T,C]

                [T,C],V

                C,[T,C]

                C,V

                [T],[T,C]   la [T] es [T,"id"]

                [T],V       la [T] es [T,"id"]

                C,[T]       la [T] es [T,"id"]




        :param nombreTabla:
        :param args:
        :return:
        """
        return self.__getFrom_Inner_Join_Where(SQLs.SELECT + " " + nombreTabla + ".* ",*args)

    def select_Distinct_Todo_Where_Inner_Join(self,nombreTabla,*args):
        """
        (nombreTabla,listaDe ELEMENTO RELACIONES ENTRE TABLAS,paresColumnaValor)

        (nombreTabla,[TABLA,COLUMNA_REFERENCIA_ID],paresColumnaValor)

        ELEMENTO RELACIONES ENTRE TABLAS (ON): siempre son [Pares]
                plq la lista de ellos es ejemplo:
                    [ [1 [T],[T,CID],[T,CID],[T] ] , [2 [T,CID],[T] ] , [3 [T,CID],[T,CID] ] ]
                recordar que siempre la un T en uno de los i tiene que aparecer en el siguiente(i+1) pq
                es un recorrido

            TABLA.CULUMNA_REFERENCIA_A_ID == a
                [T] ,[T,CID]  a TABLA.COLUMNA_NOMBRE_PERSONALIZADO_ID

                [T,CID],[T]  a TABLA.ID el default dado de automatico

                [T,CID],[T,CID]





            PAR COLUMNA VALOR
                [T,C],[T,C]

                [T,C],V

                C,[T,C]

                C,V

                [T],[T,C]   la [T] es [T,"id"]

                [T],V       la [T] es [T,"id"]

                C,[T]       la [T] es [T,"id"]




        :param nombreTabla:
        :param args:
        :return:
        """
        return self.__getFrom_Inner_Join_Where(SQLs.SELECT_DISTINCT + " " + nombreTabla + ".* ",*args)

    def select_Todo_Where_Inner_Join_ORDER_BY(self,nombreTabla,*args):
        """
        (nombreTabla,listaDe ELEMENTO RELACIONES ENTRE TABLAS,where[paresColumnaValor],columnasDeOrden, o+ ordenaminento)

        (nombreTabla,[TABLA,COLUMNA_REFERENCIA_ID],where[paresColumnaValor],columnasDeOrden, o+ ordenaminento)

        ELEMENTO RELACIONES ENTRE TABLAS (ON): siempre son [Pares]
                plq la lista de ellos es ejemplo:
                    [ [1 [T],[T,CID],[T,CID],[T] ] , [2 [T,CID],[T] ] , [3 [T,CID],[T,CID] ] ]
                recordar que siempre la un T en uno de los i tiene que aparecer en el siguiente(i+1) pq
                es un recorrido

            TABLA.CULUMNA_REFERENCIA_A_ID == a
                [T] ,[T,CID]  a TABLA.COLUMNA_NOMBRE_PERSONALIZADO_ID

                [T,CID],[T]  a TABLA.ID el default dado de automatico

                [T,CID],[T,CID]





            PAR COLUMNA VALOR
                [T,C],[T,C]

                [T,C],V

                C,[T,C]

                C,V

                [T],[T,C]   la [T] es [T,"id"]

                [T],V       la [T] es [T,"id"]

                C,[T]       la [T] es [T,"id"]




        :param nombreTabla:
        :param args:
        :return:
        """
        return self.__getFrom_Inner_Join_Where_ORDER_BY(SQLs.SELECT + " " + nombreTabla + ".* ",*args)


    def select_Distinct_Where(self,nombreTabla,*args):
        return self.select_Where(nombreTabla, tuplaRectificada(args)).replace(SQLs.SELECT + " ", SQLs.SELECT_DISTINCT + " ", 1)
    def select_Distinct_Todo(self,nombreTabla):
        return self.select_Todo(nombreTabla).replace(SQLs.SELECT + " ", SQLs.SELECT_DISTINCT + " ", 1)
    def select_Distinct(self,nombreTabla,*args):
        return self.select(nombreTabla, tuplaRectificada(args)).replace(SQLs.SELECT + " ", SQLs.SELECT_DISTINCT + " ", 1)
    def select_Distinct_ORDER_BY(self,nombreTabla,*args):
        return self.select_ORDER_BY(nombreTabla, tuplaRectificada(args)).replace(SQLs.SELECT + " ", SQLs.SELECT_DISTINCT + " ", 1)
    def select_Distinct_Where_ORDER_BY(self,nombreTabla,*args):
        return self.select_Where_ORDER_BY(nombreTabla,tuplaRectificada(args)).replace(SQLs.SELECT+" ",SQLs.SELECT_DISTINCT+" ",1)
    def select_Where_ValorMaximo(self,nombreTabla,columnaValorMaximo,*paresColumnaValor):
        """
        (nombreTabla,columnaValorMaximo,paresColumnaValor)
        la idea es crear un subSql que seleccione el maximo valor utlizando los pares columna valor
        tanto en el sql(todo) como en el subSql
            SubSql
                SELECT MAX(nombreTabla.columnaValorMaximo) FROM nombreTabla WHERE pares columna valor
            sql(todo)
                 SELECT nombreTabla.columnaValorMaximo FROM  nombreTabla WHERE pares columna valor
                 AND columnaValorMaximo=(SubSql)

                 Ejemplo:
                     SELECT nombreTabla.columnaValorMaximo FROM  nombreTabla WHERE pares columna valor
                     AND columnaValorMaximo = ( SELECT MAX(nombreTabla.columnaValorMaximo) FROM nombreTabla WHERE pares columna valor )



        :param nombreTabla:
        :param columnaValorMaximo:
        :param paresColumnaValor:
        :return:
        """
        pares=list(paresColumnaValor)
        pares.append(columnaValorMaximo)
        pares.append("("+self.getValorMaximo_Where(nombreTabla,columnaValorMaximo,*paresColumnaValor)+")")
        pares=tuple(pares)
        return self.select_Where(nombreTabla,*pares)
    def select_Where_ORDER_BY(self,nombreTabla,*args):
        """
        (nombreTabla,columnas[],where[pares .. Columna-Valor],columnas por los que ordenar,o+ ordenamiento)
        (nombreTabla,where[pares .. Columna-Valor],columnas por los que ordenar,o+ ordenamiento)
        :param nombreTabla:
        :param args:
        :return:
        """
        #a = tuplaRectificada(args)
        a=args
        leng = len(a)
        # sql = ""
        inicioDeColumnas = 0
        sqlSelect = ""
        if leng > 0:
            if esLista(a[0]):
                inicioDeColumnas = 1
                if esLista(a[1]):
                    inicioDeColumnas = 2
                    lista2 = list(a[1])
                    lista2.insert(0, a[0])

                    sqlSelect = self.select_Where(nombreTabla, *tuple(lista2))
                else:
                    sqlSelect = self.select_Where(nombreTabla, *tuple(a[0]))
            else:
                sqlSelect = self.select_Todo(nombreTabla)
        #     for i in range(inicioDeColumnas, leng):
        #         esOrdenamiento = TipoDeOrdenamientoSQL.esTipoDeOrdenamientoSQL(a[i])
        #         if esOrdenamiento:
        #             sql += " " + a[i].getValor()
        #         else:
        #             if i != inicioDeColumnas:
        #                 sql += " , "
        #             sql += str(a[i])
        # return sqlSelect + " " + ORDER_BY + " " + sql
        return sqlSelect + " "+self.__getStr_ORDER_BY(*a,inicioDeColumnas=inicioDeColumnas)


    def select_ORDER_BY(self,nombreTabla,*args):
        """
        (nombreTabla,columnas[],where[pares .. Columna-Valor],columnas por los que ordenar,o+ ordenamiento)
        (nombreTabla,columnas[],columnas por los que ordenar,o+ ordenamiento)
        (nombreTabla,columnas por los que ordenar,o+ ordenamiento) selecciona todas las columnas
        :param nombreTabla:
        :param args:
        :return:
        """
        a = tuplaRectificada(args)
        leng = len(a)
        sql = ""
        inicioDeColumnas = 0
        sqlSelect = ""
        if leng > 0:
            if esLista(a[0]):
                inicioDeColumnas = 1
                if esLista(a[1]):
                    inicioDeColumnas = 2
                    lista2=list(a[1])
                    lista2.insert(0,a[0])
                    sqlSelect=self.select_Where(nombreTabla,tuple(lista2))
                else:
                    sqlSelect=self.select(nombreTabla,tuple(a[0]))
            else:
                sqlSelect=self.select_Todo(nombreTabla)
            for i in range(inicioDeColumnas,leng):
                esOrdenamiento=TipoDeOrdenamientoSQL.esTipoDeOrdenamientoSQL(a[i])
                if esOrdenamiento:
                    sql += " "+a[i].getValor()
                else:
                    if i!=inicioDeColumnas:
                        sql+=" , "
                    sql+=str(a[i])
        return sqlSelect+" "+SQLs.ORDER_BY+" "+sql
    def select_forID(self,nombreTabla,id):
        return self.select_Where(nombreTabla,"id",id)
    def select_Where(self,nombreTabla,*args):
        """
        (nombreTabla,columnas[],pares .. Columna-Valor)
        (nombreTabla,pares .. Columna-Valor)
        :param nombreTabla:
        :param args:
        :return:
        """
        #a = tuplaRectificada(args)
        a=args
        leng = len(a)
        sql = ""
        inicioDePares=0
        sqlSelect=""
        if leng>0:
            if esLista(a[0]):
                inicioDePares=1
                if not isEmpty(a[0]):
                    sqlSelect=self.select(nombreTabla,tuple(a[0]))
            if isEmpty(sqlSelect):
                sqlSelect=self.select_Todo(nombreTabla)
            #pos=0
        #     for i in range(inicioDePares,leng):
        #         if i!=inicioDePares and pos==0:
        #             sql+=" AND "
        #         if pos==0:
        #             sql+=str(a[i])
        #         elif pos==1:
        #             sql+=" = '"+str(a[i])+"'"
        #         pos=(pos+1)%2
        # return sqlSelect+" "+WHERE+" "+sql
        #return sqlSelect + __getStr_Where_Conf(None,inicioDePares,*args)
        return sqlSelect + self.__getStr_Where( *args,inicioDePares=inicioDePares)


    def select_Todo(self,nombreTabla):
        return self.select(nombreTabla,"*")
    def select(self,nombreTabla,*args):
        a=tuplaRectificada(args)
        leng=len(a)
        sql=""
        for i in range(leng):
            if i!=0:
                sql+=" , "
            sql+=str(a[i])
        return SQLs.SELECT+" "+sql+" "+SQLs.FROM+" "+nombreTabla

    def copyEnTXT(self,nombreTabla,direccion):
        if not isEmpty(direccion):
            if not direccion.endswith(".txt"):
                direccion+=".txt"
            return SQLs.COPY+" "+nombreTabla+" "+SQLs.FROM+" "+direccion
    def getPoint(self,X,Y):
        return "("+str(X)+","+str(Y)+")"
    def getDate(self,año,mes,dia):
        return str(año)+"-"+str(mes)+"-"+str(dia)

    def dropTable(self,nombreTabla):
        return SQLs.DROP_TABLE+" "+nombreTabla

    def getIdCorrespondiente(self,nombreTabla,id="id"):
        return "("+self.getValorMaximo(nombreTabla,id)+")+1"
    def getSuma(self,nombreTabla,columna):
        return SQLs.SELECT_SUM+"("+nombreTabla+"."+columna+") "+SQLs.FROM+" "+nombreTabla



    def getSuma_Where_Inner_Join(self,nombreTabla,columna,*args):
        return self.__getFrom_Inner_Join_Where(SQLs.SELECT_SUM + "(" + nombreTabla + "." + columna + ") ",*args)





    def getSuma_Where(self,nombreTabla,columna,*paresColumnaValor):
        return self.getSuma(nombreTabla,columna)+self.__getStr_Where(*paresColumnaValor)
    def getCantidad(self,nombreTabla,columna):
        return SQLs.SELECT_COUNT+"("+nombreTabla+"."+columna+") "+SQLs.FROM+" "+nombreTabla
    def getCantidad_Where(self,nombreTabla,*paresColumnaValor):

        return self.getCantidad(nombreTabla,paresColumnaValor[0])+self.__getStr_Where(*paresColumnaValor)
    def getCantidad_Where_Inner_Join(self,nombreTabla,columna,*args):
        return self.__getFrom_Inner_Join_Where(SQLs.SELECT_COUNT+"("+nombreTabla+"."+columna+") ",*args)
    def getValorPromedio(self,nombreTabla,columna):
        return SQLs.SELECT_AVG+"("+nombreTabla+"."+columna+") "+SQLs.FROM+" "+nombreTabla
    def getValorPromedio_Where_Inner_Join(self,nombreTabla,columna,*args):
        return self.__getFrom_Inner_Join_Where(SQLs.SELECT_AVG+"("+nombreTabla+"."+columna+") ",*args)
    def getValorPromedio_Where(self,nombreTabla,columna,*paresColumnaValor):
        return self.getValorPromedio(nombreTabla,columna)+self.__getStr_Where(*paresColumnaValor)
    def getValorMinimo(self,nombreTabla,columna):
        return SQLs.SELECT_MIN+"("+nombreTabla+"."+columna+") "+SQLs.FROM+" "+nombreTabla
    def getValorMinimo_Where_Inner_Join(self,nombreTabla,columna,*args):
        return self.__getFrom_Inner_Join_Where(SQLs.SELECT_MIN+"("+nombreTabla+"."+columna+") ",*args)
    def getValorMinimo_Where(self,nombreTabla,columna,*paresColumnaValor):
        return self.getValorMinimo(nombreTabla,columna)+self.__getStr_Where(*paresColumnaValor)
    def getValorMaximo(self,nombreTabla,columna):
        return SQLs.SELECT_MAX+"("+nombreTabla+"."+columna+") "+SQLs.FROM+" "+nombreTabla
    def getValorMaximo_Where_Inner_Join(self,nombreTabla,columna,*args):
        return self.__getFrom_Inner_Join_Where(SQLs.SELECT_MAX+"("+nombreTabla+"."+columna+") ",*args)
    def getValorMaximo_Where(self,nombreTabla,columna,*paresColumnaValor):
        return self.getValorMaximo(nombreTabla,columna)+self.__getStr_Where(*paresColumnaValor)

    def getLastId(self,nombreTabla):
        return self.getValorMaximo(nombreTabla,"id")
    def select_ConUltimoID(self,nombreTabla):
        return self.select_forID(nombreTabla,"("+self.getLastId(nombreTabla)+")")
    def insertar_ConIdAutomatico(self,nombreTabla,nombreId,*args):
        """
        (nombreTabla,valores una sola fila completa)
        (nombreTabla,[]columnas,valores)<br/>
        si no lo tiene pone el id de forma automatica con el nombre del argumento
        :param nombreTabla:
        :param nombreId:
        :param args:
        :return:
        """
        return self.__insertar(nombreTabla, True, nombreId, tuplaRectificada(args))
    def insertar_SinIdAutomatico(self,nombreTabla,*args):
        """
        (nombreTabla,valores una sola fila completa)
        (nombreTabla,[]columnas,valores)<br/>
        es nuestra responsabiladad asegurarnos de que almenos uno de los valores sea una llave
        :param nombreTabla:
        :param args:
        :return:
        """
        return self._insertar(nombreTabla, False, "", tuplaRectificada(args))
    def insertar(self,nombreTabla,*args):
        """
        (nombreTabla,valores una sola fila completa)
        (nombreTabla,[]columnas,valores)<br/>
        si no lo tiene pone el id de forma automatica
        :param nombreTabla:
        :param args:
        :return:
        """
        return self._insertar(nombreTabla,True,"id",*args)
    def _insertar(self,nombreTabla,idAutomatico,nombreId,*args):
        """
        (nombreTabla,valores una sola fila completa)
        (nombreTabla,[]columnas,valores)
        :param nombreTabla:
        :param args:
        :return:
        """
        #cada []leng comienza la sigiente fila
        sql=""
        sqlColumnas=""
        a=tuplaRectificada(args)
        leng=len(a)
        listaColumnas=None
        inicioDeValores=0
        if leng>0:
            if esLista(a[0]):
                listaColumnas=a[0]
                leng2=len(listaColumnas)
                for i in range(leng2):
                    if i!=0:
                        sqlColumnas+=" , "
                    sqlColumnas+=listaColumnas[i]
                inicioDeValores=1
            for i in range(inicioDeValores,leng):
                if i!=inicioDeValores:
                    sql+=" , "
                if str(a[i]).startswith("b'") and str(a[i]).endswith("'"):
                    sql += a[i]
                else:
                    if esInt(a[i]):
                        sql += str(a[i]) + " "
                    else:
                        sql+=" '"+str(a[i])+"' "
        if idAutomatico:
            if isEmpty(nombreId):
                nombreId="id"
            #sql="("+getIdCorrespondiente(nombreTabla,nombreId)+") , "+sql
            sql = " NULL , " + sql
            if not isEmpty(sqlColumnas):
                sqlColumnas=nombreId+" , "+sqlColumnas

        if not isEmpty(sqlColumnas):
            sql= SQLs.INSERT_INTO+" "+nombreTabla+" ( "+sqlColumnas+" ) "+SQLs.VALUES+" ( "+sql+" ) "
        else:
            sql=SQLs.INSERT_INTO+" "+nombreTabla+" "+SQLs.VALUES+" ( "+sql+" ) "
        return sql
    def insertar_Many_SinIdAutomatico(self,nombreTabla,cantidadDeColumnas):
        return self.__insertar_Many(nombreTabla, False, "", cantidadDeColumnas)
    def insertar_Many_idAutomatico(self,nombreTabla,id,cantidadDeColumnas):
        return self.__insertar_Many(nombreTabla,True,id,cantidadDeColumnas)
    def insertar_Many(self,nombreTabla,cantidadDeColumnas):
        return self.__insertar_Many(nombreTabla,True,"id",cantidadDeColumnas)
    def __insertar_Many(self,nombreTabla,idAutomatico,nombreId,cantidadDeColumnas):
        sql =""
        for i in range(cantidadDeColumnas):
            if i!=0:
                sql+=" , "
            sql+="?"
        if idAutomatico:
            #if isEmpty(nombreId):
             #   nombreId="id"
            #sql="("+getIdCorrespondiente(nombreTabla,nombreId)+") , "+sql
            sql = " NULL , " + sql
        return SQLs.INSERT_INTO + " " + nombreTabla + " " + SQLs.VALUES + " ( " + sql + " ) "

    def crearTabla(self,nombreTabla,*nombre_tipos):
        """
        (nombre,.. nombreColumna,TipoDeDatoSQL,capacidad#,isKeyPrimary o tipoDeClasificacionSQL)<br/>
     *  (nombre,.. nombreColumna,TipoDeDatoSQL,capacidad#)<br/> asumo que no es llave primaria
        (nombre,.. nombreColumna,capacidad#) asumo que es VARCHAR <br/>
        (nombre,.. nombreColumna) asumo que es VARCHAR(255)<br/>
        si el siguiente a nombreColumna no es un TipoDeDatoSQL asumo que es VARCHAR(255) <br/>
        si el siguiente a TipoDeDatoSQL no es un # asumo que es VARCHAR(255)  <br/>
        :param NombreTabla:
        :param nombre_tipos:
        :return:
        """

        a=tuplaRectificada(nombre_tipos)
        leng=len(a)

        #if leng>0 and nombre_tipos[0]=='valor1':
            #println("tipos=",a)
        sql=""
        tipoAnterior=None
        pos=0
        tieneClavePrimaria=False
        for i in a:
            pos=pos%4

            if pos==3:
                if esBool(i):
                    if i:

                        #sql += strg(" ", NOT_NULL," ", PRIMARY_KEY)
                        sql += strg(" ", SQLs.NOT_NULL, " ", SQLs.PRIMARY_KEY)
                        tieneClavePrimaria=True
                elif TipoDeClasificacionSQL.esTipoDeClasificacionSQl(i):
                    sql += strg(" ", i.getValor())
                    if TipoDeClasificacionSQL.esLlave(i):
                        tieneClavePrimaria = True

                else:
                    pos=0
                sql+=" , "
                tipoAnterior=None

            if pos==2:
                if esInt(i):
                    sql+=strg("(",i,")")
                else:
                    if tipoAnterior==TipoDeDatoSQL.VARCHAR:
                        sql += strg("(255)")
                    if esBool(i):
                        if i:
                            sql += strg(" ", SQLs.PRIMARY_KEY)
                            tieneClavePrimaria = True
                        sql += " , "
                        pos = 0
                        tipoAnterior = None
                        continue
                    elif TipoDeClasificacionSQL.esTipoDeClasificacionSQl(i):
                        sql += strg(" ", i.getValor())
                        if TipoDeClasificacionSQL.esLlave(i):
                            tieneClavePrimaria = True
                        sql += " , "
                        pos = 0
                        tipoAnterior = None
                        continue
                    else:
                        pos=0
                        sql += " , "



            if pos==1:
                tipo = None
                if TipoDeDatoSQL.esTipoDeDatoSQL(i):
                    tipo=i
                if tipo!=None:
                    sql += strg(" ",i.getValor())
                    tipoAnterior=tipo

                elif esInt(i):
                    #println("i=",i)
                    tipo=TipoDeDatoSQL.VARCHAR
                    sql += strg(" ", tipo.getValor(),"(",i,")")
                    tipoAnterior=tipo
                    pos=3
                    continue
                else:
                    tipo = TipoDeDatoSQL.VARCHAR
                    sql +=strg(" ",tipo.getValor(),"(255)")
                    tipoAnterior = tipo
                    if esBool(i):
                        if i:
                            sql += strg(" ", SQLs.PRIMARY_KEY)
                            tieneClavePrimaria = True
                        sql += " , "
                        pos = 0
                        tipoAnterior = None
                        continue
                    elif TipoDeClasificacionSQL.esTipoDeClasificacionSQl(i):
                        sql += strg(" ", i.getValor())
                        if TipoDeClasificacionSQL.esLlave(i):
                            tieneClavePrimaria = True
                        sql += " , "
                        pos = 0
                        tipoAnterior = None
                        continue
                    else:
                        pos=0
                        sql += " , "

            if pos==0:
                #print("pos 0")
                sql += strg(" ",i)
            pos+=1


        if pos == 1:
            tipo = TipoDeDatoSQL.VARCHAR
            sql += strg(" ", tipo.getValor(), "(255) ")


        elif pos==2:
            if tipoAnterior==TipoDeDatoSQL.VARCHAR:
                sql += strg("(255)")
        if endsWithOR(sql,", ",","):
            sql=sql[:sql.rfind(",")]

        if (not tieneClavePrimaria) and (not contiene(sql," id ")):
            add=""
            if not isEmpty(sql.strip()):
                add=" , "

            sql = " id " + TipoDeDatoSQL.INTEGER.getValor() + " " + SQLs.PRIMARY_KEY+" "+SQLs.AUTOINCREMENT +add+sql
            #sql = " id "  + SERIAL +" " + PRIMARY_KEY +  add + sql

        return SQLs.CREATE_TABLE+" "+nombreTabla+" ( "+sql+" ) "

class SQLs_Postgres(SQLs):
    def _insertar(self, nombreTabla, idAutomatico, nombreId, *args):
        """
        (nombreTabla,valores una sola fila completa)
        (nombreTabla,[]columnas,valores)
        :param nombreTabla:
        :param args:
        :return:
        """
        # cada []leng comienza la sigiente fila
        sql = ""
        sqlColumnas = ""
        a = tuplaRectificada(args)
        leng = len(a)
        listaColumnas = None
        inicioDeValores = 0
        if leng > 0:
            if esLista(a[0]):
                listaColumnas = a[0]
                leng2 = len(listaColumnas)
                for i in range(leng2):
                    if i != 0:
                        sqlColumnas += " , "
                    sqlColumnas += listaColumnas[i]
                inicioDeValores = 1
            for i in range(inicioDeValores, leng):
                if i != inicioDeValores:
                    sql += " , "
                if str(a[i]).startswith("b'") and str(a[i]).endswith("'"):
                    sql += a[i]
                else:
                    if esInt(a[i]):
                        sql += str(a[i]) + " "
                    else:
                        sql += " '" + str(a[i]) + "' "
        # if idAutomatico:
        #     if isEmpty(nombreId):
        #         nombreId = "id"
        #     # sql="("+getIdCorrespondiente(nombreTabla,nombreId)+") , "+sql
        #     sql = " NULL , " + sql
        #     if not isEmpty(sqlColumnas):
        #         sqlColumnas = nombreId + " , " + sqlColumnas

        if not isEmpty(sqlColumnas):
            sql = SQLs.INSERT_INTO + " " + nombreTabla + " ( " + sqlColumnas + " ) " + SQLs.VALUES + " ( " + sql + " ) "
        else:
            sql = SQLs.INSERT_INTO + " " + nombreTabla + " " + SQLs.VALUES + " ( " + sql + " ) "
        return sql

    def crearTabla(self, nombreTabla, *nombre_tipos):
        """
        (nombre,.. nombreColumna,TipoDeDatoSQL,capacidad#,isKeyPrimary o tipoDeClasificacionSQL)<br/>
     *  (nombre,.. nombreColumna,TipoDeDatoSQL,capacidad#)<br/> asumo que no es llave primaria
        (nombre,.. nombreColumna,capacidad#) asumo que es VARCHAR <br/>
        (nombre,.. nombreColumna) asumo que es VARCHAR(255)<br/>
        si el siguiente a nombreColumna no es un TipoDeDatoSQL asumo que es VARCHAR(255) <br/>
        si el siguiente a TipoDeDatoSQL no es un # asumo que es VARCHAR(255)  <br/>
        :param NombreTabla:
        :param nombre_tipos:
        :return:
        """

        a = tuplaRectificada(nombre_tipos)
        leng = len(a)

        # if leng>0 and nombre_tipos[0]=='valor1':
        # println("tipos=",a)
        sql = ""
        tipoAnterior = None
        pos = 0
        tieneClavePrimaria = False
        for i in a:
            pos = pos % 4

            if pos == 3:
                if esBool(i):
                    if i:
                        # sql += strg(" ", NOT_NULL," ", PRIMARY_KEY)
                        sql += strg(" ", SQLs.NOT_NULL, " ", SQLs.PRIMARY_KEY)
                        tieneClavePrimaria = True
                elif TipoDeClasificacionSQL.esTipoDeClasificacionSQl(i):
                    sql += strg(" ", i.getValor())
                    if TipoDeClasificacionSQL.esLlave(i):
                        tieneClavePrimaria = True

                else:
                    pos = 0
                sql += " , "
                tipoAnterior = None

            if pos == 2:
                if esInt(i):
                    sql += strg("(", i, ")")
                else:
                    if tipoAnterior == TipoDeDatoSQL.VARCHAR:
                        sql += strg("(255)")
                    if esBool(i):
                        if i:
                            sql += strg(" ", SQLs.PRIMARY_KEY)
                            tieneClavePrimaria = True
                        sql += " , "
                        pos = 0
                        tipoAnterior = None
                        continue
                    elif TipoDeClasificacionSQL.esTipoDeClasificacionSQl(i):
                        sql += strg(" ", i.getValor())
                        if TipoDeClasificacionSQL.esLlave(i):
                            tieneClavePrimaria = True
                        sql += " , "
                        pos = 0
                        tipoAnterior = None
                        continue
                    else:
                        pos = 0
                        sql += " , "

            if pos == 1:
                tipo = None
                if TipoDeDatoSQL.esTipoDeDatoSQL(i):
                    tipo = i
                if tipo != None:
                    sql += strg(" ", i.getValor())
                    tipoAnterior = tipo

                elif esInt(i):
                    # println("i=",i)
                    tipo = TipoDeDatoSQL.VARCHAR
                    sql += strg(" ", tipo.getValor(), "(", i, ")")
                    tipoAnterior = tipo
                    pos = 3
                    continue
                else:
                    tipo = TipoDeDatoSQL.VARCHAR
                    sql += strg(" ", tipo.getValor(), "(255)")
                    tipoAnterior = tipo
                    if esBool(i):
                        if i:
                            sql += strg(" ", SQLs.PRIMARY_KEY)
                            tieneClavePrimaria = True
                        sql += " , "
                        pos = 0
                        tipoAnterior = None
                        continue
                    elif TipoDeClasificacionSQL.esTipoDeClasificacionSQl(i):
                        sql += strg(" ", i.getValor())
                        if TipoDeClasificacionSQL.esLlave(i):
                            tieneClavePrimaria = True
                        sql += " , "
                        pos = 0
                        tipoAnterior = None
                        continue
                    else:
                        pos = 0
                        sql += " , "

            if pos == 0:
                # print("pos 0")
                sql += strg(" ", i)
            pos += 1

        if pos == 1:
            tipo = TipoDeDatoSQL.VARCHAR
            sql += strg(" ", tipo.getValor(), "(255) ")


        elif pos == 2:
            if tipoAnterior == TipoDeDatoSQL.VARCHAR:
                sql += strg("(255)")
        if endsWithOR(sql, ", ", ","):
            sql = sql[:sql.rfind(",")]

        if (not tieneClavePrimaria) and (not contiene(sql, " id ")):
            add = ""
            if not isEmpty(sql.strip()):
                add = " , "

            #sql = " id " + TipoDeDatoSQL.INTEGER.getValor() + " " + SQLs.PRIMARY_KEY + " " + SQLs.AUTOINCREMENT + add + sql
            sql = " id "  + TipoDeDatoSQL.SERIAL.getValor() +" " + SQLs.PRIMARY_KEY +  add + sql

        return SQLs.CREATE_TABLE + " " + nombreTabla + " ( " + sql + " ) "



