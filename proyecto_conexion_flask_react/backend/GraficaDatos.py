#FUNCIONES QUE HAY QUE HACER 

# Gráficas de dispersión: Relación entre dos variables importantes. X (falta test) -
# Histogramas: Distribución de los datos (p. ej., glucosa, creatinina). X (falta test) -
# Boxplots: Dispersión y valores atípicos. X (falta test) -
# Gráficas de barras: Comparación entre grupos o condiciones. X (falta test) -
# Matriz de correlación (Heatmap): Relación entre múltiples variables. X (falta test) -
# Curvas de tendencia: Evolución de datos a lo largo del tiempo. X(M)(falta test) -
# Diagramas de violín: Comparación de distribuciones y dispersión de los datos. X(M)(falta test) -
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import DataFrame
# Definir los colores personalizados
color2 = "#c5e86c"  # greenD
color1 = "#4298b5"  # azul1D Actual

PATH="pacientes"

#Funciones de gráficas
def grafica(df, path):
    graficaCorrelacion(df,path)
 

def graficaCorrelacion(df,path):
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10,8))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Mapa de Calor de Correlación")

    path_file  = pathDirectorio(f"{path}\matrizCorrelacion",f"matrizCorrelacion-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
    #path_file = os.path.join(path,path_file)
    

    plt.savefig(path_file)

    limpiar()
    return path_file

def graficaDispersion(df: DataFrame,x:str,y:str,path:str):
    lista =[x,y]
    if verificarNombreColumnas(df,lista) == True:
        x = lista[0]
        y= lista[1]

        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(8,5))
        ax = sns.scatterplot(x=df[x], y=df[y], color= color1)
        plt.title("Relación entre " + x + " y " + y)
        plt.xlabel(x)
        plt.ylabel(y)

        path_file  = pathDirectorio(f"{path}\graficaDispersion",f"graficaDispersion-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
        #path_file = os.path.join(path,path_file)
    

        plt.savefig(path_file)

        limpiar()
        return path_file
    else:
        return -1

def graficaHistograma(df, y,path,bins=10):
    lista =[y]
    if verificarNombreColumnas(df,lista) == True:
        y= lista[0]
        sns.set_theme(style="whitegrid")
        if bins == None:
            bins = 10
        ax = sns.histplot(df[y], kde=True, bins=bins, color= color1)
        plt.title("Histograma " + y)
        plt.xlabel(y)
        plt.ylabel("Frecuencia")

        path_file  = pathDirectorio(f"{path}\graficaHistograma",f"graficaHistograma-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
        #path_file = os.path.join(path,path_file)
    

        plt.savefig(path_file)

        limpiar()
        return path_file
    else:
        return -1    

def graficaBarras(df,x,y,path):
    lista =[x,y]
    if verificarNombreColumnas(df,lista) == True:
        x = lista[0]
        y= lista[1]
        sns.set_theme(style="whitegrid")
        ax = sns.barplot(x=df[x], y=df[y], data=df, color= color1)
        plt.title("Gráfica de barras")

        path_file  = pathDirectorio(f"{path}\graficaBarras",f"graficaBarras-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
        #path_file = os.path.join(path,path_file)
    

        plt.savefig(path_file)

        limpiar()
        return path_file
    else:
        return -1

def graficaBoxplot(df,x,path):
    lista =[x]
    if verificarNombreColumnas(df,lista) == True:
        x = lista[0]
        
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(8,5))
        ax = sns.boxplot(y=df[x], color= color1) 
        plt.title("Boxplot de " + x)
        plt.xlabel(x)

        path_file  = pathDirectorio(f"{path}\graficaBoxplot",f"graficaBoxplot-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
        #path_file = os.path.join(path,path_file)
    

        plt.savefig(path_file)

        limpiar()
        return path_file
    else:
        return -1


def graficaViolin(df, x,path):
    lista =[x]
    if verificarNombreColumnas(df,lista) == True:
        x = lista[0]
        
        sns.set_theme(style="whitegrid")
        sns.violinplot(x=df[x], color= color1)
        plt.title("diagramaViolin")
        #print("tengo el grafico")
        path_file  = pathDirectorio(f"{path}\graficaViolin",f"graficaViolin-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
        #path_file = os.path.join(path,path_file)
        #print(path_file)

        plt.savefig(path_file)
        #print("guarde el grafico en el path" + path_file)
        limpiar()
        return path_file
    else:
        return -1
    
def graficaCurvaTendencia(df,x,y,path):
    lista =[x,y]
    if verificarNombreColumnas(df,lista) == True:
        x = lista[0]
        y= lista[1]
        sns.set_theme(style="whitegrid")
        sns.regplot(data=df, x=x, y=y, order=2, color= color1)
        plt.title("curvaTendencia")

        path_file  = pathDirectorio(f"{path}\graficaCurvaTendencia",f"graficaCurvaTendencia-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
        #path_file = os.path.join(path,path_file)
    

        plt.savefig(path_file)

        limpiar()
        return path_file
    else:
        return -1
    
#Crea si no existe un directorio con el nombre pasado por direc y 
# devuelve un path con el directorio y la imagen
# Si no hay filename crea un directorio (generalmente el del paciente)
def pathDirectorio(dir_name,filename= "non"):
    # Crea el directorio si no existe
    os.makedirs(dir_name, exist_ok=True) 
    file_path = os.path.relpath(dir_name)

    if filename != "non": #si se genera una imagen
        file_path = os.path.join(dir_name, f"{filename}.png")

    # Guardar el gráfico dentro del directorio
    return file_path

# Actualizar las gráficas
def limpiar ():
    plt.clf()   # Limpia la figura actual
    plt.close() # Cierra la figura para evitar acumulación

# Devuelve los nombres de las columnas del dataframe
def cargarNombreColumnas(df: DataFrame):
    return df.columns


#Verifica que los nombres de columnas pasados por parámetro existan en el dataframe
#Devuelve True si el nombre pasado no existe dentro del conjunto de nombres de columnas
def verificarNombreColumnas(df: DataFrame,columnas: (str |list)):
    for i in range(len(columnas)):
        x = str(columnas[i])

        j=0
        for col in df.columns:
            c = str(col)
            j+=1

            if x!=c :
                if x.casefold() == c.casefold():
                    columnas[i] = c
                    j=0
                    continue
            
        if j== len(df.columns):
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
    path = rf".\datos_pacientes\resumen_{tipoDatos}.csv"  # La 'r' antes de la cadena evita caracteres de escape
    df = pd.read_csv(path)
    return df

def generarRutaPublicPacientes():
    # Obtener la ruta absoluta de la carpeta 'backend'
    ruta_backend = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta de la carpeta 'public'
    ruta_public = os.path.join(ruta_backend, "..", "public", "pacientes")

    # Crear el directorio si no existe
    os.makedirs(ruta_public, exist_ok=True)

    print(f"backend: {ruta_backend} y public: {ruta_public}")
    return os.path.relpath(ruta_public)

def modificarPath(path_orig):
    #palabra ="pacientes"
    #while palabra not in path_orig:
    #    path_orig = path_orig[1:]  # Elimina el primer caracter de la cadena (izquierda a derecha)
    path_orig = path_orig.replace('..\\public\\', "")
    return path_orig

#FUNCION GENERAL A LLAMAR
def generarGrafica(data_name: str,id_patient:str,x:str,y:str=None,graphics:(str | list)=[]):

    path_ruta_pacientes = generarRutaPublicPacientes()

    path = os.path.join(path_ruta_pacientes,id_patient)
    print(f"Path con directorio paciente id: {path}")

    path = pathDirectorio(path) #Se genera directorio si no existe

    df = cargarDatos(data_name)

    if not graphics:
        return graficaCorrelacion(df,path)
    
    lista_paths = []
    res=-1

    for g in graphics:
        if g == "graficaCorrelacion":
            res=graficaCorrelacion(df,path)
        elif g =="graficaDispersion":
            res=graficaDispersion(df,x,y,path)
        elif g =="graficaHistograma":
            res=graficaHistograma(df,x,path=path)
        elif g =="graficaBarras":
            res=graficaBarras(df,x,y,path)
        elif g =="graficaBoxplot" :
            res=graficaBoxplot(df,x,path)
            #lista_paths.append(graficaBoxplot(df,x,path))
        elif g == "graficaViolin":
            res = graficaViolin(df,x,path)
        elif g == "graficaCurvaTendencia":
            res = graficaCurvaTendencia(df,x,y,path)
        else :
            lista_paths.append(" ")


        if res != -1:
            path_new = modificarPath(res)
            #print("path new es " + path_new)
            lista_paths.append(path_new)




    return lista_paths

    

    



   