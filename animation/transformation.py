import numpy as np
from math import cos, sin, tan


def translation(v):
    """
    Realiza uma translação de um vetor no espaço 3D
    :param v: Vetor de translação [dx, dy, dz]
    :return: Matriz de translação 4x4
    """
    size = len(v)
    value = np.eye(size + 1)
    value[:-1, -1] = v
    return value


def dilation(v):
    """
    Realiza uma dilatação de um vetor no espaço 3D
    :param v: Vetor de dilatação [sx, sy, sz]
    :return: Matriz de dilatação 4x4
    """
    size = len(v)
    value = np.eye(size + 1)
    value[:-1, :-1] = np.diag(v)
    return value


def rotation_x(angle):
    """
    Realiza uma rotação em torno do eixo x no espaço 3D
    :param angle: Ângulo de rotação em graus
    :return: Matriz de rotação 4x4
    """
    angle = np.radians(angle)
    value = np.array([[1, 0, 0, 0],
                      [0, np.cos(angle), -np.sin(angle), 0],
                      [0, np.sin(angle), np.cos(angle), 0],
                      [0, 0, 0, 1]])
    return value


def rotation_y(angle):
    """
    Realiza uma rotação em torno do eixo y no espaço 3D
    :param angle: Ângulo de rotação em graus
    :return: Matriz de rotação 4x4
    """
    return np.array([[cos(angle), 0, sin(angle), 0],
                     [0, 1, 0, 0],
                     [-sin(angle), 0, cos(angle), 0],
                     [0, 0, 0, 1]])


def rotation_z(angle):
    """
    Realiza uma rotação em torno do eixo z no espaço 3D
    :param angle: Ângulo de rotação em graus
    :return: Matriz de rotação 4x4
    """
    angle = np.radians(angle)
    value = np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                      [np.sin(angle), np.cos(angle), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])
    return value


def apply_perspective_projection(rotated_vertices, fov, aspect_ratio, near, far):
    """
    Aplica a projeção de perspetiva aos vértices rotacionados
    :param rotated_vertices: Lista de vértices rotacionados [(x, y, z), ...]
    :param fov: Campo de visão em radianos
    :param aspect_ratio: Razão de aspeto da tela (largura/altura)
    :param near: Plano de corte próximo
    :param far: Plano de corte distante
    :return: Lista de vértices projetados [(x_proj, y_proj, z_proj), ...]
    """
    # Cria a matriz de projeção perspetiva.
    proj_matrix = [
        [aspect_ratio * (1 / tan(fov / 2)), 0, 0, 0],
        [0, 1 / tan(fov / 2), 0, 0],
        [0, 0, -(far + near) / (far - near), -2 * far * near / (far - near)],
        [0, 0, -1, 0]
    ]

    projected_vertices = []

    # Converte o vértice para coordenadas homogéneas
    for vertex in rotated_vertices:
        x, y, z = vertex
        vertex_4d = [x, y, z, 1]
        # Aplica a projeção de perspetiva aos vértices
        vertex_proj = [sum([vertex_4d[i] * proj_matrix[j][i] for i in range(4)]) for j in range(4)]

        # Divide pelos componentes homogéneos para obter as coordenadas projetadas
        if vertex_proj[3] != 0:
            vertex_proj = [i / vertex_proj[3] for i in vertex_proj[:-1]]
        else:
            vertex_proj = vertex_proj[:-1]
        projected_vertices.append(vertex_proj)

    return projected_vertices
