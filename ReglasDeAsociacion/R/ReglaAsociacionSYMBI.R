
library(arules)
symbipredict_2022 <- read.csv("CSV/symbipredict_2022.csv")

df_reduced <- symbipredict_2022[1:2000,]
#Estas son la enfermedades que se detectan con el dataset
symbipredict_2022$prognosis |> unique()

df_reduced$prognosis |> unique()

#Obetenemos las columnas que no sean relevantes ya que solo tengan un valor
valores_unicos <- lapply(df_reduced, unique)

valores_unicos_len_1 <- valores_unicos[sapply(valores_unicos, length) == 1]

# En este caso es fluid_overload y la eliminamos
df_reduced$fluid_overload <- NULL

df_reduced$prognosis <- as.factor(df_reduced$prognosis)
          

trans <- as(df_reduced, "transactions")

rules <- apriori(trans, parameter = list(support = 0.01, confidence = 0.8, maxlen=5))


