import numpy as np

### Symmetry operations in 3D space ###

def rotation_matrix(axis, angle_degrees):
    angle_radians = np.radians(angle_degrees)
    axis = np.asarray(axis)
    axis = axis / np.linalg.norm(axis)
    a = np.cos(angle_radians / 2.0)
    b, c, d = -axis * np.sin(angle_radians / 2.0)
    return np.array([
        [a*a + b*b - c*c - d*d, 2*(b*c - a*d), 2*(b*d + a*c)],
        [2*(b*c + a*d), a*a + c*c - b*b - d*d, 2*(c*d - a*b)],
        [2*(b*d - a*c), 2*(c*d + a*b), a*a + d*d - b*b - c*c]
    ])

def reflection_matrix(normal):
    normal = np.asarray(normal)
    normal = normal / np.linalg.norm(normal)
    return np.eye(3) - 2 * np.outer(normal, normal)

def inversion_matrix():
    return -np.eye(3)

def improper_rotation_matrix(axis, angle_degrees):
    rotation = rotation_matrix(axis, angle_degrees)
    reflection = reflection_matrix(axis)
    return np.dot(reflection, rotation)

# Application of symmetry operations to a set of coordinates
def apply_symmetry_operation(operation, coordinates):
    return np.dot(coordinates, operation.T)


### Construction of symmetry operations for a symmmetry group ### (Only D4h is implemented) #TODO: Implement more groups

def D4h_symmetry_operations():
    # D4h group
    # E, C4, C4_-1, C2, C2'(x), C2'(y), C2''(xy), C2''(-xy), i, S4, S4_-1, sigma_h, sigma_v(x), sigma_v'(y), sigma_d(xy), sigma_d'(-xy)
    # E
    E = np.eye(3)
    # C4
    C4 = rotation_matrix([0, 0, 1], 90)
    # C4_-1
    C4_minus_1 = rotation_matrix([0, 0, 1], -90)
    # C2
    C2 = rotation_matrix([0, 0, 1], 180)
    # C2'(x)
    C2_prime = rotation_matrix([1, 0, 0], 180)
    # C2'(y)
    C2_double_prime = rotation_matrix([0, 1, 0], 180)
    # C2''(xy)
    C2_double_prime_xy = rotation_matrix([1, 1, 0], 180)
    # C2''(-xy)
    C2_double_prime_minus_xy = rotation_matrix([1, -1, 0], 180)
    # i
    i = inversion_matrix()
    # S4
    S4 = improper_rotation_matrix([0, 0, 1], 90)
    # S4_-1
    S4_minus_1 = improper_rotation_matrix([0, 0, 1], -90)
    # sigma_h
    sigma_h = reflection_matrix([0, 0, 1])
    # sigma_v(x)
    sigma_v_x = reflection_matrix([0, 1, 0])
    # sigma_v'(y)
    sigma_v_y = reflection_matrix([1, 0, 0])
    # sigma_d(xy)
    sigma_d_xy = reflection_matrix([1, -1, 0])
    # sigma_d'(-xy)
    sigma_d_minus_xy = reflection_matrix([1, 1, 0])
    
    # return a dict with name and matrix
    return {
        'E': E,
        'C4': C4,
        'C4_-1': C4_minus_1,
        'C2': C2,
        'C2\'(x)': C2_prime,
        'C2\'(y)': C2_double_prime,
        'C2\'\'(xy)': C2_double_prime_xy,
        'C2\'\'(-xy)': C2_double_prime_minus_xy,
        'i': i,
        'S4': S4,
        'S4_-1': S4_minus_1,
        'sigma_h': sigma_h,
        'sigma_v(x)': sigma_v_x,
        'sigma_v\'(y)': sigma_v_y,
        'sigma_d(xy)': sigma_d_xy,
        'sigma_d\'(-xy)': sigma_d_minus_xy
    }
    
    
