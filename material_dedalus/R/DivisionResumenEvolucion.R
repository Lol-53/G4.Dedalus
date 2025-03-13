resumen_evolucion_process <- read.csv("C:/Users/mpord/Documents/3IngSoft/2Cuatri/G4.Dedalus/material_dedalus/DatosSQUAD/resumen_evolucion_process.csv")


str(resumen_evolucion_process)


p1 <- resumen_evolucion_process[1:15,]

p2 <- resumen_evolucion_process[16:27,]




write.csv(p1, "resumen_evolucion_p1.csv",row.names = FALSE)
write.csv(p2, "resumen_evolucion_p2.csv",row.names = FALSE)



