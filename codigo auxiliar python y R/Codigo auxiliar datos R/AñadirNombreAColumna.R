resumen_lab_iniciales <- read.csv("C:/Users/mpord/Documents/3IngSoft/2Cuatri/G4.Dedalus/material_dedalus/DatosSQUAD/resumen_lab_iniciales.csv")
resumen_pacientes <- read.csv("C:/Users/mpord/Documents/3IngSoft/2Cuatri/G4.Dedalus/material_dedalus/DatosSQUAD/resumen_pacientes.csv")


df_nombre <- cbind(resumen_lab_iniciales,Nombre=resumen_pacientes$Nombre)


write.csv(df_nombre,file="resumen_lab_iniciales_conNombre.csv",row.names = FALSE)


resumen_medicacion <- read.csv("C:/Users/mpord/Documents/3IngSoft/2Cuatri/G4.Dedalus/material_dedalus/DatosSQUAD/resumen_medicacion.csv")

df_nombre <- cbind(resumen_medicacion,Nombre=resumen_pacientes$Nombre)


write.csv(df_nombre,file="resumen_medicacion_conNombre.csv",row.names = FALSE)