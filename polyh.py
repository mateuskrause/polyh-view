import wireframe as wf
import re

def parse_polyhedron(filename, scale=15):
    with open(filename, 'r') as file:
        lines = file.readlines()

    if not lines:
        raise ValueError("The file is empty")

    # first line containe the polyhedron name
    polyhedron_name = lines[0].strip()

    variables = {}
    vertices = []
    edges = []
    faces = []

    # define regular expressions to parse the file (maybe something wrong)
    var_pattern = re.compile(r'(C\w+)\s*=\s*([0-9.eE\+\-]+)')
    vertex_pattern = re.compile(r'V(\d+)\s*=\s*\(\s*([^,\)]+),\s*([^,\)]+),\s*([^,\)]+)\s*\)')
    edge_pattern = re.compile(r'\{(.+?)\}')

    # scan the file line by line
    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line: 
            continue
        
        # parse variables
        var_match = var_pattern.match(line)
        if var_match:
            var_name, value = var_match.groups()
            variables[var_name] = float(value)  # Store the value
            continue
  
        # parse vertices
        vertex_match = vertex_pattern.match(line)
        if vertex_match:
            index, x, y, z = vertex_match.groups()
            # Replace any variable with its value and scale the coordinates
            x = scale * eval(x, {}, variables)
            y = scale * eval(y, {}, variables)
            z = scale * eval(z, {}, variables)
            vertices.append(wf.Point(x, y, z, 1))
            continue 

        # parse edges
        edge_match = edge_pattern.match(line)
        if edge_match:
            edge_indices = list(map(int, edge_match.group(1).split(',')))
            # print(edge_indices)
            edges.append(edge_indices)
            
            for i in range(len(edge_indices)):
                p1 = edge_indices[i]
                p2 = edge_indices[(i + 1) % len(edge_indices)]
                face_edges = [wf.Edge(vertices[p1], vertices[p2])]
                faces.append(wf.Face(face_edges))

    # create polyhedron and add edges
    polyhedron = wf.Wireframe()
    polyhedron.name = polyhedron_name

    for edge in edges:
        for i in range(len(edge)):
            p1 = vertices[edge[i]]
            p2 = vertices[edge[(i + 1) % len(edge)]]
            polyhedron.add_edge(p1, p2)

    for face in faces:
        polyhedron.add_face(face)
    
    # Print all polyhedron faces
    # for face in faces:
    #     print("Face with edges:")
    #     for edge in face.edges:
    #         print(f"Edge from {edge.p1.coords} to {edge.p2.coords}")

    return polyhedron