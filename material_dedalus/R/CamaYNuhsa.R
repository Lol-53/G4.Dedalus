#Añadir las columas camas y NUHSA



lista_NUHSA <-  c('58386840', '34720037', '62347987', '69669872', '87428439', '72171424', '19263546', '39677235', '31031511', '97905741')

lista_NUHSA <-  paste("NA",lista_NUHSA)


camas <-  c(1:10)


resumen_pacientes <- read.csv("C:/Users/mpord/Documents/3IngSoft/2Cuatri/G4.Dedalus/material_dedalus/DatosSQUAD/CSV/resumen_pacientes.csv")


resumen_pacientes$Cama <- camas
resumen_pacientes$NUHSA <- lista_NUHSA

df_final <-  resumen_pacientes


write.csv(df_final,file="resumen_pacientes_NUHSA.csv",row.names = FALSE)
