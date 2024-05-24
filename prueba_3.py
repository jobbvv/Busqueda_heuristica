from funciones import* #importa todas las funciones del script funciones.py

#Almacena las rutas de buses en un diccionario de la forma "nombre_ruta":{nodos que recorre la ruta},
#estas rutas serán comparados con la ruta optima obtenida del algoritmo A* para recomendar
#una ruta al usuario del sistema de transporte

rutas_buses = {
    "C1": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9)],
    "C2": [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9)],
    "C3": [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9)],
    "C4": [(3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9)],
    "C5": [(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9)],
    "C6": [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9)],
    "C7": [(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9)],
    "C8": [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9)],
    "C9": [(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9)],
    "C10": [(9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9)],
    "A1": [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0)],
    "A2": [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)],
    "A3": [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2)],
    "A4": [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3)],
    "A5": [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4)],
    "A6": [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5)],
    "A7": [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6)],
    "A8": [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7)],
    "A9": [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8)],
    "A10": [(0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9)],
    "D1": [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)]
}



# Crear la malla vial de 10 calles por 10 carreras
G, pos, etiquetas = crear_malla_vial(10, 10)

# Definir el nodo de origen y el nodo de llegada
inicio = (3, 5)  # Nodo de origen
meta = (8, 9)    # Nodo de llegada

# Encontrar la ruta más corta usando A*
ruta = algoritmo_a_estrella(G, inicio, meta)
ruta_coordenadas=algoritmo_a_estrella(G, inicio, meta)

#Compara las rutas de buses con la ruta optima y recomienda al usuario el bus de mayores coincidencias en la ruta
#Luego elimina los nodos que coinciden para buscar la siguiente ruta
#se logra borrando los nodos cubiertos hasta que el vector que contiene la ruta queda vacio
rutas_diccionario = {}

while ruta_coordenadas:
    nombre_ruta, coincidencias, coordenadas = contar_coincidencias(rutas_buses, ruta_coordenadas)
    
    # Agregar nombre de la ruta y coordenadas al diccionario
    rutas_diccionario[nombre_ruta] = coordenadas[-1]
    
#Ordeba los buses desde el mas cercano al origen hasta el mas lejano
rutas_ordenadas = ordenar_diccionario(rutas_diccionario)

#Imprime la recomendacion de rutas favorables al usuario
for bus in rutas_ordenadas:
    print(f"Tome la ruta:{bus} hasta la calle {rutas_ordenadas[bus][0]+1} con carrera {rutas_ordenadas[bus][1]+1}")

# Dibujar la malla vial con la ruta más corta y los nodos de origen y llegada

dibujar_malla_vial(G, pos, etiquetas, ruta, inicio, meta)

