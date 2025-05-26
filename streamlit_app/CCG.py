"""
Crystal Configuration Generator (Streamlit app)

Enumerate unique Br/I configurations for several coordination spheres,
show summary stats, and visualize configurations (if feasible).
"""

import streamlit as st
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
import sym_operations as sym
import define_permutations as pr
import visualize_streamlit_plotly as vis
import time
from fast_enum import enumerate_unique
from burnside import burnside_count

# --- Coordination spheres ---
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

# --- Utility ---
def get_streamlit_configs(n_br, coordinates, enum_max=30_000_000, sphere=1):
    """
    Compute unique Br/I configurations (or counts) for a coordination sphere.

    Returns
    -------
    tuple: (uniq_dict, n_unique, n_total, can_visualize)
        uniq_dict: {config_int: degeneracy} or None
        n_unique: int, number of unique configurations
        n_total: int, total configurations before symmetry
        can_visualize: bool, True if enumeration (not Burnside) is used
    """
    ops = sym.D4h_symmetry_operations()
    perms = list(pr.find_all_permutations(ops, coordinates).values())
    n_sites = len(coordinates)
    uniq_dict, n_total = enumerate_unique(n_sites, n_br, perms, enum_max)
    if uniq_dict is None:  # Burnside Tier
        n_unique = burnside_count(n_sites, n_br, sphere=sphere, perms=perms)
        return None, n_unique, n_total, False  # Not visualizable
    n_unique = len(uniq_dict)
    return uniq_dict, n_unique, n_total, True

# --- Streamlit UI ---
st.title("Crystal Configuration Generator")

sphere = st.selectbox(
    "Select Coordination Sphere",
    [1, 2, 3],
    format_func=lambda x: "1st (14 atoms)" if x == 1 else
                          "2nd (46 atoms)" if x == 2 else
                          "Reduced (8 atoms)"
)
enum_max = st.number_input(
    "Max configs for enumeration (otherwise Burnside, no visualization)", value=30_000_000, min_value=1000
)
if sphere == 1:
    num_i = st.slider('Number of I Atoms', 0, 7, 1)
    coordinates = coordinates_first_sphere
elif sphere == 2:
    num_i = st.slider('Number of I Atoms', 0, 28, 1)
    coordinates = coordinates_second_sphere
else:
    num_i = st.slider('Number of I Atoms', 0, 4, 1)
    coordinates = coordinates_reduced_sphere

show_axis = st.checkbox('Show Axis', value=True)
if st.button('Generate Configurations'):
    start = time.time()
    uniq_dict, n_unique, n_total, can_visualize = get_streamlit_configs(num_i, coordinates, enum_max, sphere=sphere)
    elapsed = time.time() - start

    st.markdown(f"**Number of I atoms:** {num_i}")
    st.markdown(f"**Number of Br atoms:** {len(coordinates) - num_i}")
    st.markdown(f"**Total number of configurations:** {n_total:,}")
    st.markdown(f"**Total number of unique configurations:** {n_unique:,}")
    st.markdown(f"**Time taken:** {elapsed:.2f} seconds")

    if not can_visualize:
        st.warning("Too many configurations to visualize. Only statistics are shown.")
    else:
        structures = []
        for idx, (config_int, degeneracy) in enumerate(uniq_dict.items()):
            bits = [(config_int >> i) & 1 for i in range(len(coordinates))]
            symbols = ['Br'] * (len(coordinates) + 1)
            for i, b in enumerate(bits):
                symbols[i + 1] = 'I' if b else 'Br'
            title = f"Config {idx+1}: Degeneracy {degeneracy}"
            full_coords = [[0, 0, 0]] + coordinates
            structures.append((full_coords, symbols, title))

        figures = vis.plot_multiple_structures(
            structures, elevation=1.5, azimuth=1.5, show_axis=show_axis
        )
        # Limit to max 100 plots to avoid browser overload!
        for i, fig in enumerate(figures[:100]):
            st.plotly_chart(fig, use_container_width=True)
        if len(figures) > 100:
            st.info(f"Only first 100 structures shown out of {len(figures)}.")

