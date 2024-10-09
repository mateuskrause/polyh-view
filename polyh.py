import wireframe as wf

def calculate_octahedron_vertices(s):
    octahedron = wf.Wireframe()

    octahedron.add_edge(wf.Point(s, 0, s, 1), wf.Point(-s, 0, s, 1))
    octahedron.add_edge(wf.Point(-s, 0, s, 1), wf.Point(-s, 0, -s, 1))
    octahedron.add_edge(wf.Point(-s, 0, -s, 1), wf.Point(s, 0, -s, 1))
    octahedron.add_edge(wf.Point(s, 0, -s, 1), wf.Point(s, 0, s, 1))

    octahedron.add_edge(wf.Point(s, 0, s, 1), wf.Point(0, 2*s, 0, 1))
    octahedron.add_edge(wf.Point(-s, 0, s, 1), wf.Point(0, 2*s, 0, 1))
    octahedron.add_edge(wf.Point(-s, 0, -s, 1), wf.Point(0, 2*s, 0, 1))
    octahedron.add_edge(wf.Point(s, 0, -s, 1), wf.Point(0, 2*s, 0, 1))

    octahedron.add_edge(wf.Point(s, 0, s, 1), wf.Point(0, -2*s, 0, 1))
    octahedron.add_edge(wf.Point(-s, 0, s, 1), wf.Point(0, -2*s, 0, 1))
    octahedron.add_edge(wf.Point(-s, 0, -s, 1), wf.Point(0, -2*s, 0, 1))
    octahedron.add_edge(wf.Point(s, 0, -s, 1), wf.Point(0, -2*s, 0, 1))

    return octahedron

def calculate_cube_vertices(s):
    cube = wf.Wireframe()

    cube.add_edge(wf.Point(s, s, -s, 1), wf.Point(-s, s, -s, 1))
    cube.add_edge(wf.Point(-s, s, -s, 1), wf.Point(-s, -s, -s, 1))
    cube.add_edge(wf.Point(-s, -s, -s, 1), wf.Point(s, -s, -s, 1))
    cube.add_edge(wf.Point(s, -s, -s, 1), wf.Point(s, s, -s, 1))

    cube.add_edge(wf.Point(s, s, s, 1), wf.Point(-s, s, s, 1))
    cube.add_edge(wf.Point(-s, s, s, 1), wf.Point(-s, -s, s, 1))
    cube.add_edge(wf.Point(-s, -s, s, 1), wf.Point(s, -s, s, 1))
    cube.add_edge(wf.Point(s, -s, s, 1), wf.Point(s, s, s, 1))

    cube.add_edge(wf.Point(s, s, s, 1), wf.Point(s, s, -s, 1))
    cube.add_edge(wf.Point(-s, s, s, 1), wf.Point(-s, s, -s, 1))
    cube.add_edge(wf.Point(-s, -s, s, 1), wf.Point(-s, -s, -s, 1))
    cube.add_edge(wf.Point(s, -s, s, 1), wf.Point(s, -s, -s, 1))

    return cube

def calculate_unit_square_vertices(s):
    unit_square = wf.Wireframe()

    unit_square.add_edge(wf.Point(s, 0, 0, 1), wf.Point(s, s, 0, 1))
    unit_square.add_edge(wf.Point(s, s, 0, 1), wf.Point(0, s, 0, 1))
    unit_square.add_edge(wf.Point(0, s, 0, 1), wf.Point(-s, s, 0, 1))
    unit_square.add_edge(wf.Point(-s, s, 0, 1), wf.Point(-s, 0, 0, 1))
    unit_square.add_edge(wf.Point(-s, 0, 0, 1), wf.Point(-s, -s, 0, 1))
    unit_square.add_edge(wf.Point(-s, -s, 0, 1), wf.Point(0, -s, 0, 1))
    unit_square.add_edge(wf.Point(0, -s, 0, 1), wf.Point(s, -s, 0, 1))
    unit_square.add_edge(wf.Point(s, -s, 0, 1), wf.Point(s, 0, 0, 1))

    unit_square.add_edge(wf.Point(0, 0, 0, 1), wf.Point(s, 0, 0, 1))
    unit_square.add_edge(wf.Point(0, 0, 0, 1), wf.Point(0, s, 0, 1))
    unit_square.add_edge(wf.Point(0, 0, 0, 1), wf.Point(-s, 0, 0, 1))
    unit_square.add_edge(wf.Point(0, 0, 0, 1), wf.Point(0, -s, 0, 1))

    return unit_square