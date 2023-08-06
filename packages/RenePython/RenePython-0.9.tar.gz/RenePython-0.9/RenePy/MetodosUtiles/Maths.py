import re
#from re import Pattern
from typing import TYPE_CHECKING, Dict, List, NoReturn, Optional, Union, Tuple, cast, ClassVar

def getMath_Str(patron:str):
    return getMath(re.compile(patron))
def getMath(patron,texto):
    l=re.findall(patron,texto)
    if len(l)>0:
        return l[0]
    return None
def hayMath(patron,texto):
    return re.match(patron,texto) is not None
