#FUNCIONES QUE HAY QUE HACER 

# Gráficas de dispersión: Relación entre dos variables importantes. X (falta test) -
# Histogramas: Distribución de los datos (p. ej., glucosa, creatinina). X (falta test) -
# Boxplots: Dispersión y valores atípicos. X (falta test) -
# Gráficas de barras: Comparación entre grupos o condiciones. X (falta test) -
# Matriz de correlación (Heatmap): Relación entre múltiples variables. X (falta test) -
# Curvas de tendencia: Evolución de datos a lo largo del tiempo. X(M)(falta test) -
# Diagramas de violín: Comparación de distribuciones y dispersión de los datos. X(M)(falta test) -
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Funciones de gráficas

def grafica(datos):
    
    return None

def graficaCorrelacion(df):
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10,8))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Mapa de Calor de Correlación")
    plt.savefig("matrizCorrelacion.png")

    limpiar()
    return 0

def graficaDispersion(df,x,y):
    if verificarNombreColumnas(df,[x,y]) == True:
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(8,5))
        ax = sns.scatterplot(x=df[x], y=df[y])
        plt.title("Relación entre " + x + " y " + y)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.savefig("graficaDispersion.png")

        limpiar()
        return 0
    else:
        return -1

def graficaHistograma(df, y, bins=10):
    if verificarNombreColumnas(df,[y]) == True: 
        sns.set_theme(style="whitegrid")
        if bins == None:
            bins = 10
        ax = sns.histplot(df[y], kde=True, bins=bins)
        plt.title("Histograma " + y)
        plt.xlabel(y)
        plt.ylabel("Frecuencia")
        plt.savefig("histograma.png")

        limpiar()
        return 0
    else:
        return -1    

def graficaBarras(df,x,y):
    if verificarNombreColumnas(df,[x,y]) == True:
        sns.set_theme(style="whitegrid")
        ax = sns.barplot(x=df[x], y=df[y], data=df)
        plt.title("Gráfica de barras")
        plt.savefig("graficaBarras.png")

        limpiar()
        return 0
    else:
        return -1

def graficaBoxplot(df,x):
    if verificarNombreColumnas(df,[x]) == True:
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(8,5))
        ax = sns.boxplot(y=df[x]) 
        plt.title("Boxplot de " + x)
        plt.xlabel(x)
        plt.savefig("boxplot.png")

        limpiar()
        return 0
    else:
        return -1


def graficaViolin(df, x):
    if verificarNombreColumnas(df,[x]) == True:
        sns.set_theme(style="whitegrid")
        sns.violinplot(x=df[x])
        plt.title("diagramaViolin")
        plt.savefig("diagramaViolin.png")

        limpiar()
        return 0
    else:
        return -1
    
def graficaCurvaTendencia(df,x,y):
    if verificarNombreColumnas(df,[x,y]) == True:
        sns.set_theme(style="whitegrid")
        sns.regplot(data=df, x=x, y=y, order=2)
        plt.title("curvaTendencia")
        plt.savefig("curvaTendencia.png")

        limpiar()
        return 0
    else:
        return -1

# Actualizar las gráficas
def limpiar ():
    plt.clf()   # Limpia la figura actual
    plt.close() # Cierra la figura para evitar acumulación

# Devuelve los nombres de las columnas del dataframe
def cargarNombreColumnas(df):
    return df.columns


#Verifica que los nombres de columnas pasados por parámetro existan en el dataframe
#Devuelve True si el nombre pasado no existe dentro del conjunto de nombres de columnas
def verificarNombreColumnas(df,columnas):
    for x in columnas:
        if x not in cargarNombreColumnas(df):
            return False
        
    return True

#Funciones de carga de datos CSV
# Posibles tiposDatos: 
# - lab_iniciales, 
# - evolucion_p1,
# - evolucion_p2, 
# - medicacion, 
# - notas, 
# - pacientes y
# - procedimientos
def cargarDatos(tipoDatos):
    path = rf".\CSV\resumen_{tipoDatos}.csv"  # La 'r' antes de la cadena evita caracteres de escape
    df = pd.read_csv(path)
    return df


