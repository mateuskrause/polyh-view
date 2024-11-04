# Code inspired by the Learn WebGL documentation: https://learnwebgl.brown37.net/#section-7-cameras

import numpy as np
import wireframe as wf

class Camera:
    matrix = np.zeros((4, 4))

    e = np.array([0, 0,  0])
    g = np.array([0, 0, -1])
    t = np.array([0, 1,  0])

    u = np.array([1, 0, 0])
    v = np.array([0, 1, 0])
    w = np.array([0, 0, 1])

    def __init__(self):
        self.matrix = np.identity(4)

    def look_at(self, e, g, t):
        # local coordinate system for the camera:
        #   u maps to the x-axis
        #   v maps to the y-axis
        #   n maps to the z-axis

        self.e = np.array([e[0], e[1], e[2]])
        self.g = np.array([g[0], g[1], g[2]])
        self.t = np.array([t[0], t[1], t[2]])

        self.w = -self.g / np.linalg.norm(self.g)
        self.u = np.cross(self.t, self.w) / np.linalg.norm(np.cross(self.t, self.w))
        self.v = np.cross(self.w, self.u)

        tx = -np.dot(self.u, self.e)
        ty = -np.dot(self.v, self.e)
        tz = -np.dot(self.w, self.e)

        M = np.identity(4)

        M[0, 0] = self.u[0];  M[0, 1] = self.u[1];  M[0, 2] = self.u[2];  M[0, 3] = tx
        M[1, 0] = self.v[0];  M[1, 1] = self.v[1];  M[1, 2] = self.v[2];  M[1, 3] = ty
        M[2, 0] = self.w[0];  M[2, 1] = self.w[1];  M[2, 2] = self.w[2];  M[2, 3] = tz
        M[3, 0] = 0        ;  M[3, 1] = 0        ;  M[3, 2] = 0        ;  M[3, 3] = 1

        self.matrix = M
        
        return M
    
    def truck(self, distance):
        # move the camera left or right along the u axis by 'distance'
        u_scaled = self.u * distance
        self.e = self.e + u_scaled

        self.matrix[0, 3] = -np.dot(self.u, self.e)
        self.matrix[1, 3] = -np.dot(self.v, self.e)
        self.matrix[2, 3] = -np.dot(self.w, self.e)

    def pedestal(self, distance):
        # move the camera up or down along the v axis by 'distance'
        v_scaled = self.v * distance
        self.e = self.e + v_scaled

        self.matrix[0, 3] = -np.dot(self.u, self.e)
        self.matrix[1, 3] = -np.dot(self.v, self.e)
        self.matrix[2, 3] = -np.dot(self.w, self.e)

    def dolly(self, distance):
        # move the camera forward or backward along the w axis by 'distance'
        w_scaled = self.w * distance
        self.e = self.e + w_scaled

        self.matrix[0, 3] = -np.dot(self.u, self.e)
        self.matrix[1, 3] = -np.dot(self.v, self.e)
        self.matrix[2, 3] = -np.dot(self.w, self.e)

    def tilt(self, angle):
        # rotate the camera's coordinate system about u; updates v and n
        m_rotate = wf.create_rotation_matrix(self.u, angle)

        self.v = (m_rotate @ np.append(self.v, 1))[:3]
        self.w = (m_rotate @ np.append(self.w, 1))[:3]

        # update the 2nd and 3rd row of the camera transformation because only the v and n axes changed.
        self.matrix[1, 0] = self.v[0];  self.matrix[1, 1] = self.v[1];  self.matrix[1, 2] = self.v[2]
        self.matrix[2, 0] = self.w[0];  self.matrix[2, 1] = self.w[1];  self.matrix[2, 2] = self.w[2]

        # update the translate values of ty and tz
        self.matrix[1, 3] = -np.dot(self.v, self.e)
        self.matrix[2, 3] = -np.dot(self.w, self.e)

    def pan(self, angle):
        # rotate the camera's coordinate system about v; updates u and n
        m_rotate = wf.create_rotation_matrix(self.v, angle)

        self.u = (m_rotate @ np.append(self.u, 1))[:3]
        self.w = (m_rotate @ np.append(self.w, 1))[:3]

        # update the 1st and 3rd row of the camera transformation because only the u and n axes changed.
        self.matrix[0, 0] = self.u[0];  self.matrix[0, 1] = self.u[1];  self.matrix[0, 2] = self.u[2]
        self.matrix[2, 0] = self.w[0];  self.matrix[2, 1] = self.w[1];  self.matrix[2, 2] = self.w[2]

        # update the translate values of tx and tz
        self.matrix[0, 3] = -np.dot(self.u, self.e)
        self.matrix[2, 3] = -np.dot(self.w, self.e)

    def cant(self, angle):
        # rotate the camera's coordinate system about w; updates u and v
        m_rotate = wf.create_rotation_matrix(self.w, angle)

        self.u = (m_rotate @ np.append(self.u, 1))[:3]
        self.v = (m_rotate @ np.append(self.v, 1))[:3]

        # update the 1st and 2nd row of the camera transformation because only the u and v axes changed.
        self.matrix[0, 0] = self.u[0];  self.matrix[0, 1] = self.u[1];  self.matrix[0, 2] = self.u[2]
        self.matrix[1, 0] = self.v[0];  self.matrix[1, 1] = self.v[1];  self.matrix[1, 2] = self.v[2]

        # update the translate values of tx and ty
        self.matrix[0, 3] = -np.dot(self.u, self.e)
        self.matrix[1, 3] = -np.dot(self.v, self.e)