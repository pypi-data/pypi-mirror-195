from RenePy.ClasesUtiles.Tipos.TipoDeImagen import TipoDeImagen
from RenePy.MetodosUtiles.Archivo import getExtencion
from RenePy.ClasesUtiles.File import File

def getTipoDeImagen(f):
    extencion = getExtencion(f)
    return TipoDeImagen.get(extencion)
def esImagen(f):
    return getTipoDeImagen(f) is not None
