# Importación de librerías
import random as rd
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

### ------     CÁLCULO ESTIMADO  ---------

# Bullet 1: Experimento aleatorio

def crear_album(figus_total):
    '''
    Se crea un álbum  de figuritas vacío, representado por un vector de ceros,
    donde cada posición representa el estado de una figurita. En este caso
    los ceros indican que las figuritas aún no han sido conseguidas.
    '''
    album = []
    for i in range(figus_total):
        album.append(0)
    return album


def comprar_paquete(figus_total, figus_paquete):
    '''
    Genera un paquete de 5 figuritas diferentes,
    elegidas al azar del total de figuritas posibles.
    '''
    # Lista de todas las figuritas posibles (de 0 a figus-total - 1)
    universo_figus = list(range(figus_total))
    # Tomamos una muestra sin repetidos
    paquete = rd.sample(universo_figus, figus_paquete)
    return paquete


def pegar_figuras(album, paquete):
    '''
    Pega las figuritas del paquete en el álbum, actualizando su estado.
    '''
    for figura in paquete:
        album[figura] = 1
    return album

# Implementá la función album_incompleto(album) que recibe un vector album y devuelve True si 
# el álbum A no está completo y False si lo está. Recordá que un álbum estará incompleto siempre 
# que haya al menos un cero en alguna de sus posiciones.

def album_incompleto(album):
    for figura in album:
        if figura == 0:
            return True
    return False

# Por último, utilizá todas estas funciones para crear una única función que las invoque y que se 
# llame cuantos_paquetes(figus_total, figus_paquete) que cuente la cantidad de paquetes necesarios 
# hasta completar el álbum. Necesitarás usar la estructura de control while(), pues comprarás paquetes 
# mientras el álbum siga incompleto; y deberás generar un contador de paquetes_comprados que arranque 
# en 0 y sume un 1 cada vez que compres un nuevo paquete.

def cuantos_paquetes(figus_total, figus_paquete):
    album = crear_album(figus_total)
    paquetes_comprados = 0
    while album_incompleto(album):
        paquete = comprar_paquete(figus_total, figus_paquete)
        album = pegar_figuras(album, paquete)
        paquetes_comprados += 1
    return paquetes_comprados

# Bullet 2: Simulación

rd.seed(1234)  # Para reproducibilidad
# Definimos los parámetros del experimento
figus_total = 680
figus_paquete = 5
n_simulaciones = 100 # Número de simulaciones

# Inicializamos un vector para guardar los resultados
resultados = np.zeros(n_simulaciones)
# Realizamos las simulaciones
for i in range(n_simulaciones):
    resultados[i] = cuantos_paquetes(figus_total, figus_paquete)
# Calculamos la media y la desviación estándar
media = np.mean(resultados)
desviacion = np.std(resultados)
# Imprimimos los resultados
print(f"Media de paquetes necesarios: {media}")
print(f"Desviación estándar: {desviacion}")
# Graficamos los resultados
plt.figure(figsize=(10, 6))
sns.histplot(resultados, bins=30, kde=True)
plt.title('Distribución de paquetes necesarios para completar el álbum')
plt.xlabel('Paquetes comprados')
plt.ylabel('Frecuencia')
plt.axvline(media, color='red', linestyle='dashed', linewidth=1)
plt.axvline(media + desviacion, color='green', linestyle='dashed', linewidth=1)
plt.axvline(media - desviacion, color='green', linestyle='dashed', linewidth=1)
plt.legend({'Media': media, 'Desviación estándar': desviacion})
plt.show()


