# Secção de Importações
from obj_handler import parse_obj_file
import numpy as np
from operations import translate, rotate_around_object_y, rotate_around_object_x, rotate_around_object_z
from math import pi, cos, sin
from transformation import apply_perspective_projection


class Object3D:
    def __init__(self, obj_file_path, position, fov, aspect_ratio, near, far, canvas_width, canvas_height, start_angle):
        """
        Inicializa um objeto 3D com as seguintes propriedades:
        :param obj_file_path: Caminho para o arquivo '.obj' contendo os vértices e faces do objeto
        :param position: Posição inicial do objeto no espaço 3D (x, y, z)
        :param fov: Campo de visão da projeção de perspetiva
        :param aspect_ratio: Razão de aspeto da janela de renderização
        :param near: Distância do plano de corte próximo
        :param far: Distância do plano de corte distante
        :param canvas_width: Largura do canvas de renderização
        :param canvas_height: Altura do canvas de renderização
        :param start_angle: Ângulo inicial de rotação do objeto
        """
        # Carregar vértices e faces do ficheiro '.obj'
        self.original_vertices, self.faces = parse_obj_file(obj_file_path)
        # Definir a posição inicial do objeto 3D
        self.x, self.y, self.z = position
        # Definir os parâmetros da projeção de perspetiva
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
        # Definir o ângulo inicial de rotação do objeto
        self.angle = start_angle
        # Definir a largura e altura do canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        # Definir a cor do objeto como azul
        self.r, self.g, self.b = 33, 70, 94  # Cor planeta Terra
        self.moon_radius = 10  # Radio de translação da Lua com base na Terra
        # Inicializar os vértices com uma cópia dos vértices originais
        self.vertices = np.copy(self.original_vertices)

    def get_animated_polygons(self, step, axis='y'):
        """
        Retorna uma lista de polígonos a serem renderizados na animação atual
        :param step: Valor do incremento do ângulo de rotação
        :param axis: Eixo de rotação ("x", "y" ou "z")
        :return: Lista de polígonos para renderização
        """
        # Atualiza o ângulo de rotação
        self.angle += step

        # Copia os vértices originais para a transformação
        self.vertices = np.copy(self.original_vertices)

        # Move os vértices para a posição do objeto
        self.vertices = translate(self.vertices, [self.x, self.y, self.z])

        # Aplica rotações em torno dos eixos
        if axis == 'x':
            self.vertices = rotate_around_object_x(self.vertices, self.angle * (pi / 180))
        elif axis == 'y':
            self.vertices = rotate_around_object_y(self.vertices, self.angle * (pi / 180))
        elif axis == 'z':
            self.vertices = rotate_around_object_z(self.vertices, self.angle * (pi / 180))

        # Aplica projeção de perspetiva nos vértices
        self.vertices = apply_perspective_projection(self.vertices, self.fov, self.aspect_ratio, self.near, self.far)

        # Mapeia os vértices para coordenadas da tela
        screen_vertices = [(x * self.canvas_width / 2 + self.canvas_width / 2, -y * self.canvas_height / 2 +
                            self.canvas_height / 2, z) for x, y, z in self.vertices]

        # Inicializa a lista para armazenar os polígonos
        polygons = []
        fill_color = '#%02x%02x%02x' % (self.r, self.g, self.b)
        # Para cada face, gera os polígonos correspondentes
        for face in self.faces:
            if len(face) > 3:  # Se a face tiver mais de 3 vértices, gera vários triângulos
                for i in range(1, len(face) - 1):
                    vertices = [screen_vertices[face[0]], screen_vertices[face[i]], screen_vertices[face[i + 1]]]
                    polygons.append((vertices, fill_color))
            else:  # Caso contrário, gera um único polígono para a face
                vertices = [screen_vertices[i] for i in face]
                polygons.append((vertices, fill_color))

        # Calcula a posição e o ângulo da lua com base no eixo da órbita
        moon_angle = -self.angle * (pi / 180)  # Inverte o sinal do ângulo da lua
        moon_x = self.x + self.moon_radius * cos(moon_angle)
        moon_y = self.y
        moon_z = self.z + self.moon_radius * sin(moon_angle)
        moon_position = [moon_x, moon_y, moon_z]

        # Translada, rotaciona e projeta os vértices da lua
        moon_vertices = translate(self.original_vertices, moon_position)
        moon_vertices = rotate_around_object_y(moon_vertices, -self.angle * (pi / 180))
        moon_vertices = translate(moon_vertices, [self.x, self.y, self.z])
        moon_vertices = apply_perspective_projection(moon_vertices, self.fov, self.aspect_ratio, self.near, self.far)

        # Mapeia os vértices da lua para coordenadas da tela
        screen_moon_vertices = [(x * self.canvas_width / 2 + self.canvas_width / 2, -y * self.canvas_height / 2 +
                                 self.canvas_height / 2, z) for x, y, z in moon_vertices]

        # Define a cor de preenchimento para a lua
        moon_fill_color = '#cccccc'

        # Gera polígonos para a lua
        for face in self.faces:
            if len(face) > 3:
                for i in range(1, len(face) - 1):
                    polygon = [screen_moon_vertices[face[0]],
                               screen_moon_vertices[face[i]],
                               screen_moon_vertices[face[i + 1]]]
                    polygons.append((polygon, moon_fill_color))
            else:
                vertices = [screen_moon_vertices[i] for i in face]
                polygons.append((vertices, moon_fill_color))

        # Retorna os polígonos tanto para a Terra quanto para a Lua
        return polygons
