### **Explicación de la función `generarGrafica`**

### **Parámetros de entrada**
```python
def generarGrafica(data_name: str, id_patient: str, x: str, y: str = None, graphics: (str | list) = []):
```


1. **`data_name` (str):** Nombre del conjunto de datos a cargar.

    (`"lab_iniciales"`, `"evolucion_p1"`, `"evolucion_p2"`,`"medicacion"`,`"notas"`,`"pacientes"` o `"procedimientos"`).


2. **`id_patient` (str):** Identificador del paciente, usado para crear un directorio donde se almacenarán las gráficas.


3. **`x` (str):** Nombre de la variable que se utilizará en el eje X del gráfico.


4. **`y` (str, opcional):** Nombre de la variable que se utilizará en el eje Y del gráfico (solo para gráficos de relación como dispersión o curvas de tendencia).


5. **`graphics` (str o lista de str, opcional):** Tipo(s) de gráfico a generar. Puede ser una cadena (un solo gráfico) o una lista con múltiples gráficos.


    La lista `graphics` puede contener los siguientes valores para generar distintos tipos de gráficos:

    - **"graficaCorrelacion"** → Mapa de calor que muestra la correlación entre variables.
    - **"graficaDispersion"** → Gráfico de dispersión que representa la relación entre dos variables.
    - **"graficaHistograma"** → Histograma que muestra la distribución de una variable.
    - **"graficaBarras"** → Gráfico de barras para comparar categorías o grupos.
    - **"graficaBoxplot"** → Diagrama de caja que muestra la dispersión y valores atípicos de una variable.
    - **"graficaViolin"** → Diagrama de violín para visualizar la distribución y dispersión de los datos.
    - **"graficaCurvaTendencia"** → Curva de tendencia que muestra la evolución de los datos en el tiempo.

    Cada uno de estos valores generará una imagen correspondiente y devolverá su ruta.


La función devolverá una lista con los path de las imágenes generadas.