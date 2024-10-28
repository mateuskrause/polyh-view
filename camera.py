import numpy as np
import wireframe as wf
import transform as tf

class Camera:

    e = np.array([0, 0, 0, 1])
    g = np.array([0, 0, -1, 1])
    t = np.array([0, 1, 0, 1])

    u = np.array([1, 0, 0, 1])
    v = np.array([0, 1, 0, 1])
    w = np.array([0, 0, 1, 1])

    def __init__(self):
        self.matrix = self.create_camera_ortho(self.u, self.v, self.w, self.e)
    
    def create_camera_ortho(self, u, v, w, e):
        M = np.zeros((4, 4))
        M_1 = np.zeros((4, 4))
        M_2 = np.zeros((4, 4))

        # "aligning _u_, _v_, _w_ to x, y, z"
        M_1[0, 0] = u[0]; M_1[0, 1] = u[1]; M_1[0, 2] = u[2]; M_1[0, 3] = 0
        M_1[1, 0] = v[0]; M_1[1, 1] = v[1]; M_1[1, 2] = v[2]; M_1[1, 3] = 0
        M_1[2, 0] = w[0]; M_1[2, 1] = w[1]; M_1[2, 2] = w[2]; M_1[2, 3] = 0
        M_1[3, 0] = 0   ; M_1[3, 1] = 0   ; M_1[3, 2] = 0   ; M_1[3, 3] = 1

        # "move _e_ to the origin"
        M_2[0, 0] = 1; M_2[0, 1] = 0; M_2[0, 2] = 0; M_2[0, 3] = -e[0]
        M_2[1, 0] = 0; M_2[1, 1] = 1; M_2[1, 2] = 0; M_2[1, 3] = -e[1]
        M_2[2, 0] = 0; M_2[2, 1] = 0; M_2[2, 2] = 1; M_2[2, 3] = -e[2]
        M_2[3, 0] = 0; M_2[3, 1] = 0; M_2[3, 2] = 0; M_2[3, 3] = 1

        M = M_1 @ M_2

        return M
    
    def create_camera(self, e, g, t):

        e = e[:3]
        g = g[:3]
        t = t[:3]

        w = -g / np.linalg.norm(g)
        u = np.cross(t, w) / np.linalg.norm(np.cross(t, w))
        v = np.cross(w, u)

        self.u = np.append(u, 1)
        self.v = np.append(v, 1)
        self.w = np.append(w, 1)

        return self.create_camera_ortho(self.u, self.v, self.w, self.e)

    def rotate(self, angle_x, angle_y, angle_z):
        M_x = wf.create_rotation_matrix_x(angle_x)
        M_y = wf.create_rotation_matrix_y(angle_y)
        M_z = wf.create_rotation_matrix_z(angle_z)

        B = np.array([self.u, self.v, self.w, np.array([0, 0, 0, 1])]).T

        self.g = B @ M_z @ M_y @ M_x @ np.linalg.inv(B) @ self.g
        self.t = B @ M_z @ M_y @ M_x @ np.linalg.inv(B) @ self.t

        self.matrix = self.create_camera(self.e, self.g, self.t)

    def translate(self, pos):
        B = np.array([self.u, self.v, self.w, np.array([0, 0, 0, 1])]).T
        M = tf.create_translation(B @ pos)

        # dont change the y when translating
        old_y = self.e[1]
        self.e = M @ self.e
        self.e[1] = old_y

        self.matrix = self.create_camera(self.e, self.g, self.t)
        print(self.e)
