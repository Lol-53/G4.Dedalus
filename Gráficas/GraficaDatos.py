'''import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def grafica(datos):
    df = pd.DataFrame(datos)
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x="x", y="y", data=df)
    plt.show()



df = pd.read_csv('data.csv')
grafica(df)'''

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Funciones de gráficas

def grafica(datos):
    
    return null

def graficaBarras(df,x,y):
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x=df[x], y=df[y], data=df)
    plt.title("Gráfica de barras")
    plt.savefig()

def cargarDatos(tipoDatos):
    df = pd.read_csv(f".\CSV\{tipoDatos}.csv",raw=True)
    
    return df



# Cargar el archivo CSV
df = pd.read_csv(r".\CSV\resumen_lab_iniciales.csv")

print(df.columns)



# Mostrar las primeras filas
print("\nPrimeras filas del dataset:")
print(df.head())

# Información sobre los datos
print("\nInformación del dataset:")
print(df.info())

# Resumen estadístico
print("\nResumen estadístico:")
print(df.describe())

# Configuración de estilo de Seaborn
sns.set_theme(style="whitegrid", palette=["#4298b5", "#c5e86c"])

# Histograma de Glucosa
plt.figure(figsize=(8,5))
sns.histplot(df["Glucosa"], kde=True, bins=10)
plt.title("Distribución de Glucosa")
plt.show()

# Gráfico de dispersión pH vs Glucosa
plt.figure(figsize=(8,5))
sns.scatterplot(x=df["Glucosa"], y=df["pH"])
plt.title("Relación entre Glucosa y pH")
plt.show()

# Regresión Cetonas vs Glucosa
plt.figure(figsize=(8,5))
sns.lmplot(x="Glucosa", y="Cetonas", data=df, line_kws={'color':'black'})
plt.title("Cetonas vs Glucosa")
plt.show()

# Boxplot de Glucosa
plt.figure(figsize=(8,5))
sns.boxplot(y=df["Glucosa"])
plt.title("Distribución de Glucosa")
plt.show()

# Boxplot de Leucocitos
plt.figure(figsize=(8,5))
sns.boxplot(y=df["Leucocitos"])
plt.title("Distribución de Leucocitos")
plt.show()

# Heatmap de correlación
plt.figure(figsize=(10,6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Matriz de Correlación")
plt.show()
