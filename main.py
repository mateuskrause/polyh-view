import pygame
import numpy as np
import os

import wireframe as wf
import camera as cam
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
M_cam = cam.Camera()

# setup view volume for perspective
fovy = 75
near = -1
far = -201

# convert perspective variables to planes
top = near * np.tan(np.radians(fovy) / 2)
bottom = -top
right = top * (SCREEN_WIDTH / SCREEN_HEIGHT)
left = -right
ortho_const = (far - near) / 2.6 # trying to guess to match the perspective view

# create projection matrix
p_matrix_ortho = transform.create_orthographic(SCREEN_WIDTH, SCREEN_HEIGHT, ortho_const, -ortho_const, ortho_const, -ortho_const, near, far)
p_matrix_persp = transform.create_perspective(SCREEN_WIDTH, SCREEN_HEIGHT, left, right, bottom, top, near, far)
p_matrix = p_matrix_persp

# create wireframe
object = wf.Wireframe()
object_world_pos = np.array([0, 0, (far - near) / 2, 1]) # move to object to the center of the view

# load polyhedra files
polyhedra_dir = "polyhedra"
polyhedra_files = [
    f for f in os.listdir(polyhedra_dir) 
    if os.path.isfile(os.path.join(polyhedra_dir, f))
]

# select a polyhedron to start
selected_file = polyhedra_files[2]  # You can change this to select a different file
object = polyh.parse_polyhedron(os.path.join(polyhedra_dir, selected_file))
print(object.name)

# variable to handle the delay between key presses
last_key_press_time = 0

# first rotation
object.rotate(10, 10, 0)

# input actions
def handle_perspective_change(keys):
    global p_matrix

    if keys[pygame.K_p] and not np.array_equal(p_matrix, p_matrix_persp):
        p_matrix = p_matrix_persp
        print("perspective")
    elif keys[pygame.K_o] and not np.array_equal(p_matrix, p_matrix_ortho):
        p_matrix = p_matrix_ortho
        print("orthographic")

def handle_camera_movement(keys):
    global p_matrix

    if keys[pygame.K_w]:
        M_cam.translate(np.array([0, 0, -1, 1]))     
    elif keys[pygame.K_s]:
        M_cam.translate(np.array([0, 0, 1, 1]))
    elif keys[pygame.K_a]:
        M_cam.translate(np.array([-1, 0, 0, 1]))
    elif keys[pygame.K_d]:
        M_cam.translate(np.array([1, 0, 0, 1]))
    elif keys[pygame.K_q]:
        M_cam.translate(np.array([0, -1, 0, 1]))
    elif keys[pygame.K_e]:
        M_cam.translate(np.array([0, 1, 0, 1]))
    elif keys[pygame.K_LEFT]:
        M_cam.rotate(0, 1, 0)
    elif keys[pygame.K_RIGHT]:
        M_cam.rotate(0, -1, 0)
    elif keys[pygame.K_UP]:
        M_cam.rotate(1, 0, 0)
    elif keys[pygame.K_DOWN]:
        M_cam.rotate(-1, 0, 0)

def handle_polyhedron_change(keys):
    global object, selected_file, last_key_press_time

    current_time = pygame.time.get_ticks()
    delay = 200  # milliseconds

    if current_time - last_key_press_time > delay:
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            current_index = polyhedra_files.index(selected_file)
            next_index = (current_index + 1) % len(polyhedra_files)

            selected_file = polyhedra_files[next_index]
            object = polyh.parse_polyhedron(os.path.join(polyhedra_dir, selected_file))
            print(f"Loaded \"{object.name}\"")

            last_key_press_time = current_time

        elif keys[pygame.K_MINUS]:
            current_index = polyhedra_files.index(selected_file)
            prev_index = (current_index - 1) % len(polyhedra_files)

            selected_file = polyhedra_files[prev_index]
            object = polyh.parse_polyhedron(os.path.join(polyhedra_dir, selected_file))
            print(f"Loaded \"{object.name}\"")

            last_key_press_time = current_time

print("Move the camera with W, A, S, D, Q, E and change perspective with P, O. Press + and - to cycle through polyhedra.")

# main loop
while running:
    # poll for events
    keys = pygame.key.get_pressed()

    handle_perspective_change(keys)
    handle_camera_movement(keys)
    handle_polyhedron_change(keys)

    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # actions
    # object.rotate(0, 1, 0)

    # get object translation matrix for the world space
    T_object = transform.create_translation(object_world_pos)

    # define matrix for the camera
    M = p_matrix @ M_cam.matrix

    # render object
    for edge in object.edges:
        p1 = edge.p1.coords
        p2 = edge.p2.coords

        # apply world translation
        p1 = T_object @ p1
        p2 = T_object @ p2

        # apply projection
        p1_proj = M @ p1
        p2_proj = M @ p2

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