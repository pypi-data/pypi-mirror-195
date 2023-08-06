from RenePy.MetodosUtiles.Imports.MetodosUtilesBasicos import *
from datetime import datetime,date, timedelta
import time
#from calendar import
class Date():

    def __init__(self,*a,año=0 ,mes=0,dia=0 ,hora=0,minuto=0,segundos=0 ,microsegundos=0):
        self.set(*a,año=año,mes=mes,dia=dia,hora=hora,minuto=minuto,segundos=segundos,microsegundos=microsegundos)



    def set(self,*a,año=0 ,mes=0,dia=0 ,hora=0,minuto=0,segundos=0 ,microsegundos=0):
        self.__año = año
        self.__mes = mes  # 1
        self.__dia = dia  # 1
        self.__hora = hora
        self.__minuto = minuto
        self.__segundos = segundos
        self.__microsegundos = microsegundos
        if And(0, año, mes, dia, hora, minuto, segundos, microsegundos):

            leng = len(a)
            if leng==0:
                dat = datetime.now()
                self.__año = dat.year
                self.__mes = dat.month
                self.__dia = dat.day
                self.__hora = dat.hour
                self.__minuto = dat.minute
                self.__segundos = dat.second
                self.__microsegundos = dat.microsecond
            elif leng==1:
                if esDatetimepy(a[0]):
                    dat:datetime =a[0]
                    self.__año = dat.year
                    self.__mes = dat.month
                    self.__dia = dat.day
                    self.__hora = dat.hour
                    self.__minuto = dat.minute
                    self.__segundos = dat.second
                    self.__microsegundos =dat.microsecond
                elif esDatepy(a[0]):
                    dat = a[0]
                    self.__año = dat.year
                    self.__mes = dat.month
                    self.__dia = dat.day
                elif esTimepy(a[0]):
                    dat = a[0]
                    self.__hora = dat.hour
                    self.__minuto = dat.minute
                    self.__segundos = dat.second
                    self.__microsegundos = dat.microsecond
                elif esTimedelta(a[0]):
                    ti:timedelta=a[0]
                    tim=time.gmtime(ti.total_seconds())
                    año0=1970
                    mes0=1
                    dia0=1
                    self.__año=tim.tm_year-año0
                    self.__mes=tim.tm_mon-mes0
                    self.__dia=tim.tm_mday-dia0
                    self.__hora=tim.tm_hour
                    self.__minuto = tim.tm_min
                    self.__segundos = tim.tm_sec
                    self.__microsegundos=ti.microseconds

                elif esInt(a[0]):
                    self.__año = a[0]
                elif esString(a[0]):
                    #print("es="+a[0])
                    dat=datetime.strptime(a[0],"%Y-%m-%d %H:%M:%S.%f")
                    self.__año = dat.year
                    self.__mes = dat.month
                    self.__dia = dat.day
                    self.__hora = dat.hour
                    self.__minuto = dat.minute
                    self.__segundos = dat.second
                    self.__microsegundos = dat.microsecond

            elif leng>1:
                datos=[self.__año ,self.__mes,self.__dia ,self.__hora ,self.__minuto,self.__segundos ,self.__microsegundos ]
                for i in range(len(a)):
                    datos[i]=a[i]
                self.__año = datos[0]
                self.__mes = datos[1]
                self.__dia = datos[2]
                self.__hora = datos[3]
                self.__minuto = datos[4]
                self.__segundos = datos[5]
                self.__microsegundos = datos[6]
            #self._datepy = datetime(self._año, self._mes,self._dia,self._hora,self._minuto,self._segundos,self._microsegundos)
        self.__initDatetime()
        return self

    def getAño(self):
        return self.__año
        #return self._datepy.year
    def getMes(self):
        return self.__mes
        #return self._datepy.month
    def getDia(self):
        return self.__dia
        #return self._datepy.day
    def getHora(self):
        return self.__hora
        #return self._datepy.hour
    def getMinutos(self):
        return self.__minuto
        #return self._datepy.minute
    def getSegundos(self):
        return self.__segundos
        #return self._datepy.second
    def getMicroSegundos(self):
        return self.__microsegundos
        #return self._datepy.microsecond
    # def getDatepy(self):
    #     return self._datepy
    def __initDatetime(self):
        año = self.__año
        mes = self.__mes
        dia = self.__dia
        if Or(0,año,mes,dia):
            año+=1
            mes+=1
            dia+=1


        if año == 0:
            año = 1

        if mes == 0:
            mes = 1

        if dia == 0:
            dia = 1
        #print("dia:",dia)
        self.__datetime=datetime(año, mes,dia,self.__hora,self.__minuto,self.__segundos,self.__microsegundos)
    def getDatetime(self):
        #return self._datepy
        return self.__datetime
    def getDiaDeLaSemana(self):
        return self.getDatetime().weekday()
    def en_año_bisiesto(self):
        return (self.__año%4==0)and(self.__año%100!=0 or self.__año%400==0)
    def add(self,date=None,años=0,meses=0,dias=0,horas=0,minutos=0,segundos=0,microsegundos=0):
        delta = getTimeDelta(date=date, años=años, meses=meses, dias=dias, horas=horas
                                  , minutos=minutos, segundos=segundos, microsegundos=microsegundos)
        return Date(self.getDatetime() + delta)
    def sub(self,date=None,años=0,meses=0,dias=0,horas=0,minutos=0,segundos=0,microsegundos=0):


        if date==None:
            delta=getTimeDelta(date=date,años=años,meses=meses,dias=dias,horas=horas
                                    ,minutos=minutos,segundos=segundos,microsegundos=microsegundos)
            if self.getAño() == 0:
                return Date(getTimeDelta(date=self) - delta)
            else:
                return Date(self.getDatetime() - delta)

        else:
            if date.getAño()==0:
                if self.getAño()==0:
                    return Date(getTimeDelta(date=self)-getTimeDelta(date=date))
                else:
                    return Date(self.getDatetime()-getTimeDelta(date=date))
            if self.esPosteriorA(date):
                return Date(self.getDatetime()-date.getDatetime())
            else:
                return getDate0()




            #delta:timedelta=self.getDatetime()-date.getDatetime()


    def getCantidadDeDias(self):
        s=self.getCantidadDeSegundos()
        return s//86400
    def getCantidadDeHoras(self):
        s=self.getCantidadDeSegundos()
        return s//3600
    def getCantidadDeMinutos(self):
        s=self.getCantidadDeSegundos()
        return s//60
    def getCantidadDeSegundos(self):
        s=getTimeDelta(date=self).total_seconds()
        return s
    def mañana(self):
        return self.add(dias=1)
    def ayer(self):
        return self.sub(dias=1)
    def esAnteriorA(self,a):
        return self.getDatetime()<a.getDatetime()
    def esAnteriorA_enDia(self,a):
        return self.getDatetime().date() < a.getDatetime().date()
    def esPosteriorA(self,a):
        return self.getDatetime()>a.getDatetime()

    def esPosteriorA_enDia(self, a):
        return self.getDatetime().date() >a.getDatetime().date()

    """
    def esAnteriorOIgual(self,a):
        return self._datepy.__le__(Date._getDatepy(a))
    
    def esPosteriorOIgual(self,a):
        return self._datepy.__ge__(Date._getDatepy(a))
    def esIgual(self,a):
        return self._datepy.__eq__(Date._getDatepy(a))
    
    def aumentar(self,*a):
        if (not isEmpty(a)):
            if (not Date.esDate(a[0])) and (not esDatepy(a)) and (not esDatetimepy(a)) and (not esTimepy(a)):
                a=[Date(*a)]
            a=a[0]
            c=Date._getDatepy(a)
            println("c=",c)
            b=self._datepy.__add__(c)
            println("b=", b)
            self.set(b)

        return self
    def restar(self,*a):
        if (not isEmpty(a)):
            if (not Date.esDate(a[0])) and (not esDatepy(a)) and (not esDatetimepy(a)) and (not esTimepy(a)):
                a=[Date(*a)]
            a=a[0]
            self.set(self._datepy.__sub__(Date._getDatepy(a)))
        return self
    def getAumentado(self,*a):
        return Date(self).aumentar(*a)
    def getRestado(self,*a):
        return Date(self).restar(*a)
    """
    def __str__(self):
        return str(self.getDatetime())
    def strTime(self):
        return "%04d-%02d-%02d %02d:%02d:%02d.%06d"%(self.__año,self.__mes,self.__dia
                                                     ,self.__hora,self.__minuto,self.__segundos,self.__microsegundos)

    @staticmethod
    def esDate(a):
        return isinstance(a,Date)
    # def getDatepy(a):
    #     if Date.esDate(a):
    #         return a.getDatepy()
    #     return a

def toDate(*args):
    if len(args)==0 or args[0]==None:
        return None
    elif args[0]=='None':
        return None
    else:
        return Date(*args)

def getTimeDelta(date=None,años=0,meses=0,dias=0,horas=0,minutos=0,segundos=0,microsegundos=0):
    if date!=None:
        años=date.getAño()
        meses=date.getMes()
        dias=date.getDia()
        horas=date.getHora()
        minutos=date.getMinutos()
        segundos=date.getSegundos()
        microsegundos=date.getMicroSegundos()
    delta=timedelta(days=((años*365)+(meses*30)+dias),hours=horas,minutes=minutos,seconds=segundos,microseconds=microsegundos)

    return delta

def getDate0():
    return Date(timedelta())



#var=Date().set(2000,10,12).getDiaDeLaSemana()
#print(var)
