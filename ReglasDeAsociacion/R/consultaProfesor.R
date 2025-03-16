library(arules)
library(jsonlite)
df <- read.csv("CSV/archive/Disease_symptom_and_patient_profile_dataset.csv")

#Observar características de la función
str(df)

df$Age <- ordered(cut(df[[ "Age"]], c(15,25,45,65,100)),
                        labels = c("Young", "Middle-aged", "Senior", "Old"))

#Procedemos a transformar las columnas a factor previamente verificado que no hay variables continuas
df <- lapply(df, factor)
str(df)

#Transformamos a 
trans <- as(df,"transactions")


rules<- apriori(trans)
inspect(head(rules))


rules_2 <- apriori(trans, parameter = list(support = 0.01, confidence = 0.5))
inspect(head(rules_2))

rules_subset_1 <- subset(rules, support >= 0.02 & confidence >= 0.6)
inspect(head(rules_subset_1))

rules_subset_2 <- subset(rules, lift>0.3)
inspect(head(rules_subset_1))


# GUARDAR REGLAS EN JSON


rules_df <- as(rules,"data.frame")
rules_2_df <- as(rules_2,"data.frame")

rules_json <- toJSON(rules_df, pretty = TRUE)
rules_2_json <- toJSON(rules_2_df, pretty = TRUE)

write(rules_json, file = "rules.json")
write(rules_2_json, file = "rules_2.json")



rules_subset_1_df <- as(rules_subset_1,"data.frame")
rules_subset_2_df <- as(rules_subset_2,"data.frame")

rules_subset_1_json <- toJSON(rules_subset_1_df, pretty = TRUE)
rules_subset_2_json <- toJSON(rules_subset_2_df, pretty = TRUE)

write(rules_subset_1_json, file = "rules_subset_1.json")
write(rules_subset_2_json, file = "rules_subset_2.json")

# Guardar el JSON en un archivo






