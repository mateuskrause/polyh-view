import pygame
import numpy as np

import wireframe as wf
import transform
import polyh

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# create camera orientation coordinates
u = np.array([1, 0, 0, 1])
v = np.array([0, 1, 0, 1])
w = np.array([0, 0, 1, 1])
e = np.array([0, 0, 0, 1])
M_cam = transform.create_camera(u, v, w, e)

# setup view volume
fovy = 75
near = -1
far = -201

top = near * np.tan(np.radians(fovy) / 2)
bottom = -top
right = top * (SCREEN_WIDTH / SCREEN_HEIGHT)
left = -right
ortho_const = (far - near) / 2.6 # trying to guess to match the perspective view

p_matrix_ortho = transform.create_orthographic(SCREEN_WIDTH, SCREEN_HEIGHT, ortho_const, -ortho_const, ortho_const, -ortho_const, near, far) @ M_cam
p_matrix_persp = transform.create_perspective(SCREEN_WIDTH, SCREEN_HEIGHT, left, right, bottom, top, near, far) @ M_cam
p_matrix = p_matrix_persp

# create wireframe
object = wf.Wireframe()
object_world_pos = np.array([0, 0, (far - near) / 2, 1]) # move to object to the center of the view

object = polyh.calculate_cube_vertices(30)
# object = polyh.calculate_octahedron_vertices(30)
# object = polyh.calculate_unit_square_vertices(30)

object.rotate(10, 10, 0)

# actions using inputs
def handle_perspective_change(keys):
    global p_matrix

    if keys[pygame.K_p] and not np.array_equal(p_matrix, p_matrix_persp):
        p_matrix = p_matrix_persp
        print("perspective")
    elif keys[pygame.K_o] and not np.array_equal(p_matrix, p_matrix_ortho):
        p_matrix = p_matrix_ortho
        print("orthographic")

def handle_camera_movement(keys):
    global p_matrix, u, v, w, e

    T_cam = np.identity(4)

    if keys[pygame.K_w]:
        T_cam = transform.create_translation(np.array([0, 0, -1, 1]))        
    elif keys[pygame.K_s]:
        T_cam = transform.create_translation(np.array([0, 0, 1, 1]))
    elif keys[pygame.K_a]:
        T_cam = transform.create_translation(np.array([-1, 0, 0, 1]))
    elif keys[pygame.K_d]:
        T_cam = transform.create_translation(np.array([1, 0, 0, 1]))
    elif keys[pygame.K_q]:
        T_cam = transform.create_translation(np.array([0, -1, 0, 1]))
    elif keys[pygame.K_e]:
        T_cam = transform.create_translation(np.array([0, 1, 0, 1]))

    M_cam = transform.create_camera(u, v, w, T_cam @ e)
    p_matrix = p_matrix @ M_cam

print("Move the camera with W, A, S, D, Q, E and change perspective with P, O")

# main loop
while running:
    # poll for events
    keys = pygame.key.get_pressed()

    handle_perspective_change(keys)
    handle_camera_movement(keys)

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # actions
    object.rotate(0, 1, 0)

    # get object translation matrix for the world space
    T_object = transform.create_translation(object_world_pos)

    # render object
    for edge in object.edges:
        p1 = edge.p1.coords
        p2 = edge.p2.coords

        # apply world translation
        p1 = T_object @ p1
        p2 = T_object @ p2

        # apply projection
        p1_proj = p_matrix @ p1
        p2_proj = p_matrix @ p2

        # normalize coordinates
        p1_proj = p1_proj / p1_proj[3]
        p2_proj = p2_proj / p2_proj[3]

        # draw a line between the two points
        start_point = (p1_proj[0], p1_proj[1])
        end_point = (p2_proj[0], p2_proj[1])
        pygame.draw.line(screen, BLACK, start_point, end_point, 2)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 30

pygame.quit()