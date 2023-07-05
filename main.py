import tkinter as tk
from Object3D import Object3D
from math import pi
import numpy as np
import time

# Creating the window
window = tk.Tk()
window.title("3D Representation of Earth and Moon")

# Create a canvas and place it in the window
canvas_width = 800
canvas_height = 800
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='#000022')
canvas.pack()

# Perspective configuration
FOV = pi / 3
ASPECT_RATIO = canvas_width / canvas_height
near = 0.1
far = 1000

# Loading the Earth and Moon models
EARTH_MODEL = './shapes/earth.obj'
MOON_MODEL = './shapes/moon.obj'

# Creating the Earth and Moon objects
earth = Object3D(EARTH_MODEL, [0, 0, 12], FOV, ASPECT_RATIO, near, far, canvas_width, canvas_height, 0)

# Center of the screen
center_x, center_y = canvas_width / 2, canvas_height / 2  # Screen center

# Frames per second
fps = 60
interval = int(1000 / fps)  # Interval between frames in milliseconds
# Animation duration
duration = 30  # Duration in seconds


# Function to calculate the distance to the center
def distance_to_center(vertex):
    dx = center_x - vertex[0]
    dy = center_y - vertex[1]
    return dx * dx + dy * dy


# Function to render polygons
def render_polygons(polygons, canvas_c, near_c, far_c):
    for vertices, color in polygons:
        # Clipping against the near and far planes
        if all((near_c <= vertex[2] <= far_c) for vertex in vertices):
            # Calculating the face normal vector
            u = np.array([vertices[1][0] - vertices[0][0], vertices[1][1] -
                          vertices[0][1], vertices[1][2] - vertices[0][2]])
            v = np.array([vertices[2][0] - vertices[0][0], vertices[2][1] -
                          vertices[0][1], vertices[2][2] - vertices[0][2]])
            normal = np.cross(u, v)

            # Checking if the face is facing backwards
            if normal[2] > 0:
                # Drawing the lines of the face
                polygon_coords = [coord for vertex in vertices for coord in vertex[:2]]
                canvas_c.create_polygon(polygon_coords, fill=color, outline='black')


# Function to animate the Earth and Moon rotation
def animate(start_time):
    # Calculate the elapsed time since the animation started
    elapsed_time = time.time() - start_time

    # Check if the animation duration has been reached
    if elapsed_time >= duration:
        window.destroy()
        return

    # Clear the canvas at the beginning of each frame
    canvas.delete("all")
    polygons = []

    earth_speed = 5  # Earth rotation speed

    # Generate the polygons for the Earth
    polygons += earth.get_animated_polygons(earth_speed, axis='y')

    # Sort the polygons by the average squared distance of their vertices to the center of the screen
    polygons.sort(key=lambda x: -np.mean([distance_to_center(vertex) for vertex in x[0]]))

    # Render the polygons
    for polygon in polygons:
        render_polygons([polygon], canvas, near, far)

    # Call the animate function again after a pause
    canvas.after(interval, animate, start_time)


# Function to start the animation
def start_animation():
    # Record the start time
    start_time = time.time()

    # Start the animation
    animate(start_time)


# Start the animation
start_animation()

# Start the main window loop
window.mainloop()
