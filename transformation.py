import numpy as np
from math import cos, sin, tan


def translation(v):
    # Esta função cria uma matriz de translação com base num vetor de translação v.
    # 'v' é uma lista ou array de valores representando a translação em cada dimensão.
    size = len(v)
    value = np.eye(size + 1)
    value[:-1, -1] = v
    return value


def dilation(v):
    # Esta função cria uma matriz de dilatação com base num vetor de dilatação v.
    # 'v' é uma lista ou array de valores representando a dilatação em cada dimensão.
    size = len(v)
    value = np.eye(size + 1)
    value[:-1, :-1] = np.diag(v)
    return value


def rotation_x(angle):
    # Esta função cria uma matriz de rotação em torno do eixo X com base num ângulo fornecido.
    # 'angle' é o ângulo de rotação em graus.
    angle = np.radians(angle)
    value = np.array([[1, 0, 0, 0],
                      [0, np.cos(angle), -np.sin(angle), 0],
                      [0, np.sin(angle), np.cos(angle), 0],
                      [0, 0, 0, 1]])
    return value


def rotation_y(angle):
    # Esta função cria uma matriz de rotação em torno do eixo Y com base num ângulo fornecido.
    # 'angle' é o ângulo de rotação em graus.
    return np.array([[cos(angle), 0, sin(angle), 0],
                     [0, 1, 0, 0],
                     [-sin(angle), 0, cos(angle), 0],
                     [0, 0, 0, 1]])


def rotation_z(angle):
    # Esta função cria uma matriz de rotação em torno do eixo Z com base num ângulo fornecido.
    # 'angle' é o ângulo de rotação em graus.
    angle = np.radians(angle)
    value = np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                      [np.sin(angle), np.cos(angle), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])
    return value


def apply_perspective_projection(rotated_vertices, fov, aspect_ratio, near, far):
    # Esta função aplica a projeção perspetiva a vértices rotacionados.
    # 'rotated_vertices' são os vértices após as transformações de rotação.
    # 'fov' é o campo de visão em radianos.
    # 'aspect_ratio' é a razão entre a largura e a altura da tela.
    # 'near' e 'far' são os planos de corte da câmara,
    # representando as distâncias mínima e máxima, respetivamente, que a câmara pode ver.

    # Cria a matriz de projeção perspetiva.
    proj_matrix = [
        [aspect_ratio * (1 / tan(fov / 2)), 0, 0, 0],
        [0, 1 / tan(fov / 2), 0, 0],
        [0, 0, -(far + near) / (far - near), -2 * far * near / (far - near)],
        [0, 0, -1, 0]
    ]

    projected_vertices = []

    for vertex in rotated_vertices:
        x, y, z = vertex
        # Converte o vértice para coordenadas homogêneas.
        vertex_4d = [x, y, z, 1]
        # Aplica a matriz de projeção ao vértice.
        vertex_proj = [sum([vertex_4d[i] * proj_matrix[j][i] for i in range(4)]) for j in range(4)]

        # Converte de volta para coordenadas 3D se o valor de w (vertex_proj[3]) for diferente de 0.
        if vertex_proj[3] != 0:
            vertex_proj = [i / vertex_proj[3] for i in vertex_proj[:-1]]
        else:
            vertex_proj = vertex_proj[:-1]
        projected_vertices.append(vertex_proj)

    return projected_vertices
