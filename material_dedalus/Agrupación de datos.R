library(dplyr)
library(readr)
library(purrr)  # Lee múltiples archivos a la vez


# Definir la ruta de los archivos
ruta_archivos <- "C:/Users/mpord/Documents/3IngSoft/2Cuatri/G4.Dedalus/material_dedalus/DataSetIndividuales/"

# Obtener lista de archivos CSV
archivos_csv <- list.files(path = ruta_archivos, pattern = "\\.csv$", full.names = TRUE)

# Leer los archivos CSV
df_list <- lapply(archivos_csv, read_csv, show_col_types = FALSE)

# Unir todos los archivos progresivamente por 'PacienteID'
df_final <- Reduce(function(x, y) full_join(x, y, by = "PacienteID"), df_list)

df_final


write_csv(df_final, "resumen_pacientes_combinados.csv")


