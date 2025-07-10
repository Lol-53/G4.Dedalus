import GraficaDatos as g 

import sys
import importlib

modulo = "GraficaDatos"  # Reemplaza con el nombre de tu módulo
if modulo in sys.modules:
    importlib.reload(sys.modules[modulo])  # Recarga el módulo


lista = g.generarGrafica("lab_iniciales","1","Glucosa",y="pH",graphics=["graficaHistograma","graficaCurvaTendencia"])


print(lista)
# #TEST GRAFICAS HISTOGRAMAS

# success_GD = g.graficaHistograma(df,"Glucosa")
# print(f"Resultado prueba valida histograma: {success_GD}")

