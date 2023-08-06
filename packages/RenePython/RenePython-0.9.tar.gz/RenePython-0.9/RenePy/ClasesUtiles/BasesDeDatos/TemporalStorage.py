from RenePy.ClasesUtiles.File import File,FileTemp
from RenePy.ClasesUtiles.BasesDeDatos import BDConexion

from RenePy.ClasesUtiles.Tipos.TipoDeDatoSQL import TipoDeDatoSQL
from RenePy.MetodosUtiles.Imports.MetodosUtilesBasicos import *
class _DatosDeColumna():
    def __init__(self,nombre,tipo,value):
        self.nombre=nombre
        self.tipo=tipo
        self.value=value
_DIR_TEMP_TEMPORAL_STORAGE="LeyenApp/PythonApps/BDs/TemporalStorage"
_TIPO_LISTA="lista"
_TIPO_TUPLA="tupla"

class TemporalStorage():
    def __init__(self,nombre,direccion=None):
        self._nombre=nombre
        self._nombreTablaTipos=str(nombre)+"Tipos"
        self._nombreTablaLugaresDeTipoLista=self._nombreTablaTipos+"DireccionesTipoLista"

        #self._nombreTablaNombres = str(nombre) + "Nombres"
        self._columnas=[]

        if direccion==None:
            direccion = FileTemp(_DIR_TEMP_TEMPORAL_STORAGE).mkdirs()

        elif File.esFile(direccion):
            direccion.mkdirs()
            #direccion=dirTemp.append(nombre+".sqlite")
        self._direccion=direccion.append("BDTemporalStorage.sqlite")
        self._conet=BDConexion.new_BDConexionSQLite(self._direccion)\
            .crearTablaSiNoExiste(self._nombre).crearTablaSiNoExiste(self._nombreTablaTipos).crearTablaSiNoExiste(self._nombreTablaLugaresDeTipoLista, "nombreTabla", "nombrePropiedad","tipo")
        #self._conet.crearTablaYBorrarSiExiste(self._nombreTablaLugaresDeTipoLista, "nombreTabla", "nombrePropiedad","tipo")

        self._leerDatosDeBD()
    def _leerDatosDeBD(self):
        self._columnas = []
        datos=self._conet.select_Todo(self._nombre)
        #println("datos=",datos)
        datosTipos=self._conet.select_Todo(self._nombreTablaTipos)
        #println("datosTipos=",datosTipos)
        for i in range(len(datos)):
            #println("i=", i)
            #self._columnas.append(_DatosDeColumna(datosTipos[1][j], datosTipos[0][j], datos[j]))
            valores=datos[i]
            #println("valores=",valores)
            for j in range(1,len(valores)):
                #println("j=",j," datos[i][j]=",datos[i][j])
                self._columnas.append(_DatosDeColumna(datosTipos[1][j],TipoDeDatoSQL.get(datosTipos[0][j]),datos[i][j]))
        datosNombreTablasListas=self._conet.select_Todo(self._nombreTablaLugaresDeTipoLista)
        for i in range(len(datosNombreTablasListas)):
            datosTabla=datosNombreTablasListas[i]
            #println("datosTabla=",datosTabla)
            datos=self._conet.select_Todo(datosTabla[1])
            valores=[]
            for j in datos:
                valores.append(j[1])
            if datosTabla[3]==_TIPO_TUPLA:
                valores=tuple(valores)
            self._columnas.append(_DatosDeColumna(datosTabla[2], datosTabla[3], valores))
    def _addColumnaDeSerNecesario(self,nombre,value):
        tipo = TipoDeDatoSQL.getTipoDeDatoSQL(value)
        if tipo == None:
            if esLista(value):
                tipo = _TIPO_LISTA
            elif esTupla(value):
                tipo = _TIPO_TUPLA

        if tipo != None:

            existe=False
            indice=len(self._columnas)
            for i in range(indice):
                if self._columnas[i].nombre==nombre:
                    indice=i
                    existe=True
                    break
            if not existe:
                self._columnas.append(_DatosDeColumna(nombre,tipo,value))
            else:
                self._columnas[indice].value=value
                self._columnas[indice].tipo = tipo


            #self._updateTabla()
    def _updateTabla(self):
        sql=[]
        insert=[]
        sqlTipos=[]
        insertTipos=[]
        insertNombres=[]

        indicesListasYTuplas=[]
        indice=0
        for i in self._columnas:
            #println("i.tipo=",i.tipo)
            if Or(i.tipo,_TIPO_TUPLA,_TIPO_LISTA):
                indicesListasYTuplas.append(indice)
                indice += 1
                continue
            sql.append(i.nombre)
            sql.append(i.tipo)
            insert.append(i.value)
            sqlTipos.append(i.nombre)
            sqlTipos.append(TipoDeDatoSQL.VARCHAR)
            if TipoDeDatoSQL.esTipoDeDatoSQL(i.tipo):
                insertTipos.append(i.tipo.getValor())
            else:
                insertTipos.append("None")
            insertNombres.append(i.nombre)
            indice += 1
        self._conet.crearTablaYBorrarSiExiste(self._nombre,*tuple(sql))
        if not isEmpty(insert):
            self._conet.insertar(self._nombre,*tuple(insert))
        self._conet.crearTablaYBorrarSiExiste(self._nombreTablaTipos, *tuple(sqlTipos))
        if not isEmpty(insert):
            self._conet.insertar(self._nombreTablaTipos,*tuple(insertTipos)).insertar(self._nombreTablaTipos,*tuple(insertNombres))


        self._conet.crearTablaYBorrarSiExiste(self._nombreTablaLugaresDeTipoLista, "nombreTabla","nombrePropiedad","tipo")

        for i in indicesListasYTuplas:
            col=self._columnas[i]
            nombreTabla = str(self._nombre) + str(col.nombre) + "TablaList"
            self._conet.insertar(self._nombreTablaLugaresDeTipoLista, nombreTabla, col.nombre, col.tipo)

            tipo=TipoDeDatoSQL.VARCHAR
            if not isEmpty(col.value):
                tipo=TipoDeDatoSQL.getTipoDeDatoSQL(col.value[0])
                if tipo==None:
                    tipo=TipoDeDatoSQL.VARCHAR
            #insert = []
            self._conet.crearTablaYBorrarSiExiste(nombreTabla, "valor", tipo)
            for j in col.value:
                self._conet.insertar(nombreTabla, j)
                #insert.append(j)
            #self._conet.insertar(nombreTabla,*tuple(insert))




    def put(self,*paresNombre_Value):
        #println("paresNombre_Value=",paresNombre_Value)
        #println("leng=",len(paresNombre_Value))
        if len(paresNombre_Value)%2==0:
            nombre=None
            pos=0
            for i in paresNombre_Value:
                if pos==0:
                    nombre=i
                elif pos==1:
                    self._addColumnaDeSerNecesario(nombre, i)
                pos=(pos+1)%2
        self._updateTabla()
    def get(self,nombre,valorDefault=None):
        for i in self._columnas:
            if i.nombre==nombre:
                return i.value
        if valorDefault!=None:
            self.put(nombre,valorDefault)
        return valorDefault
    def getValues(self):
        res=[]
        for i in self._columnas:
            res.append(i.value)
        return tuple(res)
    def getNombresColumnas(self):
        res = []
        for i in self._columnas:
            res.append(i.nombre)
        return tuple(res)
    def clear(self):
        self._conet.crearTablaYBorrarSiExiste(self._nombre).crearTablaYBorrarSiExiste(self._nombreTablaTipos).crearTablaYBorrarSiExiste(self._nombreTablaLugaresDeTipoLista, "nombreTabla","nombrePropiedad","tipo")
        self._columnas.clear()


#tem=TemporalStorage("prebaTem")
#tem.clear()
#tem.put("unalista",["a","b","c"])
#var=tem.get("unalista")
#print(var)
#tem.put("unaTupla",(1,2,3))
#var=tem.get("unaTupla")
#print(var)
#tem.put("valor1","uno3")
#tem.put("valor2","dos2")
#var=tem.get("valor1")
#print(var)
#var=tem.get("valor2")
#tem.put("valor3",5,"valor4",False,"valor5",6.4)

#print(var)


    #@staticmethod
    #def _crearDirBDDeSerNecesario():
        #FileTemp(_DIR_TEMP_TEMPORAL_STORAGE).mkdirs()



