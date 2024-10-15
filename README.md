# polyh-view

![Screenshot from 2024-10-09 00-14-49](https://github.com/user-attachments/assets/e52cf4fc-bda4-4bdf-9adb-13e0f651d7d4)

This python project implements a 3D polyhedron wireframe viewer using Pygame, but the main focus is to understant the representation of 3D objects and how it can be viewed as a 2D image using matrix transformations to express parallel and perspective views. We archieved this projecting 3D points in the _world space_ to 2D point in the _image space_ - which is good for producing _wireframe_ renderings (where only the edges of the object are draw).

## Run

To run the viewer just execute the `main.py` file. Make sure you have [PyGame](https://www.pygame.org) and [NumPy](https://numpy.org/) installed.
```
python main.py
```

## Behind the Scenes

To create a 3D wireframe representation of a polyhedron, besides the need of a data structure to represent the object (vertices and edges), we need to map the 3D locations (coordinates _x_, _y_ and _z_ in the canonical coordinate system) onto the screen (represented in pixels). This can be fully represented as matrix multiplication, thanks to [projective geometry](https://en.wikipedia.org/wiki/Projective_geometry) and its propeties.

### Viewing Transformation

This mapping is known as the viewing transformation and depends on several factors, including the camera's position and orientation, type of projection, field of view, and resolution of the image. We can break this process into a sequence of simpler transformations:

- _Camera transformation_: A rigid-body transformation that adjusts the view for the camera position (with the default camera located at the origin, looking in the -z direction).
- _Projection transformation_: Projects points from _camera space_ so that all visible points are mapped to the unit image rectangle (ranging from -1 to 1 in both $x$ and $y$).
- _Viewport transformation_: Maps this unit rectangle to the desired screen rectangle (e.g. the window's resolution in pixel coordinates).

The entire process can be summarized as follows:

![birds_camera](https://github.com/user-attachments/assets/09d54a5f-c4fd-47fe-96aa-d7242921a57b)

Objects initially exist in _object space_, where local rigid-body transformations like rotation and scaling are applied. The object is then placed into _world space_, which represents the scene (in this case, a simple translation from the origin). The camera transformation converts the points into _camera space_ (camera coordinates), after which the projection maps the points to the _canonical view volume_. Finally, the viewport transformation maps the canonical view to _screen space_.

#### Viewport Transformation

We assume that the geometry we want to view is in the canonical view volume, a 3D cube with sides of length 2, centered at the origin (i.e. $(x, y, z) \in [-1,1]^3$), with the default camera looking in the $-z$ direction. In this setup, the point _x = -1_ is projected to the left side of the screen, _x = +1_ to the right side of the screen, _y = -1_ to the bottom side of the screen, and _y = +1_ to the top side of the screen.

Given a screen with dimensions $n_x$ by $n_y$ pixels, the goal is to map the coordinates $[-1,1]^2$ to the screen space $[-0.5, n_x - 0.5] \times [-0.5, n_y - 0.5]$. We follow the convention that pixels are centered on integer coordinates, with a 0.5 offset.

This transformation maps one axis-aligned rectangle to another, and can be represented as:

$$
\begin{bmatrix}
x_{\text{screen}} \\
y_{\text{screen}} \\
1
\end{bmatrix} = 
\begin{bmatrix}
\frac{n_x}{2} & 0             & \frac{n_x - 1}{2} \\
0             & \frac{n_y}{2} & \frac{n_y - 1}{2} \\
0             & 0             & 1
\end{bmatrix}
\begin{bmatrix}
x_{\text{canonical}} \\
y_{\text{canonical}} \\
1
\end{bmatrix}
$$

This representation ignores the $z$-coordinate since depth information does not affect where the point will be projected on screen. However, in our final matrix we add a row to copy the $z$ coordinate, as it can be useful for operations like [depth sorting](https://en.wikipedia.org/wiki/Painter's_algorithm) (where nearer surfaces hide farther ones). The final viewport transformation matrix becomes:

$$
M_{\text{vp}} = 
\begin{bmatrix}
\frac{n_x}{2} & 0             & 0 & \frac{n_x - 1}{2} \\
0             & \frac{n_y}{2} & 0 & \frac{n_y - 1}{2} \\
0             & 0             & 1 & 0 \\
0             & 0             & 0 & 1
\end{bmatrix}
$$

Note the use of [homogeneous coordinates](https://en.wikipedia.org/wiki/Homogeneous_coordinates) as we are dealing with transformations on the [projective space](https://en.wikipedia.org/wiki/Projective_space).

#### Projection Transformation

It is often convenient to render geometry in some region of space other than the canonical view volume. To generalize the view, we keep the idea of the view direction looking along $-z$ axis with $+y$ pointing up, but allow for arbitrary rectangular regions (or frustums) to be projected. Instead of replacing the viewport matrix, we apply another matrix by multiplying on the right to get the effect.

##### Orthographic Projection

The goal of orthographic projection is to arrange points so that when projected onto the screen, parallel lines remain parallel. This type of projection applies to any arbitrary rectangular view volume, defined by the coordinates of its sides, such that the view volume is $[l,r] \times [b, t] \times [f, n]$. This is called the orthographic view box, and we refer to the bounding planes as follows:

- $x = l$ (left plane),
- $x = r$ (right plane),
- $y = b$ (bottom plane),
- $y = t$ (top plane),
- $z = n$ (near plane),
- $z = f$ (far plane).

The near plane is closer to the camera than the far plane, so it must have the relation $n > f$

![ortho_view_volume](https://github.com/user-attachments/assets/01b0ec15-eb0f-44fd-8af5-6699d3f38fc8)

Transforming from the orthographic view volume to the canonical view volume requires a scaling and translation transformation, which can be represented as:

$$
M_{\text{orth}} = 
\begin{bmatrix}
\frac{2}{r-l} & 0             & 0             & -\frac{r+l}{r-l} \\
0             & \frac{2}{t-b} & 0             & -\frac{t+b}{t-b} \\
0             & 0             & \frac{2}{n-f} & -\frac{n+f}{n-f} \\
0             & 0             & 0             & 1
\end{bmatrix}
$$

To draw 3D line segments in the orthographic view volume, we project the vertices points to the screen by ignoring the $z$-coordinate. This can be done by combining the orthographic and viewport transformation:

$$
\begin{bmatrix}
x_{\text{pixel}} \\
y_{\text{pixel}} \\
z_{\text{canonical}} \\
0
\end{bmatrix} = 
(M_{\text{vp}} M_{\text{orth}})
\begin{bmatrix}
x \\
y \\
z \\
1
\end{bmatrix}
$$

A simple code to render a polyhedron wireframe can be written as:

```
construct M_vp
construct M_orth
M = M_vp M_orth
for each edge (a_i, b_i) do
  p = M a_i
  q = M b_i
  drawline(x_p, y_p, x_q, y_q)
```

##### Perspective Projection

In perspective projection, objects that are farther from the camera appear smaller, following an inverse relationship with depth. We assume the camera is positioned at the origin $e$, and the gaze direction $g$ is along the $-z$-axis. The size of an object on screen is proportional to $1/z$, as described by:

$$
y_s = \frac{d}{z}y
$$

where $y_s$​ is the size on the screen, $d$ is the distance from the camera, and $z$ is the depth of the object in the camera's view.

![persp_view](https://github.com/user-attachments/assets/91c102f4-b10f-4096-a7cd-a74f1f33e173)

To represent perspective projection as a matrix transformation, we use homogeneous coordinates (where a point can be represented in infinitely many ways). Modifying the $w$-coordinate by a component proportional to $z$, we ensure that the final step of the transformation involves normalizing the screen coordinates, dividing $x, y$ and $z$ by this distance factor $w$. The resulting perspective projection matrix is:

$$
\begin{bmatrix}
x_s \\
0
\end{bmatrix} \sim
\begin{bmatrix}
d & 0 & 0 \\
0 & 1 & 0
\end{bmatrix}
\begin{bmatrix}
y \\
z \\
1
\end{bmatrix}
$$

With this approach, we can build the perspective projection matrix in 3D, considering a default camera position. Since we typically define near and far planes along the negative $z$-axis, we use a near plane distance of $-n$. The perspective projection matrix for all coordinates can be described as:

$$
P = \begin{bmatrix}
n & 0 & 0 & 0 \\
0 & n & 0 & 0 \\
0 & 0 & n+f & -fn \\
0 & 0 & 1 & 0
\end{bmatrix}
$$

This perspective projection leaves points on $z = n$ plane unchanged and maps the larger $z = f$ rectangle in the back to a smaller rectangle within the orthographic volume.

![persp_proj](https://github.com/user-attachments/assets/a9ef33c7-b335-416c-ae33-69f58bd29709)

The praticality of this approach is that once we apply perspective, we can use the same orthographic projection matrix to map the result to the canonical view volume. The final perspective projection matrix is obtained by combining these two transformations:

$$
M_{\text{per}} = M_{\text{orth}} P
$$

To set values for $l, r, b$ and $t$, we can specify them on the plane $z=n$ since the perspective matrix does not change the values on that plane. The complete code can be thought as:

```
construct M_vp
construct M_per
M = M_vp M_per
for each edge (a_i, b_i) do
  p = M a_i
  q = M b_i
  drawline(x_p/w_p, y_p/w_p, x_q/w_p, y_q/w_p)
```

###### Field of View

An important consideration when constructing projection matrices is how to select appropriate values for $l, r, b$ and $t$  to achieve the desired field of view (FOV). Specifically, the vertical FOV (fovy) is the angle between the top and bottom of the view, measured from the eye point $e$ to the near plane.

To calculate these values, we can use the screen's aspect ratio (the ratio of width to height) and the angle $\theta$ (the field of view in the y-axis). The near and far planes follow the same rules as in the previous projection.

![fovy](https://github.com/user-attachments/assets/2b7c1c42-9263-4c83-b542-f29c58e9e844)

From the figure, we can calculate the boundaries of the viewing frustum based on the fovy angle $\theta$ and the aspect ratio $\text{width}/\text{height}$

$$
\begin{align*}
  \text{top} &= \text{near} \cdot \tan{(\theta/2)} \\
  \text{bottom} &= -\text{top} \\
  \text{right} &= \text{top} \cdot (\text{width} / \text{height}) \\
  \text{left} &= -\text{right}
\end{align*}
$$

##### Camera Transformation

It would be good to render a 3D scene from different viewpoints, so we need to define the camera's position and orientation in space. We specify the viewer’s position and orientation using the following convention specifying the vectors:

- _Eye position_ $e$: The position of the camera or the center of the viewer’s eye,
- _Gaze direction_ $g$: The direction the viewer is looking at,
- _View-up vector_ $t$: A vector that defines the "up" direction for the viewer. It points upward, bisecting the viewer’s field of view into right and left halves.

To define the viewing transformation, the user specifies viewing with $e, g$ and $t$. From these, we construct a right-handed coordinate system basis with $w$ pointing opposite to the gaze and $v$ being in the same plane as $g$ and $t$.
  
![camera_vectors](https://github.com/user-attachments/assets/5107bc3d-b4ef-4bd7-87f1-c0e1f847c674)

With these vectors, we can build a coordinate system with origin $e$ and a basis defined by three orthogonal vectors $u, v$ and $w$, allowing us to transform from world space to the camera's space: 

$$
\begin{align*}
w &= -\frac{g}{||g||}, \\
u &= \frac{t \times w}{||t \times w||}, \\
v &= w \times u
\end{align*}
$$

To handle arbitrary viewing directions, we need to change the points for a appropriated coordinated system.

![camera_position](https://github.com/user-attachments/assets/aab0a89b-04a6-4c97-b421-157ef5e22f2c)

To transform the coordinates between this spaces, we apply a transformation matrix that change it basis to one with $u, v$ and $w$ as basis vectors. This can be done by the following rotation and a translation:

$$
M_{\text{cam}} = \begin{bmatrix}
x_u & y_u & z_u & 0 \\
x_v & y_v & z_v & 0 \\
x_w & y_w & z_w & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
1 & 0 & 0 & -x_e \\
0 & 1 & 0 & -y_e \\
0 & 0 & 1 & -z_e \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

To use this camera transformation in the rendering pipeline (which previously assumed a fixed origin looking down the $-z$-axis), we combine the camera transformation matrix $M_{cam}$​ with the viewport and projection matrices. Using the perspective projection as example:

```
construct M_vp
construct M_per
construct M_cam
M = M_vp M_per M_cam
for each edge (a_i, b_i) do
  p = M a_i
  q = M b_i
  drawline(x_p/w_p, y_p/w_p, x_q/w_p, y_q/w_p)
```

This matrix $M_{cam}$ allow us to apply camera's position and orientation in addition to the usual transformations.

### References

- Book - Fundamentals of Computer Graphics -  P. Shirley and S. Marschner, Fundamentals of Computer Graphics, 3rd ed. A K Peters, 2009.
- Book - Computer Graphics: Theory and Practice - J. Gomes, L. Velho, and M. Costa Sousa, Computer Graphics: Theory and Practice. CRC Press, 2012.
- Webpages - Learn WebGL:
  - "Perspective projections," Learn WebGL. [Online]. Available: http://learnwebgl.brown37.net/08_projections/projections_perspective.html.
  - "Orthographic projections," Learn WebGL. [Online]. Available: http://learnwebgl.brown37.net/08_projections/projections_ortho.html.
