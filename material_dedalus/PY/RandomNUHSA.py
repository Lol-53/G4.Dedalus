import random

def generar_numero_aleatorio(longitud):
    return str(random.randint(10**(longitud-1), 10**longitud - 1))

# Generar un número de 16 dígitos
numero_aleatorio = generar_numero_aleatorio(8)
lista= []


for i in range(1,11):
    numero_aleatorio = generar_numero_aleatorio(8)
    lista.append(numero_aleatorio)

print(lista, len(lista))