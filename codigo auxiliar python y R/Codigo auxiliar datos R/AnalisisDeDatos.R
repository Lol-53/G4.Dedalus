resumen_evolucion_process <- read.csv("C:/Users/mpord/Documents/3IngSoft/2Cuatri/G4.Dedalus/material_dedalus/resumen_evolucion_process.csv")
library(tidyverse)

# # 1. Asignar la primera fila como nombres de las columnas
# colnames(resumen_evolucion) <- as.character(resumen_evolucion[1, ])
# 
# # 2. Eliminar la primera fila del dataset
# resumen_evolucion <- resumen_evolucion[-1, ]
# 
# resumen_evolucion
# 
# # 3. Eliminar la última columna 
# resumen_evolucion$`NA` <- NULL
# 
# class(resumen_evolucion)
# 
# resumen_evolucion |>
#   filter(PacienteID=18)
#   
# class(resumen_evolucion[[3]][23])
class(resumen_evolucion_process)

resumen_evolucion_process |>
  str()

resumen_evolucion_process |>
  filter(is.integer())





# 
# 
# resumen_evolucion_process$NA. <- NULL
# # # Exportar el dataset modificado como un archivo CSV
# write.csv(resumen_evolucion, "resumen_evolucion_process.csv", row.names = FALSE)


colnames(resumen_evolucion_process)
colnames(resumen_lab_iniciales)
colnames(resumen_medicacion)
colnames(resumen_notas)
colnames(resumen_pacientes)
colnames(resumen_procedimientos)
