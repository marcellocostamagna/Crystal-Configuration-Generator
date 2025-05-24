"""
Script for the efficient calculation of the number of symmetry-unique configurations
using Burnside's lemma.

This module enables to:
  - Precompute and cache the cycle structure of all symmetry operations for a site set.
  - Quickly compute, for any number k of Br atoms, the number of unique configurations
    (i.e., orbits) under symmetry, without explicit enumeration.
  - Autogenerate the cache if missing (with the group permutations provided).

The cache is stored as a pickle file, one per site set (distinguished by `sphere`).
"""

from math import comb
import pickle, pathlib

def get_cache_path(sphere):
    """
    Returns the cache path for a given site set (sphere).
    """
    return pathlib.Path(__file__).with_name(f'burnside.sphere{sphere}.cycles.pkl')

def _cycle_structure_from_permutation(p):
    """
    Given a permutation of N sites (as a list of length N),
    returns the number of cycles in the permutation.

    Example: p = [2,0,1] (0->2, 1->0, 2->1) has one 3-cycle.
    """
    seen = set()
    cycles = 0
    for i in range(len(p)):
        if i in seen:
            continue
        cycles += 1
        j = i
        while p[j] not in seen:
            seen.add(j)
            j = p[j]
    return cycles

def prepare_cycle_cache(permutations, group_order=16, sphere=1):
    """
    Computes the cycle structure of each permutation (symmetry operation)
    and saves it, along with the group order, to a cache file for fast lookup.

    Parameters:
        permutations: List of permutations (each as a list or tuple of site indices).
        group_order:  Order of the symmetry group (number of group elements).
        sphere:       Integer ID for the site set (to distinguish caches).
    """
    cycles = [_cycle_structure_from_permutation(p) for p in permutations]
    cache_path = get_cache_path(sphere)
    with cache_path.open('wb') as f:
        pickle.dump((cycles, group_order), f)

def burnside_count(N, k, sphere=1, perms=None, group_order=16):
    """
    Calculates the number of symmetry-unique ways to place k Br atoms on N sites,
    under the action of a symmetry group, using Burnside's lemma.

    If the cycle cache does not exist for this sphere, and `perms` is given,
    it creates the cache and proceeds.

    Parameters:
        N:      Number of sites (int).
        k:      Number of Br atoms (int).
        sphere: Integer ID for the site set (default 1).
        perms:  List of group permutations (if cache needs to be built).
        group_order: Order of the symmetry group (default 16 for D4h).

    Returns:
        Number of unique configurations (int).

    Raises:
        RuntimeError if cache does not exist and `perms` is not supplied.
    """
    cache_path = get_cache_path(sphere)
    try:
        cycles, gsize = pickle.load(cache_path.open('rb'))
    except FileNotFoundError:
        if perms is None:
            raise RuntimeError(
                f"Burnside cache '{cache_path}' not found and perms not provided to create it."
            )
        # Create the cache and try again
        prepare_cycle_cache(perms, group_order, sphere)
        cycles, gsize = pickle.load(cache_path.open('rb'))
    S = sum(comb(c, k) for c in cycles)
    return S // gsize
