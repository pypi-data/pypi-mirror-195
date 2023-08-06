import uuid
import random
from RenePy.MetodosUtiles.MetodosUtiles import esLista,esTupla

def getRandomStr_DeHostYDate():
    return str(uuid.uuid1())

def getRandomStr():
    return str(uuid.uuid4())

def getBoolRandom(unoDe=2):
    if unoDe==2 or unoDe<2:
        return bool(random.getrandbits(1))
    return getIntRandom(unoDe)==0

def getIntRandom(*a):
    """
    (i)

    (i0,i)

    (i0,i,salto#)
    :param a:
    :return:
    """
    a = tuple([int(i) for i in a])
    if len(a)>=2 and a[0]==a[1]:
        return a[0]

    return random.randrange(*a)


def getRandom(*a):
    leng=len(a)
    if leng>1:
        return random.choice(list(a))
    if leng==1:
        e=a[0]
        if esLista(e) or esTupla(e):
            return getRandom(*tuple(e))
        return e
    return None