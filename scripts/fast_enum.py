"""
Script for the explicit enumeration of unique Br/I configurations
(up to symmetry) on a finite set of sites, given a list of symmetry operations.

This module:
- Efficiently enumerates all possible I arrangements with k I atoms on N sites,
  avoiding redundant work by canonicalizing each configuration under the symmetry group.
- Uses bitwise encoding (integers as bitvectors) for each configuration,
  making permutation and comparison fast and memory-light.
- Divides the enumeration across multiple CPU cores for scalability.
- Returns both a dictionary of unique configurations (as canonical bitvectors)
  and their degeneracies (the number of symmetry-equivalent arrangements).

Limitations:
- Only feasible (timewise) for cases where total combinations (N choose k) is moderate (up to enum_max).
- For large systems, use Burnside's lemma instead (see burnside.py).
"""

import multiprocessing as mp
from math import comb
from itertools import islice, combinations

def chunk_indices(total, n_chunks):
    """
    Divides a total number of items into n_chunks nearly equal pieces.

    Yields:
        (start, stop) pairs giving the slice indices for each chunk.
    """
    chunk = total // n_chunks
    for i in range(n_chunks):
        start = i * chunk
        stop  = (i + 1) * chunk if i < n_chunks - 1 else total
        yield (start, stop)

def _apply_perm_bits(bitvec: int, perm: tuple[int, ...]) -> int:
    """
    Applies a permutation to a bitvector.

    Parameters:
        bitvec: Integer representing the configuration (bits set = Br sites).
        perm:   Tuple mapping output positions to input positions.
    
    Returns:
        Integer representing the permuted bitvector.
    """
    out = 0
    for i, j in enumerate(perm):
        if (bitvec >> j) & 1:        # Check if Br at position j in input
            out |= (1 << i)          # Set Br at position i in output
    return out

def _canonical_int(bitvec: int, perms: list[tuple[int, ...]]) -> int:
    """
    Computes the canonical (minimum) bitvector under all group operations.

    Parameters:
        bitvec: Integer representing a configuration.
        perms:  List of group permutations (as tuples).

    Returns:
        Smallest integer corresponding to any symmetry-related image.
    """
    m = bitvec
    for p in perms:
        m = min(m, _apply_perm_bits(bitvec, p))
    return m

def _worker(task):
    """
    Worker function for parallel enumeration.

    Parameters:
        task: (start, stop, k, N, perm_tuples)
              start, stop: slice of combinations to enumerate.
              k: number of Br atoms.
              N: number of sites.
              perm_tuples: list of symmetry permutations.

    Returns:
        Dictionary mapping canonical bitvector (int) to degeneracy (int).
    """
    start, stop, k, N, perm_tuples = task
    seen = {}
    # Use islice to enumerate just the slice [start, stop) of combinations
    for combi in islice(combinations(range(N), k), start, stop):
        bitvec = 0
        for idx in combi:
            bitvec |= 1 << idx
        canon = _canonical_int(bitvec, perm_tuples)
        seen[canon] = seen.get(canon, 0) + 1
    return seen

def enumerate_unique(N, k, permutations, enum_max=30_000_000):
    """
    Enumerate all unique (up to symmetry) Br/I configurations for k I on N sites.

    Parameters:
        N:           Number of sites.
        k:           Number of I atoms.
        permutations: List of symmetry permutations (as lists/tuples of indices).
        enum_max:    Maximum allowed total combinations before switching to fallback.

    Returns:
        (degeneracy_dict, total_combinations)
          - degeneracy_dict: {canonical_bitvector (int): degeneracy (int)}
          - total_combinations: Total number of configurations (N choose k)
        If total combinations > enum_max, returns (None, total_combinations).
    """
    total = comb(N, k)
    nprocs = mp.cpu_count()
    chunks = list(chunk_indices(total, nprocs))
    if total > enum_max:
        return None, total         

    # Store each permutation as a tuple of indices
    perm_tuples = [tuple(p) for p in permutations]

    tasks  = [(start, stop, k, N, perm_tuples) for start, stop in chunks]
    with mp.Pool() as pool:
        parts = pool.map(_worker, tasks)

    # Merge dictionaries from all processes
    merged = {}
    for d in parts:
        for k_, v_ in d.items():
            merged[k_] = merged.get(k_, 0) + v_
    return merged, total
