library(arules)
library(jsonlite)
df <- read.csv("C:/Users/mpord/Documents/3IngSoft/2Cuatri/G4.Dedalus/ReglasDeAsociacion/CSV/archive/Disease_symptom_and_patient_profile_dataset.csv")

str(df)

df[] <- lapply(df,factor)

trans <- as(df, "transactions")

rules <- apriori(trans, parameter = list(support = 0.01, confidence = 0.5))
inspect(head(rules,10))


# Filtrar las reglas con un soporte mínimo de 0.02 y confianza de 0.6
strong_rules <- subset(rules, support >= 0.02 & confidence >= 0.6)

# Ver las reglas filtradas
inspect(tail(strong_rules))

# Filtrar reglas con un Lift mayor a 3 (indica una relación fuerte entre A y B)
strong_rules_lift <- subset(rules, lift > 3)
inspect(head(strong_rules_lift,20))


strong_rules_lift_df <- as(strong_rules_lift,"data.frame")

# Convertir el data frame a JSON
rules_json <- toJSON(strong_rules_lift_df, pretty = TRUE)

# Guardar el JSON en un archivo
write(rules_json, file = "rules.json")
