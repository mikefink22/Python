x = "10"
y = "hola"
print (x+y)

def prueba():
  return 5
  print("Hola")

print(prueba())

def cambiar_valor(x):
  x = 5

valor = 10
cambiar_valor(valor)
print(valor)

x = 3
while x > 0:
  x -= 1
print("Fin del bucle")

def generar_lista(n):
  lista = []
  for i in range(n):
    lista.append(i * 2)
  return lista

print(generar_lista(-5))

# Genera ciclo infinito!!
# x = 10
# while x > 0:
#   if x == 5:
#     continue
# print(x)
# x -= 1


