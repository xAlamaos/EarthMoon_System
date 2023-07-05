from transformation import rotation_x, rotation_y, rotation_z, translation
import numpy as np


# Agora a gente roda os vértices ao redor do eixo y do objeto
def rotate_around_object_y(vertices, angle):
    """

    :param vertices:
    :param angle:
    :return:
    """
    center = np.mean(vertices, axis=0)  # Descobre o centro do objeto
    translated_to_origin_vertices = vertices - center  # Translada o objeto para a origem
    # Transforma os vértices para coordenadas homogêneas
    homogeneous_vertices = np.array([np.append(vertex, 1) for vertex in translated_to_origin_vertices])
    rotation_matrix = rotation_y(angle)  # Pega a matriz de rotação
    rotated_vertices = np.dot(homogeneous_vertices, rotation_matrix.T)  # Aplica a matriz de rotação
    rotated_vertices = rotated_vertices[:, :3]  # Volta para coordenadas não homogêneas
    repositioned_vertices = rotated_vertices + center  # Reposiciona o objeto
    return repositioned_vertices


# E aqui roda os vértices ao redor do eixo x do objeto
def rotate_around_object_x(vertices, angle):
    """

    :param vertices:
    :param angle:
    :return:
    """
    center = np.mean(vertices, axis=0)  # Descobre o centro do objeto
    translated_to_origin_vertices = vertices - center  # Translada o objeto para a origem
    # Transforma os vértices para coordenadas homogêneas
    homogeneous_vertices = np.array([np.append(vertex, 1) for vertex in translated_to_origin_vertices])
    rotation_matrix = rotation_x(angle)  # Pega a matriz de rotação
    rotated_vertices = np.dot(homogeneous_vertices, rotation_matrix.T)  # Aplica a matriz de rotação
    rotated_vertices = rotated_vertices[:, :3]  # Volta para coordenadas não homogêneas
    repositioned_vertices = rotated_vertices + center  # Reposiciona o objeto
    return repositioned_vertices


# E agora a gente roda os vértices ao redor do eixo z do objeto
def rotate_around_object_z(vertices, angle):
    """

    :param vertices:
    :param angle:
    :return:
    """
    center = np.mean(vertices, axis=0)  # Descobre o centro do objeto
    translated_to_origin_vertices = vertices - center  # Translada o objeto para a origem
    # Transforma os vértices para coordenadas homogêneas
    homogeneous_vertices = np.array([np.append(vertex, 1) for vertex in translated_to_origin_vertices])
    rotation_matrix = rotation_z(angle)  # Pega a matriz de rotação
    rotated_vertices = np.dot(homogeneous_vertices, rotation_matrix.T)  # Aplica a matriz de rotação
    rotated_vertices = rotated_vertices[:, :3]  # Volta para coordenadas não homogêneas
    repositioned_vertices = rotated_vertices + center  # Reposiciona o objeto
    return repositioned_vertices


# E por fim, uma função para transladar os vértices, ou seja, mover o objeto para lá e para cá
def translate(vertices, translation_vector):
    """

    :param vertices:
    :param translation_vector:
    :return:
    """
    translation_matrix = translation(translation_vector)  # Pega a matriz de translação
    # Transforma os vértices para coordenadas homogêneas
    homogeneous_vertices = [np.append(vertex, 1) for vertex in vertices]
    # Aplica a matriz de translação
    translated_vertices = [np.dot(translation_matrix, vertex) for vertex in homogeneous_vertices]
    translated_vertices = [list(vertex[:3]) for vertex in translated_vertices]  # Volta para coordenadas não homogêneas
    return translated_vertices


