# Leer el CSV (ajusta la ruta al archivo)
resumen_notas <- read.csv("C:/Users/mpord/Documents/3IngSoft/2Cuatri/G4.Dedalus/material_dedalus/DatosSQUAD/resumen_notas.csv")

# Renombrar las columnas para mayor claridad
colnames(resumen_notas) <- c("ID", "Fecha", "Nota")

# Ver las primeras filas para inspeccionar las fechas
head(resumen_notas$Fecha)
tail(resumen_notas$Fecha)

# Función para convertir las fechas al formato dd/MM/yyyy
convertir_fecha <- function(fecha) {
  # Si la fecha está en formato yyyy-MM-dd (Ej: 2024-08-09)
  if (grepl("^\\d{4}-\\d{2}-\\d{2}$", fecha)) {
    fecha_convertida <- as.Date(fecha, format="%Y-%m-%d")
  } else if (grepl("^\\d{2}/\\d{2}/\\d{4}$", fecha)) {  # Si está en formato dd/MM/yyyy (Ej: 13/07/2023)
    fecha_convertida <- as.Date(fecha, format="%d/%m/%Y")
  } else {
    fecha_convertida <- NA  # Si no se encuentra el formato, dejarlo como NA
  }
  return(format(fecha_convertida, "%d/%m/%Y"))
}

# Aplicar la función de conversión a la columna 'fecha'
resumen_notas$Fecha <- sapply(resumen_notas$Fecha, convertir_fecha)

# Verificar los resultados
head(resumen_notas$Fecha)
tail(resumen_notas$Fecha)



# Guardar el archivo CSV con las fechas formateadas
write.csv(resumen_notas, "resumen_medicacion_fechaEstandar.csv", row.names = FALSE)
