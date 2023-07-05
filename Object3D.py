import random
import time
from obj_handler import parse_obj_file
import numpy as np
from operations import translate, rotate_around_object_y, rotate_around_object_x, rotate_around_object_z
from math import pi, cos, sin

from utils import apply_perspective_projection


class Object3D:
    def __init__(self, obj_file_path, position, fov, aspect_ratio, near, far, canvas_width, canvas_height, start_angle):
        # Carregar vértices e faces do arquivo .obj
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
        self.r, self.g, self.b = 33, 70, 94  # Blue color
        self.moon_radius = 10

    def get_animated_polygons(self, step, axis='y'):
        # Update the rotation angle
        self.angle += step

        # Copy the original vertices for transformation
        self.vertices = np.copy(self.original_vertices)

        # Move the vertices to the object's position
        self.vertices = translate(self.vertices, [self.x, self.y, self.z])

        # Apply rotations around the axes
        if axis == 'x':
            self.vertices = rotate_around_object_x(self.vertices, self.angle * (pi / 180))
        elif axis == 'y':
            self.vertices = rotate_around_object_y(self.vertices, self.angle * (pi / 180))
        elif axis == 'z':
            self.vertices = rotate_around_object_z(self.vertices, self.angle * (pi / 180))

        # Apply perspective projection to the vertices
        self.vertices = apply_perspective_projection(self.vertices, self.fov, self.aspect_ratio, self.near, self.far)

        # Map vertices to screen coordinates
        screen_vertices = [(x * self.canvas_width / 2 + self.canvas_width / 2, -y * self.canvas_height / 2 +
                            self.canvas_height / 2, z) for x, y, z in self.vertices]

        # Initialize the list to store polygons
        polygons = []
        fill_color = '#%02x%02x%02x' % (self.r, self.g, self.b)
        # Para cada face, gerar os polígonos correspondentes
        for face in self.faces:
            if len(face) > 3:  # Se a face tem mais de 3 vértices, geramos múltiplos triângulos
                for i in range(1, len(face) - 1):
                    vertices = [screen_vertices[face[0]], screen_vertices[face[i]], screen_vertices[face[i + 1]]]
                    polygons.append((vertices, fill_color))
            else:  # Caso contrário, geramos um único polígono para a face
                vertices = [screen_vertices[i] for i in face]
                polygons.append((vertices, fill_color))

        # Calculate moon's position and angle based on the orbit axis

        moon_angle = self.angle * (pi / 180)
        if axis == 'x':
            moon_x = self.x
            moon_y = self.y + self.moon_radius * cos(moon_angle)
            moon_z = self.z + self.moon_radius * sin(moon_angle)
        elif axis == 'y':
            moon_x = self.x + self.moon_radius * cos(moon_angle)
            moon_y = self.y
            moon_z = self.z + self.moon_radius * sin(moon_angle)
        elif axis == 'z':
            moon_x = self.x + self.moon_radius * cos(moon_angle)
            moon_y = self.y + self.moon_radius * sin(moon_angle)
            moon_z = self.z

        moon_position = [moon_x, moon_y, moon_z]

        # Translate, rotate, and project the moon vertices
        moon_vertices = translate(self.original_vertices, moon_position)
        moon_vertices = rotate_around_object_y(moon_vertices, -self.angle * (pi / 180))
        moon_vertices = translate(moon_vertices, [self.x, self.y, self.z])
        moon_vertices = apply_perspective_projection(moon_vertices, self.fov, self.aspect_ratio, self.near, self.far)
        moon_screen_vertices = [(x * self.canvas_width / 2 + self.canvas_width / 2, -y * self.canvas_height / 2 +
                                 self.canvas_height / 2, z) for x, y, z in moon_vertices]

        # Define the fill color for the moon
        moon_fill_color = '#cccccc'  # Color for the moon

        # Generate polygons for the moon
        for face in self.faces:
            if len(face) > 3:
                for i in range(1, len(face) - 1):
                    polygon = [moon_screen_vertices[face[0]],
                               moon_screen_vertices[face[i]],
                               moon_screen_vertices[face[i + 1]]]
                    polygons.append((polygon, moon_fill_color))

        # Return the polygons for both the Earth and the Moon
        return polygons