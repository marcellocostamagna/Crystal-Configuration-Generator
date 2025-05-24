"""
Script to enumerate unique configurations of Br/I for selected 'coordination spheres'.
"""

import time
import sym_operations as sym
import define_permutations as pr
import visualize as vis
from fast_enum import enumerate_unique
from burnside import burnside_count, prepare_cycle_cache 
import argparse

############################
# === COORDINATE LIBRARIES
############################
coordinates_first_sphere = [
    [0, 0, 2],
    [1, 0, 1], [0, -1, 1], [-1, 0, 1], [0, 1, 1],
    [1, 0, -1], [0, -1, -1], [-1, 0, -1], [0, 1, -1],
    [0, 0, -2], [2, 0, 0], [-2, 0, 0], [0, 2, 0], [0, -2, 0],
]

coordinates_second_sphere = [
    [0, 0, 2], [1, 0, 1], [0, -1, 1], [-1, 0, 1], [0, 1, 1],
    [1, 0, -1], [0, -1, -1], [-1, 0, -1], [0, 1, -1], [0, 0, -2],
    [2, 0, 0], [2, 0, 2], [3, 0, 1], [2, -1, 1], [2, 1, 1],
    [3, 0, -1], [2, -1, -1], [2, 1, -1], [2, 0, -2],
    [0, 2, 0], [0, 2, 2], [1, 2, 1], [-1, 2, 1], [0, 3, 1],
    [1, 2, -1], [-1, 2, -1], [0, 3, -1], [0, 2, -2],
    [-2, 0, 0], [-2, 0, 2], [-3, 0, 1], [-2, -1, 1], [-2, 1, 1],
    [-3, 0, -1], [-2, -1, -1], [-2, 1, -1], [-2, 0, -2],
    [0, -2, 0], [0, -2, 2], [1, -2, 1], [-1, -2, 1], [0, -3, 1],
    [1, -2, -1], [-1, -2, -1], [0, -3, -1], [0, -2, -2],
]

coordinates_reduced_sphere = [
    [1, 0, 1], [0, -1, 1], [-1, 0, 1], [0, 1, 1],
    [1, 0, -1], [0, -1, -1], [-1, 0, -1], [0, 1, -1],
]

ENUM_MAX = 30_000_000  # switch to Burnside above this many total configs

def get_unique_configs(n_br, coords, perms, enum_max=ENUM_MAX, sphere=1):
    """
    Enumerate unique configurations for placing `n_br` Br atoms among the given coordinates,
    using symmetry operations specified by `perms`.

    Tries direct enumeration if the total number of configurations is less than `enum_max`.
    If the enumeration would be too large, uses Burnside's lemma for counting only.

    Parameters
    ----------
    n_br : int
        Number of Br atoms to place.
    coords : list of lists
        List of coordinate positions (for all sites).
    perms : list of lists
        List of permutations (symmetry operations).
    enum_max : int, optional
        Maximum number of configurations for explicit enumeration (default: 30,000,000).
    sphere : int, optional
        Sphere identifier, used for Burnside cache (default: 1).

    Returns
    -------
    uniq_dict : dict
        Dictionary mapping canonical configuration to degeneracy, or empty if Burnside's lemma is used.
    n_unique : int
        Number of unique configurations.
    n_total : int
        Total number of possible configurations.
    """
    n_sites = len(coords)
    uniq_dict, n_total = enumerate_unique(n_sites, n_br, perms, enum_max)
    if uniq_dict is None:  
        n_unique = burnside_count(n_sites, n_br, sphere=sphere, perms=perms)
        return {}, n_unique, n_total
    n_unique = len(uniq_dict)
    return uniq_dict, n_unique, n_total

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Enumerate unique Br/I configurations and optionally save as SVG."
    )
    parser.add_argument("--sphere", type=int, default=1, choices=[1,2,3],
                        help="Which sphere to use: 1=first, 2=second, 3=reduced (default: 1)")
    parser.add_argument("--nbr", type=int, default=2, help="Number of Br atoms (default: 2)")
    parser.add_argument("--enum-max", type=int, default=30_000_000,
                        help="Switch to Burnside above this number of configs (default: 30,000,000)")
    parser.add_argument("--save-svg", "-s", action='store_true',
                        help="Save each structure as an SVG in a folder.")

    args = parser.parse_args()

    SPHERE = args.sphere
    N_BR = args.nbr
    ENUM_MAX = args.enum_max

    if SPHERE == 1:
        coordinates = coordinates_first_sphere
    elif SPHERE == 2:
        coordinates = coordinates_second_sphere
    elif SPHERE == 3:
        coordinates = coordinates_reduced_sphere
    else:
        raise ValueError("Sphere must be 1, 2 or 3")

    start = time.time()
    ops   = sym.D4h_symmetry_operations()
    perms = list(pr.find_all_permutations(ops, coordinates).values())

    try:
        _ = burnside_count(len(coordinates), 0, sphere=SPHERE)
    except RuntimeError:
        print(f"Burnside cache for sphere={SPHERE} not found. Creating it now...")
        prepare_cycle_cache(perms, sphere=SPHERE)
        print("...Burnside cache created!")

    deg_dict, n_unique, n_total = get_unique_configs(
        N_BR, coordinates, perms, enum_max=ENUM_MAX, sphere=SPHERE
    )

    elapsed = time.time() - start

    print(f"Br atoms: {N_BR} on {len(coordinates)} sites")
    print(f"Total configurations:  {n_total:,}")
    print(f"Unique configurations: {n_unique:,}")
    print(f"Elapsed time: {elapsed:.2f} s")

    # === Save SVGs if requested and possible ===
    if deg_dict and args.save_svg:
        structures = []
        for idx, (config_int, degeneracy) in enumerate(deg_dict.items()):
            bits = [(config_int >> i) & 1 for i in range(len(coordinates))]
            symbols = ['I'] * (len(coordinates) + 1)
            for i, b in enumerate(bits):
                symbols[i + 1] = 'Br' if b else 'I'
            title = f"Config {idx+1}: deg {degeneracy}"
            full_coords = [[0, 0, 0]] + coordinates
            structures.append((full_coords, symbols, title))

        svg_dir = f"svg_configs_sphere{SPHERE}_Br{N_BR}_I{len(coordinates)-N_BR}"
        prefix = f"Br{N_BR}_I{len(coordinates)-N_BR}"
        vis.save_structures_as_svgs(structures, svg_dir, prefix=prefix)
        print(f"SVG images saved in folder: {svg_dir}")
