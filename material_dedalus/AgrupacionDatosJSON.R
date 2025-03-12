library(tidyverse)

library(jsonlite) 



resumen_evolucion_process <- read.csv("C:/Users/mpord/Documents/3IngSoft/2Cuatri/G4.Dedalus/material_dedalus/resumen_evolucion_process.csv")

df <- resumen_evolucion_process

df$Fecha <- paste(df$Fecha,df$Hora,sep= "-")
df$Hora <- NULL


json_result <- toJSON(df[-c(1)], pretty = TRUE)
df_json$JSON <- json_result


df_json <- mutate(df,JSON=json_result)

json_result_2 <- toJSON(df_json[c(2,30)], pretty = TRUE)
cat(json_result_2)


# Mostrar el resultado JSON
cat(json_result)

df_grouped <- df %>%
  group_by(PacienteID) %>%
  summarise(
    registros = list(
      data.frame(
        Fecha = Fecha,
        PresionSistolica = PresionSistolica,
        PresionDiastolica = PresionDiastolica,
        FrecuenciaCardiaca = FrecuenciaCardiaca,
        Temperatura = Temperatura,
        FrecuenciaRespiratoria = FrecuenciaRespiratoria,
        SaturacionOxigeno = SaturacionOxigeno,
        Glucosa = Glucosa,
        Leucocitos = Leucocitos,
        Hemoglobina = Hemoglobina,
        Plaquetas = Plaquetas,
        Colesterol = Colesterol,
        HDL = HDL,
        LDL = LDL,
        Trigliceridos = Trigliceridos,
        Sodio = Sodio,
        Potasio = Potasio,
        Cloro = Cloro,
        Creatinina = Creatinina,
        Urea = Urea,
        AST = AST,
        ALT = ALT,
        Bilirrubina = Bilirrubina,
        pH = pH,
        pCO2 = pCO2,
        pO2 = pO2,
        HCO3 = HCO3,
        Lactato = Lactato
      )
    ),
    .groups = "drop"
  )

df_flattened <- df_grouped %>%
  unnest(cols = c(registros))

# Guardar el resultado en un archivo CSV
write.csv(df_flattened, "output.csv", row.names = FALSE)


# Convertir a JSON
json_result <- toJSON(df_grouped, pretty = TRUE, auto_unbox = TRUE)


write_json(json_result,"datos_evolucion.json")
# Mostrar el resultado JSON
cat(json_result)


data_pac <- 

