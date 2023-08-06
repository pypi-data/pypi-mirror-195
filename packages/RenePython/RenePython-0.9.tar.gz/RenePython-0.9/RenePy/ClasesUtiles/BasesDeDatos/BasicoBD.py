from RenePy.Utiles import *
import re
class BasicoBD:
    PATRON_TIMES=re.compile("(\d\d)[:](\d\d)[:](\d\d)")
    def toBool(self,a):
        return toBool(a)
    def toBlob(self,a):
        return SQL.toBlob(a)
    def toDate(self,a):
        return toDate(a)
    def toInt(self,a):
        return toInt(a)
    def toPoint(self,a):
        return None
    def toFloat(self,a):
        return toFloat(a)
    def toTime(self,a):
        find=re.findall(BasicoBD.PATRON_TIMES,a)
        if len(find)>0:
            return Date(hora=toInt(find[0][0]),minuto=toInt(find[0][1]),segundos=toInt(find[0][2]))
        return None