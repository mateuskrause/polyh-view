import numpy as np

def create_rotation_matrix_x(angle):
    rad = np.radians(angle)
    return np.array([
        [1, 0          , 0           , 0],
        [0, np.cos(rad), -np.sin(rad), 0],
        [0, np.sin(rad),  np.cos(rad), 0],
        [0, 0          , 0           , 1]
    ])

def create_rotation_matrix_y(angle):
    rad = np.radians(angle)
    return np.array([
        [ np.cos(rad), 0, np.sin(rad), 0],
        [0           , 1, 0          , 0],
        [-np.sin(rad), 0, np.cos(rad), 0],
        [0           , 0, 0          , 1]
    ])

def create_rotation_matrix_z(angle):
    rad = np.radians(angle)
    return np.array([
        [np.cos(rad), -np.sin(rad), 0, 0],
        [np.sin(rad),  np.cos(rad), 0, 0],
        [0          , 0           , 1, 0],
        [0          , 0           , 0, 1]
    ])

def create_rotation_matrix(axis, angle):
    # rotation matrix around an arbitrary axis
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis

    rad = np.radians(angle)
    cos_a = np.cos(rad)
    sin_a = np.sin(rad)

    return np.array([
        [cos_a + x * x * (1 - cos_a)    , x * y * (1 - cos_a) - z * sin_a, x * z * (1 - cos_a) + y * sin_a, 0],
        [y * x * (1 - cos_a) + z * sin_a, cos_a + y * y * (1 - cos_a)    , y * z * (1 - cos_a) - x * sin_a, 0],
        [z * x * (1 - cos_a) - y * sin_a, z * y * (1 - cos_a) + x * sin_a, cos_a + z * z * (1 - cos_a)    , 0],
        [0                              , 0                              , 0                              , 1]
    ])

class Point:
    def __init__(self, x, y, z, w):
        self.coords = np.array([x, y, z, w])

class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

class Face:
    def __init__(self, edges):
        self.edges = edges

    def add_edge(self, edge):
        self.edges.append(edge)

class Wireframe:
    def __init__(self):
        self.points = []
        self.edges = []
        self.faces = []
        self.name = ""

    def add_edge(self, p1, p2):
        if p1 not in self.points:
            self.points.append(p1)

        if p2 not in self.points:
            self.points.append(p2)

        self.edges.append(Edge(p1, p2))

    def add_face(self, face):
        self.faces.append(face)

    # rotate all the poins in the wireframe on the y axis by a certain degree
    def rotate(self, angle_x, angle_y, angle_z):
        rotation_matrix_x = create_rotation_matrix_x(angle_x)
        rotation_matrix_y = create_rotation_matrix_y(angle_y)
        rotation_matrix_z = create_rotation_matrix_z(angle_z)

        for point in self.points:
            point.coords = np.dot(rotation_matrix_x, point.coords)
            point.coords = np.dot(rotation_matrix_y, point.coords)
            point.coords = np.dot(rotation_matrix_z, point.coords)