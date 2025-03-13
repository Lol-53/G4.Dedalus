import GraficaDatos as g 

import sys
import importlib

modulo = "GraficaDatos"  # Reemplaza con el nombre de tu módulo
if modulo in sys.modules:
    importlib.reload(sys.modules[modulo])  # Recarga el módulo


df = g.cargarDatos("lab_iniciales")

print(g.cargarNombreColumnas(df))



#TEST GRAFICAS DISPERSION

success_GD = g.graficaDispersion(df,"Glucosa","pH")
print(f"Resultado prueba valida dispersion: {success_GD}")

success_GD = g.graficaDispersion(df,"Paco","Ana")
print(f"Resultado prueba invalida dispersion: {success_GD}")

#Traza del código:
# Index(['PacienteID', 'Glucosa', 'pH', 'Cetonas', 'Creatinina', 'Hemoglobina',
#        'Leucocitos', 'Sodio', 'Potasio', 'Urea', 'Amilasa'],
#       dtype='object')
# Resultado prueba valida: 0
# Resultado prueba invalida: -1


#TEST GRAFICAS HISTOGRAMAS

success_GD = g.graficaHistograma(df,"Glucosa")
print(f"Resultado prueba valida histograma: {success_GD}")

success_GD = g.graficaHistograma(df,"Paco")
print(f"Resultado prueba invalida histograma: {success_GD}")

#Traza del código:
# Resultado prueba valida histograma: 0
# Resultado prueba invalida histograma: -1


#TEST GRAFICA DE BARRAS

success_GD = g.graficaBarras(df,"Glucosa","pH")
print(f"Resultado prueba valida barras: {success_GD}")

success_GD = g.graficaBarras(df,"Paco","Ana")
print(f"Resultado prueba invalida barras: {success_GD}")

#Traza del código:
# Resultado prueba valida barras: 0
# Resultado prueba invalida barras: -1


#TEST GRAFICA BOXPLOT 
success_GD = g.graficaBoxplot(df, "Glucosa")
print(f"Resultado prueba válida boxplot: {success_GD}")

success_GD = g.graficaBoxplot(df, "Paco")
print(f"Resultado prueba inválida boxplot: {success_GD}")

#Traza del código:
# Resultado prueba válida boxplot: 0
# Resultado prueba inválida boxplot: -1

#TEST GRAFICA DIAGRAMA DE VIOLIN
success_GD = g.graficaViolin(df, "Glucosa")
print(f"Resultado prueba válida diagrama violín: {success_GD}")

success_GD = g.graficaViolin(df, "Paco")
print(f"Resultado prueba inválida diagrama violín: {success_GD}")

#Traza del código:
# Resultado prueba válida diagrama violín: 0
# Resultado prueba inválida diagrama violín: -1

#TEST MATRIZ DE CORRELACIÓN
success_GD = g.graficaCorrelacion(df)
print(f"Resultado prueba válida matriz correlacion: {success_GD}")

#Traza del código:
# Resultado prueba válida matriz correlacion: 0

#TEST MATRIZ DE TENDENCIA
success_GD = g.graficaCurvaTendencia(df, "Glucosa","pH")
print(f"Resultado prueba válida curvaTendencia: {success_GD}")

success_GD = g.graficaCurvaTendencia(df, "Paco", "Ana")
print(f"Resultado prueba inválida curvaTendencia: {success_GD}")

#Traza del código:
# Resultado prueba válida curvaTendencia: 0
# Resultado prueba inválida curvaTendencia: -1

