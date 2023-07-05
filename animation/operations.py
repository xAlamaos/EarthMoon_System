from transformation import rotation_x, rotation_y, rotation_z, translation
import numpy as np


def rotate_around_object_y(vertices, angle):
    """
    Rotaciona os vértices de um objeto ao redor do eixo y.
    :param vertices: Lista de vértices do objeto
    :param angle: Ângulo de rotação em radianos
    :return: Lista de vértices rotacionados
    """
    center = np.mean(vertices, axis=0)  # Calcula o centro do objeto
    translated_to_origin_vertices = vertices - center  # Translada os vértices para a origem
    # Transforma os vértices para coordenadas homogêneas
    homogeneous_vertices = np.array([np.append(vertex, 1) for vertex in translated_to_origin_vertices])
    rotation_matrix = rotation_y(angle)  # Obtém a matriz de rotação em torno do eixo y
    rotated_vertices = np.dot(homogeneous_vertices, rotation_matrix.T)  # Aplica a matriz de rotação
    rotated_vertices = rotated_vertices[:, :3]  # Remove as coordenadas homogêneas
    repositioned_vertices = rotated_vertices + center  # Reposiciona os vértices
    return repositioned_vertices


# E aqui roda os vértices ao redor do eixo x do objeto
def rotate_around_object_x(vertices, angle):
    """
    Rotaciona os vértices em torno do eixo z de um objeto 3D
    :param vertices: Lista de vértices do objeto
    :param angle: Ângulo de rotação em radianos
    :return: Vértices rotacionados
    """
    center = np.mean(vertices, axis=0)  # Calcula o centro do objeto
    translated_to_origin_vertices = vertices - center  # Translada os vértices para a origem
    # Transforma os vértices para coordenadas homogêneas
    homogeneous_vertices = np.array([np.append(vertex, 1) for vertex in translated_to_origin_vertices])
    rotation_matrix = rotation_x(angle)  # Obtém a matriz de rotação em torno do eixo x
    rotated_vertices = np.dot(homogeneous_vertices, rotation_matrix.T)  # Aplica a matriz de rotação
    rotated_vertices = rotated_vertices[:, :3]  # Remove as coordenadas homogêneas
    repositioned_vertices = rotated_vertices + center  # Reposiciona os vértices
    return repositioned_vertices


# E agora a gente roda os vértices ao redor do eixo z do objeto
def rotate_around_object_z(vertices, angle):
    """
    Rotaciona os vértices em torno do eixo z de um objeto 3D
    :param vertices: Lista de vértices do objeto
    :param angle: Ângulo de rotação em radianos
    :return: Vértices rotacionados
    """
    center = np.mean(vertices, axis=0)  # Calcula o centro do objeto
    translated_to_origin_vertices = vertices - center  # Translada os vértices para a origem
    # Transforma os vértices para coordenadas homogêneas
    homogeneous_vertices = np.array([np.append(vertex, 1) for vertex in translated_to_origin_vertices])
    rotation_matrix = rotation_z(angle)  # Obtém a matriz de rotação em torno do eixo z
    rotated_vertices = np.dot(homogeneous_vertices, rotation_matrix.T)  # Aplica a matriz de rotação
    rotated_vertices = rotated_vertices[:, :3]  # Remove as coordenadas homogêneas
    repositioned_vertices = rotated_vertices + center  # Reposiciona os vértices
    return repositioned_vertices


def translate(vertices, translation_vector):
    """
    Translada os vértices de um objeto 3
    :param vertices: Lista de vértices do objeto
    :param translation_vector: Vetor de translação representado por uma lista de três valores (x, y, z)
    :return: Lista de vértices transladados
    """
    translation_matrix = translation(translation_vector)  # Obtém a matriz de translação com base no vetor de translação
    # Adiciona um valor 1 no final de cada vértice para coordenadas homogêneas
    homogeneous_vertices = [np.append(vertex, 1) for vertex in vertices]
    # Aplica a translação a cada vértice multiplicando a matriz de
    # translação pelo vetor de coordenadas homogêneas do vértice
    translated_vertices = [np.dot(translation_matrix, vertex) for vertex in homogeneous_vertices]
    # Remove o valor 1 adicionado anteriormente para voltar às coordenadas não homogêneas
    translated_vertices = [list(vertex[:3]) for vertex in translated_vertices]
    return translated_vertices  # Retorna a lista de vértices transladados
