import numpy as np
import sym_operations as sym


# Find the permutation corresponding to a symmetry operation
def find_permutation(original_coords, transformed_coords):
    permutation = []
    for point in transformed_coords:
        for i, orig_point in enumerate(original_coords):
            if np.allclose(point, orig_point):
                permutation.append(i)
                break
    return permutation

# functions that returns all the permutations for a given group
def find_all_permutations(group_operations, coordinates):
    permutations = {}
    for name, operation in group_operations.items():
        transformed_coords = sym.apply_symmetry_operation(operation, coordinates)
        permutation = find_permutation(coordinates, transformed_coords)
        permutations[name] = permutation

    return permutations
