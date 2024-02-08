import networkx as nx
from tkinter import *
from tkinter import ttk
from collections import Counter

# Construcción del grafo de características
def construir_grafo_caracteristicas():
    G = nx.Graph()
    
    G.add_node("Inicio")  # Agregar nodo de inicio
    G.add_node("Color")
    G.add_node("Forma del cuerpo")
    G.add_node("Tipo de antenas")
    G.add_node("Número de patas")

    G.add_edge("Inicio", "Color", weight=0)  # Agregar conexión desde nodo de inicio a características
    G.add_edge("Inicio", "Forma del cuerpo", weight=0)
    G.add_edge("Inicio", "Tipo de antenas", weight=0)
    G.add_edge("Inicio", "Número de patas", weight=0)

    G.add_edge("Color", "Forma del cuerpo", weight=0.8)
    G.add_edge("Color", "Tipo de antenas", weight=0.6)
    G.add_edge("Color", "Número de patas", weight=0.7)
    # Agregar más relaciones...

    return G

# Algoritmo de clasificación utilizando Dijkstra
def clasificar_insecto(caracteristicas, grafo):
    # Construir el nombre del nodo objetivo
    nodo_objetivo = "_".join([caracteristica + "_" + caracteristicas[caracteristica] for caracteristica in caracteristicas])

    # Encontrar el camino más corto desde el nodo de inicio hasta el nodo objetivo
    try:
        camino_mas_corto = nx.dijkstra_path(grafo, "Inicio", nodo_objetivo, weight="weight")
        clasificacion = camino_mas_corto[-1].split("_")[-1]  # Obtener la clasificación del último nodo del camino
        return clasificacion
    except nx.NetworkXNoPath:
        return "Insecto no clasificado"


# Interfaz de usuario
def clasificar_insecto_interfaz(grafo):
    ventana = Tk()
    ventana.title("Clasificación de Insectos")

    def clasificar():
        caracteristicas = {
            "Color": color_combobox.get(),
            "Forma del cuerpo": forma_combobox.get(),
            "Tipo de antenas": antenas_combobox.get(),
            "Número de patas": patas_combobox.get()
        }
        tipo_insecto = clasificar_insecto(caracteristicas, grafo)
        resultado.config(text="Clasificación: " + tipo_insecto)

    color_label = Label(ventana, text="Color:")
    color_label.grid(row=0, column=0)
    color_combobox = ttk.Combobox(ventana, values=["Amarillo", "Verde", "Naranja", "Rojo"])
    color_combobox.grid(row=0, column=1)

    forma_label = Label(ventana, text="Forma del cuerpo:")
    forma_label.grid(row=1, column=0)
    forma_combobox = ttk.Combobox(ventana, values=["Alargada", "Redonda"])
    forma_combobox.grid(row=1, column=1)

    antenas_label = Label(ventana, text="Tipo de antenas:")
    antenas_label.grid(row=2, column=0)
    antenas_combobox = ttk.Combobox(ventana, values=["Largas", "Cortas"])
    antenas_combobox.grid(row=2, column=1)

    patas_label = Label(ventana, text="Número de patas:")
    patas_label.grid(row=3, column=0)
    patas_combobox = ttk.Combobox(ventana, values=["6", "8"])
    patas_combobox.grid(row=3, column=1)

    clasificar_button = Button(ventana, text="Clasificar", command=clasificar)
    clasificar_button.grid(row=4, column=0, columnspan=2)

    resultado = Label(ventana, text="")
    resultado.grid(row=5, column=0, columnspan=2)

    ventana.mainloop()

# Datos de evaluación
datos_evaluacion = [
    ({"Color": "Amarillo", "Forma del cuerpo": "Alargada", "Tipo de antenas": "Largas", "Número de patas": "6"}, "Abeja"),
    ({"Color": "Verde", "Forma del cuerpo": "Redonda", "Tipo de antenas": "Cortas", "Número de patas": "8"}, "Escarabajo"),
    ({"Color": "Amarillo", "Forma del cuerpo": "Alargada", "Tipo de antenas": "Largas", "Número de patas": "6"}, "Abeja"),
    ({"Color": "Verde", "Forma del cuerpo": "Redonda", "Tipo de antenas": "Cortas", "Número de patas": "8"}, "Escarabajo"),
    ({"Color": "Naranja", "Forma del cuerpo": "Alargada", "Tipo de antenas": "Largas", "Número de patas": "8"}, "Mariposa"),
    # Agregar más datos de evaluación según sea necesario
]

# Evaluación del sistema
def evaluar_sistema(datos_evaluacion, grafo):
    total = len(datos_evaluacion)
    correctos = 0
    for caracteristicas, clasificacion_correcta in datos_evaluacion:
        resultado_clasificacion = clasificar_insecto(caracteristicas, grafo)
        if resultado_clasificacion == clasificacion_correcta:
            correctos += 1
    
    precision = correctos / total
    return precision

# Construir el grafo de características
grafo_caracteristicas = construir_grafo_caracteristicas()

# Evaluación del sistema
precision_sistema = evaluar_sistema(datos_evaluacion, grafo_caracteristicas)
print("La precisión del sistema de clasificación es:", precision_sistema)

# Interfaz de usuario para clasificar insectos
clasificar_insecto_interfaz(grafo_caracteristicas)
