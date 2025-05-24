"""
Utility functions for generating permutation mappings induced by symmetry operations
on atomic coordinates.
"""

import numpy as np
import sym_operations as sym


# Find the permutation corresponding to a symmetry operation
def find_permutation(original_coords, transformed_coords):
    """
    Given two coordinate lists, returns a list mapping each transformed coordinate
    to its index in the original coordinate list (i.e., the permutation applied).

    Args:
        original_coords (list): List of original coordinates.
        transformed_coords (list): Coordinates after symmetry operation.

    Returns:
        permutation (list): List of indices representing the permutation.
    """
    permutation = []
    for point in transformed_coords:
        for i, orig_point in enumerate(original_coords):
            if np.allclose(point, orig_point):
                permutation.append(i)
                break
    return permutation

# functions that returns all the permutations for a given group
def find_all_permutations(group_operations, coordinates):
    """
    For each symmetry operation, computes the permutation induced on coordinates.

    Args:
        group_operations (dict): Dict of {operation_name: operation_matrix}.
        coordinates (list): Atomic coordinates.

    Returns:
        permutations (dict): Dict of {operation_name: permutation_list}.
    """
    permutations = {}
    for name, operation in group_operations.items():
        transformed_coords = sym.apply_symmetry_operation(operation, coordinates)
        permutation = find_permutation(coordinates, transformed_coords)
        permutations[name] = permutation

    return permutations
