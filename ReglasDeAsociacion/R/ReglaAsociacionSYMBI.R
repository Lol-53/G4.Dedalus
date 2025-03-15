
library(arules)
symbipredict_2022 <- read.csv("CSV/symbipredict_2022.csv")


#Estas son la enfermedades que se detectan con el dataset
symbipredict_2022$prognosis |> unique()

#Obetenemos las columnas que no sean relevantes ya que solo tengan un valor
valores_unicos <- lapply(symbipredict_2022, unique)

valores_unicos_len_1 <- valores_unicos[sapply(valores_unicos, length) == 1]

# En este caso es fluid_overload y la eliminamos
symbipredict_2022$fluid_overload <- NULL

symbipredict_2022$prognosis <- as.factor(symbipredict_2022$prognosis)
          

trans <- as(symbipredict_2022, "transactions")

rules <- apriori(trans, parameter = list(support = 0.01, confidence = 0.9))


