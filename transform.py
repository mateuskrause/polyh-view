import numpy as np

def create_translation(pos):
    T = np.zeros((4, 4))

    T[0, 0] = 1; T[0, 1] = 0; T[0, 2] = 0; T[0, 3] = pos[0]
    T[1, 0] = 0; T[1, 1] = 1; T[1, 2] = 0; T[1, 3] = pos[1]
    T[2, 0] = 0; T[2, 1] = 0; T[2, 2] = 1; T[2, 3] = pos[2]
    T[3, 0] = 0; T[3, 1] = 0; T[3, 2] = 0; T[3, 3] = 1

    return T

def create_camera(u, v, w, e):
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

def create_orthographic(screen_width, screen_height, left, right, bottom, top, near, far):
    M = np.zeros((4, 4))
    M_vp = np.zeros((4, 4))
    M_orth = np.zeros((4, 4))
    
    # verify possible division by zero
    if left == right or bottom == top or near == far:
        print("invalid create_orthographic parameters")
        return np.identity(4)
    
    # create viewport matrix
    m_vp_00 = screen_width / 2
    m_vp_11 = screen_height / 2
    m_vp_03 = (screen_width - 1) / 2
    m_vp_13 = (screen_height - 1) / 2

    M_vp[0, 0] = m_vp_00; M_vp[0, 1] = 0      ; M_vp[0, 2] = 0; M_vp[0, 3] = m_vp_03
    M_vp[1, 0] = 0      ; M_vp[1, 1] = m_vp_11; M_vp[1, 2] = 0; M_vp[1, 3] = m_vp_13
    M_vp[2, 0] = 0      ; M_vp[2, 1] = 0      ; M_vp[2, 2] = 1; M_vp[2, 3] = 0
    M_vp[3, 0] = 0      ; M_vp[3, 1] = 0      ; M_vp[3, 2] = 0; M_vp[3, 3] = 1
    
    # create orthographic projection matrix
    m_orth_00 = 2 / (right - left)
    m_orth_11 = 2 / (top - bottom)
    m_orth_22 = 2 / (near - far)
    m_orth_03 = - (right + left) / (right - left)
    m_orth_13 = - (top + bottom) / (top - bottom)
    m_orth_23 = - (near + far) / (near - far)

    M_orth[0, 0] = m_orth_00; M_orth[0, 1] = 0        ; M_orth[0, 2] = 0        ; M_orth[0, 3] = m_orth_03
    M_orth[1, 0] = 0        ; M_orth[1, 1] = m_orth_11; M_orth[1, 2] = 0        ; M_orth[1, 3] = m_orth_13
    M_orth[2, 0] = 0        ; M_orth[2, 1] = 0        ; M_orth[2, 2] = m_orth_22; M_orth[2, 3] = m_orth_23
    M_orth[3, 0] = 0        ; M_orth[3, 1] = 0        ; M_orth[3, 2] = 0        ; M_orth[3, 3] = 1

    # construct M matrix
    M = M_vp @ M_orth
    
    return M

def create_perspective(screen_width, screen_height, left, right, bottom, top, near, far):
    M_vp_ortho = create_orthographic(screen_width, screen_height, left, right, bottom, top, near, far)

    P = np.zeros((4, 4))
    M = np.zeros((4, 4))

    # define the perspective matrix
    P[0, 0] = near; P[0, 1] = 0   ; P[0, 2] = 0         ; P[0, 3] = 0
    P[1, 0] = 0   ; P[1, 1] = near; P[1, 2] = 0         ; P[1, 3] = 0
    P[2, 0] = 0   ; P[2, 1] = 0   ; P[2, 2] = near + far; P[2, 3] = -far * near
    P[3, 0] = 0   ; P[3, 1] = 0   ; P[3, 2] = 1         ; P[3, 3] = 0

    M = M_vp_ortho @ P

    return M