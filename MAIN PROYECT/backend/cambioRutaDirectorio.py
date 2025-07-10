import shutil


def cambioRuta(origen_directorio: str, destino_directorio: str):
    shutil.move(origen_directorio,destino_directorio)
