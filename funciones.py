import math
import networkx as nx
import matplotlib.pyplot as plt
from heapq import heappush, heappop
def crear_malla_vial(n_calles, n_carreras):
    G = nx.grid_2d_graph(n_calles, n_carreras)
   
    # Convertir las posiciones (i, j) a sistema coordenado (j,i) por que salen
    #de la forma (y,x) y almacenarlas en el diccionario pos
    pos = {(x, y): (y, x) for x, y in G.nodes()}
    
    # Enumerar nodos de izquierda a derecha y de arriba a abajo
    etiquetas = {}
    contador = 1
    for x in range(n_calles):
        for y in range(n_carreras):
            etiquetas[(x, y)] = contador
            contador += 1

    # Agregar conexión diagonal principal
    for i in range(min(n_calles, n_carreras) - 1):
        G.add_edge((i, i), (i + 1, i + 1))
   
    return G, pos, etiquetas

def dibujar_malla_vial(G, pos, etiquetas, ruta=None, origen=None, llegada=None):
    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=False, node_size=500, node_color='lightblue', font_size=8)
    nx.draw_networkx_labels(G, pos, labels=etiquetas, font_size=8, font_color='black')
    # si se le proporciuona una ruta la pinta de azul
    if ruta:
        aristas_ruta = list(zip(ruta, ruta[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=aristas_ruta, edge_color='b', width=2)
  
    if origen:
        nx.draw_networkx_nodes(G, pos, nodelist=[origen], node_color='g', node_size=500)

    if llegada:
        nx.draw_networkx_nodes(G, pos, nodelist=[llegada], node_color='r', node_size=500)

    plt.title("Malla Vial 10x10 con Nodos Enumerados y Diagonal Principal")
    plt.show()

def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def algoritmo_a_estrella(G, inicio, meta):
    conjunto_abierto = []
    #pone al nodo inicial en cola de prioridad
    heappush(conjunto_abierto, (0, inicio))
    padre = {}
    costo_g = {nodo: float('inf') for nodo in G.nodes()}
    costo_g[inicio] = 0
    costo_total = {nodo: float('inf') for nodo in G.nodes()}
    costo_total[inicio] = heuristica(inicio, meta)

    ruta_coordenadas = None  # Inicializa ruta_coordenadas como None

    while conjunto_abierto:
        #extrae el nodo de menor costo en la cola de prioridad
        actual = heappop(conjunto_abierto)[1]

        if actual == meta:
            ruta = []
            while actual in padre:
                ruta.append(actual)
                actual = padre[actual]
            ruta.append(inicio)
            ruta.reverse()
            ruta_coordenadas = [(nodo[0], nodo[1]) for nodo in ruta]

        for vecino in G.neighbors(actual):
            costo_g_tentativo = costo_g[actual] + 1

            if costo_g_tentativo < costo_g[vecino]:
                padre[vecino] = actual
                costo_g[vecino] = costo_g_tentativo
                costo_total[vecino] = costo_g[vecino] + heuristica(vecino, meta)
                heappush(conjunto_abierto, (costo_total[vecino], vecino))

    return ruta_coordenadas

def contar_coincidencias(rutas_buses, ruta_coordenadas):
    max_coincidencias_seguidas = 0
    ruta_max_coincidencias_seguidas = None
    coordenadas_max_coincidencias = []
    
    for ruta, coordenadas_ruta in rutas_buses.items():
        coincidencias_seguidas = 0
        coordenadas_coincidencias_seguidas = []
        
        for coordenada_ruta in coordenadas_ruta:
            if coordenada_ruta in ruta_coordenadas:
                coincidencias_seguidas += 1
                coordenadas_coincidencias_seguidas.append(coordenada_ruta)
            else:
                if coincidencias_seguidas > max_coincidencias_seguidas:
                    max_coincidencias_seguidas = coincidencias_seguidas
                    ruta_max_coincidencias_seguidas = ruta
                    coordenadas_max_coincidencias = coordenadas_coincidencias_seguidas
                coincidencias_seguidas = 0
                coordenadas_coincidencias_seguidas = []
        
        # Verificar si las coincidencias seguidas al final de la ruta son las máximas
        if coincidencias_seguidas > max_coincidencias_seguidas:
            max_coincidencias_seguidas = coincidencias_seguidas
            ruta_max_coincidencias_seguidas = ruta
            coordenadas_max_coincidencias = coordenadas_coincidencias_seguidas
    
    # Eliminar las coordenadas de coordenadas_coincidencias_seguidas de ruta_coordenadas
    for coordenada in coordenadas_max_coincidencias:
        if coordenada in ruta_coordenadas:
            ruta_coordenadas.remove(coordenada)
    
    return ruta_max_coincidencias_seguidas, max_coincidencias_seguidas, coordenadas_max_coincidencias



# Función para calcular la distancia euclidiana al origen
def calcular_distancia(coord, inicio):
    return math.sqrt((coord[0] - inicio[0])**2 + (coord[1] - inicio[1])**2)

# Función para ordenar el diccionario
def ordenar_diccionario(rutas_diccionario, inicio=(0, 1)):
    return dict(sorted(rutas_diccionario.items(), key=lambda item: calcular_distancia(item[1], inicio)))
