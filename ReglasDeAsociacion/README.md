# README - Detección de Enfermedades y Reglas de Asociación

Esta sección del proyecto tiene como objetivo el uso de bases de datos relacionadas con la detección de enfermedades para generar reglas de asociación utilizando el lenguaje de programación R. A continuación, se detallan las bases de datos utilizadas y cómo se aplican las reglas de asociación.


## **Base de Datos de Diagnóstico de Enfermedades **
   Estas bases de datos contiene registros de pacientes, junto con características relacionadas con la salud y diagnósticos médicos. Los datos incluyen información sobre síntomas, condiciones preexistentes, historial médico, edad, género y diagnóstico final. Estas bases de datos se usa para detectar patrones en los síntomas y factores asociados a diferentes enfermedades.

[Disease Symptoms and Patient Profile Dataset](https://data.mendeley.com/datasets/dv5z3v2xyd/1)

[SymbiPredict](https://data.mendeley.com/datasets/dv5z3v2xyd/1)

## Generación de Reglas de Asociación en R

### Paso 1: Preparación de los Datos
Antes de generar las reglas de asociación, se realiza una limpieza de los datos para asegurarse de que las variables relevantes estén en el formato adecuado (por ejemplo, convertir los datos de síntomas y tratamientos a formato binario, donde 1 indica la presencia del síntoma o tratamiento, y 0 indica su ausencia).

### Paso 2: Instalación de Paquetes Necesarios
En R, utilizamos el paquete `arules` para generar las reglas de asociación. Este paquete permite realizar análisis de reglas de asociación sobre conjuntos de datos transaccionales.

```r
install.packages("arules")
library(arules)
```

### Paso 3: Carga de Datos
Los datos se cargan en R en formato adecuado, como CSV o archivo de texto.

```r
datos_enfermedades <- read.csv("disease_diagnosis.csv")
datos_tratamientos <- read.csv("medications_and_treatments.csv")
```

### Paso 4: Transformación de Datos a Formato Transaccional
Convertimos los datos en un formato transaccional adecuado para las reglas de asociación. Esto puede implicar la conversión de los síntomas y tratamientos en columnas binarias.

```r
# Ejemplo de conversión de datos
enfermedades_binarias <- as.data.frame(sapply(datos_enfermedades, function(x) ifelse(x == "Síntoma_A", 1, 0)))
```

### Paso 5: Generación de Reglas de Asociación
Utilizamos la función `apriori()` para generar reglas de asociación sobre las bases de datos.

```r
# Generación de reglas con el algoritmo Apriori
reglas <- apriori(enfermedades_binarias, parameter = list(support = 0.05, confidence = 0.7))

# Visualización de las reglas
inspect(reglas)
```

### Paso 6: Interpretación de las Reglas
Las reglas generadas muestran asociaciones entre los síntomas y las enfermedades. Por ejemplo, una regla podría ser:  
**{Síntoma_X, Síntoma_Y} => {Enfermedad_A}**  
Lo que significa que si un paciente tiene el Síntoma_X y el Síntoma_Y, es probable que sea diagnosticado con la Enfermedad_A.

## Recomendaciones
Las reglas de asociación pueden ayudar a identificar patrones clave en los datos médicos y facilitar la toma de decisiones sobre diagnósticos y tratamientos. Sin embargo, es importante tener en cuenta que las reglas generadas son una guía y deben ser validadas con expertos médicos antes de su implementación práctica.

