# Seção de Importações
import tkinter as tk
from Object3D import Object3D
from math import pi
import numpy as np
import time


# Criação da janela e o seu nome
window = tk.Tk()
window.title("3D Representation of Earth and Moon")

# Criar o 'canvas' e meter-la na janela
canvas_width = 800
canvas_height = 800
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='#000022')
canvas.pack()

# Configuração de Perspetiva
FOV = pi / 3
ASPECT_RATIO = canvas_width / canvas_height
near = 0.1
far = 1000

# Carregar os modelos da Terra e Lua
EARTH_MODEL = './shapes/earth.obj'
MOON_MODEL = './shapes/moon.obj'

# Criação do Objeto Terra
earth = Object3D(EARTH_MODEL, [0, 0, 12], FOV, ASPECT_RATIO, near, far, canvas_width, canvas_height, 0)

# Centro do Ecrã
center_x, center_y = canvas_width / 2, canvas_height / 2

# Quadros por segundo
fps = 60
interval = int(1000 / fps)  # Intervalo entre quadros em milissegundos
# Duração da Animação
duration = 30  # Tempo em segundos (60 = 1 min)


# Função para calcular a distância até ao centro
def distance_to_center(vertex):
    """
    Calcula a distância de um vértice até o centro do canvas
    :param vertex: Lista com as coordenadas x, y e z do vértice
    :return: Distância do vértice ao centro do canvas
    """
    dx = center_x - vertex[0]
    dy = center_y - vertex[1]
    return dx * dx + dy * dy


# Função para renderizar polígonos
def render_polygons(polygons, canvas_c, near_c, far_c):
    """
    Renderiza os polígonos na tela
    :param polygons: Lista de polígonos a serem renderizados, cada um contendo uma lista de vértices e a cor do polígono
    :param canvas_c: Objeto de canvas do Tkinte
    :param near_c: Distância do plano de recorte próximo
    :param far_c: Distância do plano de recorte distante
    """
    for vertices, color in polygons:
        # Cortando contra os planos próximos e distantes
        if all((near_c <= vertex[2] <= far_c) for vertex in vertices):
            # Cálculo do vetor normal da face
            u = np.array([vertices[1][0] - vertices[0][0], vertices[1][1] -
                          vertices[0][1], vertices[1][2] - vertices[0][2]])
            v = np.array([vertices[2][0] - vertices[0][0], vertices[2][1] -
                          vertices[0][1], vertices[2][2] - vertices[0][2]])
            normal = np.cross(u, v)

            # Verificação se a face está voltada para trás
            if normal[2] > 0:
                # Desenhar as linhas da face
                polygon_coords = [coord for vertex in vertices for coord in vertex[:2]]
                canvas_c.create_polygon(polygon_coords, fill=color, outline='black')


# Função para animar a rotação da Terra e da Lua
def animate(start_time):
    """
    Função de animação para girar a Terra e a Lua
    :param start_time: Tempo de início da animação
    """
    # Cálculo do tempo decorrido após o início da animação
    elapsed_time = time.time() - start_time

    # Verifica se a duração da animação foi atingida
    if elapsed_time >= duration:
        window.destroy()  # Fecha a animação por completo quando o tempo final é atingido
        return

    # Limpa o ecrã no início de cada atualização de 'frame'
    canvas.delete("all")
    polygons = []

    earth_speed = 10  # Velocidade da Rotação da Terra

    # Criação de polígonos para a Terra
    polygons += earth.get_animated_polygons(earth_speed, axis='y')

    # Organiza os polígonos pela distância média ao quadrado dos seus vértices até o centro do ecrã
    polygons.sort(key=lambda x: -np.mean([distance_to_center(vertex) for vertex in x[0]]))

    # Renderiza os polígonos
    for polygon in polygons:
        render_polygons([polygon], canvas, near, far)

    # Chama a função 'animate' novamente após uma pausa
    canvas.after(interval, animate, start_time)


# Function to start the animation
def start_animation():
    """
    Função para iniciar a animação
    :return:
    """
    # Registra o tempo de início
    start_time = time.time()

    # Inicia a animação
    animate(start_time)


# Inicia a animação
start_animation()

# Inicia o loop principal da janela
window.mainloop()
