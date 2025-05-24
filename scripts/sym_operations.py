"""
Script for symmetry operations in 3D space and their collection in symmetry groups.
"""

import numpy as np

### Symmetry operations in 3D space ###

def rotation_matrix(axis, angle_degrees):
    """Returns 3x3 rotation matrix for rotation about given axis (unit vector)."""
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
    """Returns reflection matrix across plane with given normal."""
    normal = np.asarray(normal)
    normal = normal / np.linalg.norm(normal)
    return np.eye(3) - 2 * np.outer(normal, normal)

def inversion_matrix():
    """Returns inversion (origin-centered) matrix."""
    return -np.eye(3)

def improper_rotation_matrix(axis, angle_degrees):
    """Returns improper rotation: rotate, then reflect through plane perpendicular to axis."""
    rotation = rotation_matrix(axis, angle_degrees)
    reflection = reflection_matrix(axis)
    return np.dot(reflection, rotation)

# Application of symmetry operations to a set of coordinates
def apply_symmetry_operation(operation, coordinates):
    """Applies symmetry operation matrix to all coordinates (Nx3 array or list)."""
    return np.dot(coordinates, operation.T)


### Symmmetry group ### (Only D4h is currently implemented) 

def D4h_symmetry_operations():
    """Returns dict {name: 3x3 matrix} for D4h symmetry operations."""
    return {
        'E': np.eye(3),
        'C4': rotation_matrix([0,0,1], 90),
        'C4_-1': rotation_matrix([0,0,1], -90),
        'C2': rotation_matrix([0,0,1], 180),
        "C2'(x)": rotation_matrix([1,0,0], 180),
        "C2'(y)": rotation_matrix([0,1,0], 180),
        "C2''(xy)": rotation_matrix([1,1,0], 180),
        "C2''(-xy)": rotation_matrix([1,-1,0], 180),
        'i': inversion_matrix(),
        'S4': improper_rotation_matrix([0,0,1], 90),
        'S4_-1': improper_rotation_matrix([0,0,1], -90),
        'sigma_h': reflection_matrix([0,0,1]),
        "sigma_v(x)": reflection_matrix([0,1,0]),
        "sigma_v'(y)": reflection_matrix([1,0,0]),
        "sigma_d(xy)": reflection_matrix([1,-1,0]),
        "sigma_d'(-xy)": reflection_matrix([1,1,0])
    }
    
# Insert more symmetry groups here as needed
    
