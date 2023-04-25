import pandas as pd
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import numpy as np
import csv
import math
import itertools
from scipy.spatial import ConvexHull
import geojson


pygame.init()

screen_width = 1920
screen_height = 1080
ortho_left = -142
ortho_right = -52
ortho_top = 84
ortho_bottom = 41

pygame.display.set_mode((screen_width, screen_height), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption('Canadian Map With PyGame and PyOpenGL')

def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(ortho_left, ortho_right, ortho_bottom, ortho_top)


province_data = {}

def load_province_data():
    with open('provinces.geojson') as f:
        data = geojson.load(f)
    for feature in data['features']:
        properties = feature['properties']
        province_name = properties['PRENAME']
        latitude = None
        longitude = None
        for coordinates in feature['geometry']['coordinates']:
            coordinates_list = []
            coordinates_list.append(coordinates)
            if province_name not in province_data:
                province_data[province_name] = {'coordinates': [coordinates_list]}
            else:
                province_data[province_name]['coordinates'].append(coordinates_list)


border_points_dict = {}


def generate_random_rgb():
    colors = []
    for i in range(3):
        rgb = tuple(random.uniform(0, 1) for i in range(3))
        colors.append(rgb)
    return colors


def draw_border(province):
    iterator = 0
    for coordinates in province_data[province]['coordinates']:
        glBegin(GL_LINE_STRIP)
        for coordinate in coordinates:
            for coord in coordinate:
                glVertex2f(float(coord[0]), float(coord[1]))
        glEnd()


done = False
init_ortho()
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
load_province_data()
clock = pygame.time.Clock()
glLineWidth(1)
glColor(1.0, 1.0, 1.0, 1.0)

# Create two surfaces, one for drawing and one for displaying
drawing_surface = pygame.Surface((screen_width, screen_height))
display_surface = pygame.display.get_surface()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear the drawing surface
    drawing_surface.fill((0, 0, 0, 255))

    # Draw each line one at a time
    for province in province_data:
        for coordinates in province_data[province]['coordinates']:
            for coordinate in coordinates:
                for i in range(len(coordinate)):
                    glBegin(GL_POINTS)
                    if i < len(coordinate) - 1:
                        glVertex2f(float(coordinate[i][0]), float(coordinate[i][1]))
                        glVertex2f(float(coordinate[i+1][0]), float(coordinate[i+1][1]))
                    else:
                        glVertex2f(float(coordinate[i-1][0]), float(coordinate[i-1][1]))
                        glVertex2f(float(coordinate[i][0]), float(coordinate[i][1]))
                    glEnd()

                    # Update the drawing surface and display the changes
                    pygame.display.flip()

                    # Limit the frame rate to 60 FPS
                    clock.tick(2400)

    # Copy the drawing surface to the display surface
    display_surface.blit(drawing_surface, (0, 0))

    # Update the display
    pygame.display.flip()

# Quit the program
pygame.quit()

