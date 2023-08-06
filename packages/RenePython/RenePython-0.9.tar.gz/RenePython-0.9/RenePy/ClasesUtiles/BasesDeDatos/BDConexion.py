from RenePy.MetodosUtiles.Imports.MetodosUtilesBasicos import *
from RenePy.MetodosUtiles import BD_SQLite
from RenePy.ClasesUtiles.Tipos.TipoDeConexion import TipoDeConexion
from RenePy.MetodosUtiles import SQL
from RenePy.ClasesUtiles.File import File,FileTemp
from RenePy.MetodosUtiles import BD_Postgres
import os
class DatosDeConexion:
    def __init__(self):
        self.url=None
        self.url_BD=None#es la url con la que se puede establecer la conexion al servidor
        self.usuario=None
        self.contrasena=None
        self.servidor=None
        self.nombreBD=None
        self.puerto=None
        self.tipoDeConexion:TipoDeConexion=None

class BDConexion():
    def __init__(self,datosDeConexion:DatosDeConexion):#nombreBD,tipoDeConexion
        #self._nombreBD=str(nombreBD)
        #self._tipoDeConexion=tipoDeConexion
        self._ultimoSQL=None
        self.__mostrarResultadosEnConsola=False
        self.__mostrarExecutes=True
        self.datosDeConexion:DatosDeConexion=datosDeConexion
        self.sqlUtil=SQL.SQLs_Postgres() if self.datosDeConexion.tipoDeConexion==TipoDeConexion.POSTGRE_SQL else SQL.SQLs()
        #self._resultados=None

    def cl(self):
        self.__mostrarResultadosEnConsola = True
        return self
    def no_ex(self):
        self.__mostrarExecutes=False
        return self
    def drop_table_if_exist(self,nombreTabla):
        self._execute(self.sqlUtil.drop_table_if_exist(nombreTabla))
        return self
    def existe(self, nombreTabla, *paresColumnaValor):
        return self.getCantidad_Where(nombreTabla, *paresColumnaValor)>0
    def contiene(self, nombreTabla, *paresColumnaValor):
        return self.getCantidad_Where(nombreTabla,*paresColumnaValor)>0
    def isEmpty(self,nombreTabla,columna):
        cant=self.getCantidad(nombreTabla,columna)
        #println("cant=",cant)
        return cant==0
    def getCantidad_Where(self,nombreTabla,*paresColumnaValor):
        return self._execute(self.sqlUtil.getCantidad_Where(nombreTabla,*paresColumnaValor))
    def getCantidad(self,nombreTabla,columna):
        return self._execute(self.sqlUtil.getCantidad(nombreTabla,columna))
    def getCantidad_Where_Inner_Join(self,nombreTabla,columna,*arg):
        return self._execute(self.sqlUtil.getCantidad_Where_Inner_Join(nombreTabla,columna,*arg))
    def getValorMaximo(self,nombreTabla,columna):
        return self._execute(self.sqlUtil.getValorMaximo(nombreTabla,columna))
    def getValorMaximo_Where(self,nombreTabla,columna,*paresColumnaValor):
        return self._execute(self.sqlUtil.getValorMaximo_Where(nombreTabla,columna,*paresColumnaValor))
    def getValorMaximo_Where_Inner_Join(self,nombreTabla,columna,*arg):
        return self._execute(self.sqlUtil.getValorMaximo_Where_Inner_Join(nombreTabla,columna,*arg))
    def getSuma_Where_Inner_Join(self,nombreTabla,columna,*arg):
        return self._execute(self.sqlUtil.getSuma_Where_Inner_Join(nombreTabla,columna,*arg))
    def getSuma_Where(self,nombreTabla,columna,*arg):
        return self._execute(self.sqlUtil.getSuma_Where(nombreTabla,columna,*arg))

    def getLastId(self, nombreTabla):
        return self._execute(self.sqlUtil.getLastId(nombreTabla))

    def select_ConUltimoID(self, nombreTabla):
        O=self._execute(self.sqlUtil.select_ConUltimoID(nombreTabla))
        if O==None or len(O)==0:
            return None
        return O[0]

    def getUltimoSQL(self):
        return self._ultimoSQL
    def getNombreBD(self):
        return self.datosDeConexion.nombreBD#self._nombreBD
    def getTipoDeConexion(self):
        return self.datosDeConexion.tipoDeConexion#self._tipoDeConexion
    def crearTablaSiNoExiste(self,nombreTabla, *args):
        self._execute(self.sqlUtil.crearTablaSiNoExiste(nombreTabla, *args))
        return self
    def delete_id(self,nombreTabla,id):

        self._execute(self.sqlUtil.delete_id(nombreTabla, id))
        return self
    def delete(self,nombreTabla, *args):
        """
        (nombreTabla,,whereColumna1,whereValor1,whereColumna2,whereValor2,...)
        :param nombreTabla:
        :param args:
        :return:
        """
        self._execute(self.sqlUtil.delete(nombreTabla,  *args))
        return self
    def update(self,nombreTabla, paresColumnaValor, *args):
        """
        (nombreTabla,[columna,setValor1,columna2,setValor2,... ],whereColumna1,whereValor1,whereColumna2,whereValor2,...)
        :param nombreTabla:
        :param paresColumnaValor:
        :param args:
        :return:
        """
        #self._execute(self.sqlUtil.update(nombreTabla, paresColumnaValor, tuplaRectificada(args)))
        self._execute(self.sqlUtil.update(nombreTabla, paresColumnaValor, *args))
        return self
    def update_Id(self,nombreTabla, id, *args):
        """
        (nombreTabla,id#,columna,setValor1,columna2,setValor2,... )
        (nombreTabla,id#,[ [columna,valor] , [columna,valor] ... ])
        :param nombreTabla:
        :param id:
        :param args:
        :return:
        """
        if (not isEmpty(args)) and esLista(args[0]):
            a=[]
            for l in args[0]:
                a.append(l[0])
                a.append(l[1])
            args=tuple(a)



        self._execute(self.sqlUtil.update_Id(nombreTabla,id, *args))
        return self
    def select_Distinct_Where(self,nombreTabla, *args):
        return self._execute(self.sqlUtil.select_Distinct_Where(nombreTabla, tuplaRectificada(args)))
     #   self._resultados = self._execute(self.sqlUtil.select_Distinct_Where(nombreTabla, tuplaRectificada(args)))
      #  return self;

    def select_Distinct_Todo(self,nombreTabla):
        return self._execute(self.sqlUtil.select_Distinct_Todo(nombreTabla))
        #self._resultados = self._execute(self.sqlUtil.select_Distinct_Todo(nombreTabla))
        #return self;

    def select_Distinct(self,nombreTabla, *args):
        return self._execute(self.sqlUtil.select_Distinct(nombreTabla, tuplaRectificada(args)))
        #self._resultados = self._execute(self.sqlUtil.select_Distinct(nombreTabla, tuplaRectificada(args)))
        #return self;

    def select_Distinct_ORDER_BY(self,nombreTabla, *args):
        return self._execute(self.sqlUtil.select_Distinct_ORDER_BY(nombreTabla, tuplaRectificada(args)))
        #self._resultados = self._execute(self.sqlUtil.select_Distinct_ORDER_BY(nombreTabla, tuplaRectificada(args)))
        #return self;

    def select_Distinct_Where_ORDER_BY(self,nombreTabla, *args):
        return self._execute(self.sqlUtil.select_Distinct_Where_ORDER_BY(nombreTabla, tuplaRectificada(args)))
        #self._resultados = self._execute(self.sqlUtil.select_Distinct_Where_ORDER_BY(nombreTabla, tuplaRectificada(args)))
        #return self;

    def select_Where_ORDER_BY_firstRow(self, nombreTabla, *args):
        O=self.select_Where_ORDER_BY(nombreTabla,*args)
        if O != None and len(O) > 0:
            return O[0]
        return None
    def select_Where_ORDER_BY(self,nombreTabla, *args):
        """
        (nombreTabla,columnas[],where[pares .. Columna-Valor],columnas por los que ordenar,o+ ordenamiento)
        (nombreTabla,where[pares .. Columna-Valor],columnas por los que ordenar,o+ ordenamiento)
        :param nombreTabla:
        :param args:
        :return:
        """
        return self._execute(self.sqlUtil.select_Where_ORDER_BY(nombreTabla, *args))
        #self._resultados = self._execute(self.sqlUtil.select_Where_ORDER_BY(nombreTabla, tuplaRectificada(args)))
        #return self;
    def select_ORDER_BY(self,nombreTabla, *args):
        return self._execute(self.sqlUtil.select_ORDER_BY(nombreTabla, *args))
        #self._resultados = self._execute(self.sqlUtil.select_ORDER_BY(nombreTabla, tuplaRectificada(args)))
        #return self;

    def select_Where_FirstRow(self, nombreTabla, *args):
        O=self.select_Where(nombreTabla,*args)
        if O!=None and len(O)>0:
            return O[0]
        return None
    def select_Where_LastRow(self, nombreTabla, *args):
        O=self.select_Where(nombreTabla,*args)
        leng=len(O)
        if O!=None and leng>0:
            return O[leng-1]
        return None
    def select_FirstRow_Where_ValorMaximo(self, nombreTabla,columnaValorMaximo,*paresColumnaValor):
        O = self._execute(self.sqlUtil.select_Where_ValorMaximo(nombreTabla, columnaValorMaximo, *paresColumnaValor))
        if O!=None and len(O)>0:
            return O[0]
        return None
    def select_Where_Inner_Join_FirstRow(self, nombreTabla, *args):#_Todo
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
        O = self.select_Where_Inner_Join(nombreTabla, *args)#_Todo
        if O != None and len(O) > 0:
            return O[0]
        return None
    def select_ID_Where(self, nombreTabla, *paresColumnaValor):
        return self.select_Where_FirstResult(nombreTabla,"id",*paresColumnaValor)

    def select_Where(self,nombreTabla, *args):
        """
            (nombreTabla,columnas[],pares .. Columna-Valor)
            (nombreTabla,pares .. Columna-Valor)
            :param nombreTabla:
            :param args:
            :return:
            """
        sql=self.sqlUtil.select_Where(nombreTabla, *args)
        return self._execute(sql)
    def select_Where_FirstResult(self,nombreTabla,columna, *args):
        """
            (nombreTabla,columnaASeleccionar,pares .. Columna-Valor)
            :param nombreTabla:
            :param args:
            :return:
            """
        args=list(args)
        args.insert(0,[columna])
        args=tuple(args)
        O=self.select_Where(nombreTabla,*args)
        #println(len(O))
        if len(O) > 0:
            return(O[0][0])
        return None

    def select_forID(self,nombreTabla, id):
        res=self._execute(self.sqlUtil.select_forID(nombreTabla, id))
        if not isEmpty(res):
            res=res[0]
        return res
    def select(self,nombreTabla, *args):
        return self._execute(self.sqlUtil.select(nombreTabla, *args))

    def select_Todo(self,nombreTabla):
        return self._execute(self.sqlUtil.select_Todo(nombreTabla))
    def select_Todo_Where_Inner_Join(self,nombreTabla,*args):
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
        return self._execute(self.sqlUtil.select_Todo_Where_Inner_Join(nombreTabla,*args))
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
        return self._execute(self.sqlUtil.select_Distinct_Todo_Where_Inner_Join(nombreTabla,*args))
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
        return self._execute(self.sqlUtil.select_Todo_Where_Inner_Join_ORDER_BY(nombreTabla,*args))
    def insertar_Many_SinIdAutomatico(self,nombreTabla, filas):
        leng = 0
        if esLista(filas) and (not isEmpty(filas)) and esTupla(filas[0]):
            leng = len(filas[0])
        self._execute(self.sqlUtil.insertar_Many_SinIdAutomatico(nombreTabla, leng), filas)
        return self;

    def insertar_Many_idAutomatico(self,nombreTabla, id, filas):
        leng = 0
        if esLista(filas) and (not isEmpty(filas)) and esTupla(filas[0]):
            leng = len(filas[0])
        self._execute(self.sqlUtil.insertar_Many_idAutomatico(nombreTabla,id, leng), filas)
        return self;

    def insertar_Many(self,nombreTabla, filas):
        leng=0
        if esLista(filas) and (not isEmpty(filas)) and esTupla(filas[0]):
            leng=len(filas[0])
        self._execute(self.sqlUtil.insertar_Many(nombreTabla,leng),filas)
        return self
    def insertar_ConIdAutomatico(self,nombreTabla, nombreId, *args):
        return self._execute(self.sqlUtil.insertar_ConIdAutomatico(nombreTabla, nombreId, *args))

    def insertar_SinIdAutomatico(self,nombreTabla, *args):
        return self._execute(self.sqlUtil.insertar_SinIdAutomatico(nombreTabla, *args))

    def insertar(self,nombreTabla,*args):
        return self._execute(self.sqlUtil.insertar(nombreTabla,*args))

    def crearTablaYBorrarSiExiste(self,NombreTabla,*nombre_tipos):
        self._execute(self.sqlUtil.drop_table_if_exist(NombreTabla))
        self._execute(self.sqlUtil.crearTabla(NombreTabla, *nombre_tipos) )
        return self
    def crearTabla(self,NombreTabla,*nombre_tipos):
        self._execute(self.sqlUtil.crearTabla(NombreTabla,tuplaRectificada(nombre_tipos)))
        #BD_SQLite.crearTabla(self.getNombreBD(),NombreTabla,tuplaRectificada(nombre_tipos))
        return self
    def _execute(self,sql:str,filas=None):
        sql=sql.replace("'None'"," NULL ")#.replace("True","true").replace("False","false")
        self._ultimoSQL=sql
        if self.__mostrarExecutes:
            println("execute=",sql)
        res=""
        dc:DatosDeConexion=self.datosDeConexion
        if self.getTipoDeConexion()==TipoDeConexion.SQLITE:
            #nombre=self.getNombreBD()
            res= BD_SQLite.execute(dc.url_BD,sql,filas,sqlUtil=self.sqlUtil)
        elif  self.getTipoDeConexion()==TipoDeConexion.POSTGRE_SQL:
            res=BD_Postgres.execute(
                sql=sql
                ,database=dc.nombreBD
                ,host=dc.servidor
                ,port=dc.puerto
                ,user=dc.usuario
                ,password=dc.contrasena
                , sqlUtil=self.sqlUtil
            )

        if(self.__mostrarResultadosEnConsola and self.sqlUtil.esSelect(sql)):
            println("resultado=",res)
        return res

#def new_BDConexionSQLite(direccion):
def getConexionSQL_LITE(direccion):
    #str(direccion) TipoDeConexion.SQLITE,
    dc=DatosDeConexion()
    dc.tipoDeConexion=TipoDeConexion.SQLITE
    dc.nombreBD=os.path.basename(direccion)
    dc.url=direccion
    dc.url_BD=dc.url
    return BDConexion(dc)
def getConexion_POSTGRES(database,host="localhost",port="5432", user="postgres", password="postgres"):
    dc = DatosDeConexion()
    dc.tipoDeConexion = TipoDeConexion.POSTGRE_SQL
    dc.nombreBD = database
    dc.contrasena=password
    dc.usuario=user
    dc.puerto=port
    dc.servidor=host
    return BDConexion(dc)

