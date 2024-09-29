import streamlit as st
import sym_operations as sym
import define_permutations as pr
import visualize_streamlit_plotly as vis
import time
import multiprocessing as mp
from itertools import combinations

# Define your coordination spheres
coordinates_first_sphere = [ 
    [0, 0, 2],
    [1, 0, 1], 
    [0, -1, 1], 
    [-1, 0, 1], 
    [0, 1, 1], 
    [1, 0, -1],
    [0, -1, -1],
    [-1, 0, -1], 
    [0, 1, -1], 
    [0, 0, -2], 
    [2, 0, 0], 
    [-2, 0, 0],
    [0, 2, 0], 
    [0, -2, 0]
]

coordinates_second_sphere = [
    [0, 0, 2],
    [1, 0, 1],
    [0, -1, 1],
    [-1, 0, 1], 
    [0, 1, 1], 
    [1, 0, -1],
    [0, -1, -1],
    [-1, 0, -1],
    [0, 1, -1], 
    [0, 0, -2], 
    [2, 0, 0], 
    [2, 0, 2],
    [3, 0, 1],
    [2, -1, 1],
    [2, 1, 1], 
    [3, 0, -1],
    [2, -1, -1],
    [2, 1, -1],
    [2, 0, -2],
    [0, 2, 0], 
    [0, 2, 2], 
    [1, 2, 1], 
    [-1, 2, 1],
    [0, 3, 1],
    [1, 2, -1], 
    [-1, 2, -1], 
    [0, 3, -1], 
    [0, 2, -2],
    [-2, 0, 0],
    [-2, 0, 2],
    [-3, 0, 1],
    [-2, -1, 1],
    [-2, 1, 1],
    [-3, 0, -1],
    [-2, -1, -1], 
    [-2, 1, -1],
    [-2, 0, -2],
    [0, -2, 0],
    [0, -2, 2],
    [1, -2, 1],
    [-1, -2, 1],
    [0, -3, 1],
    [1, -2, -1],
    [-1, -2, -1],
    [0, -3, -1],
    [0, -2, -2], 
    # [1, 1, 0], 
    # [2, 2, 0], 
    # [-1, 1, 0], 
    # [-2, 2, 0],
    # [1, -1, 0],
    # [2, -2, 0], 
    # [-1, -1, 0],
    # [-2, -2, 0],
    
]

def apply_permutation(configuration, permutation):
    return [configuration[i] for i in permutation]

def normalize_configuration(configuration, symmetry_operations):
    equivalent_configs = [apply_permutation(configuration, op) for op in symmetry_operations]
    return min(equivalent_configs)

def process_permutations(data):
    perms, permutations = data
    unique_configs = {}
    for perm in perms:
        normalized_config = tuple(normalize_configuration(list(perm), permutations))
        if normalized_config not in unique_configs:
            unique_configs[normalized_config] = 0
        unique_configs[normalized_config] += 1
    return unique_configs

def generate_combinations(total_positions, num_br):
    for br_positions in combinations(range(total_positions), num_br):
        elements_list = ['I'] * total_positions
        for pos in br_positions:
            elements_list[pos] = 'Br'
        yield tuple(elements_list)

def generate_unique_configurations(num_br, total_positions=10, sphere=1):

    all_combinations = set(generate_combinations(total_positions, num_br))

    total_combinations = len(all_combinations)
    operations = sym.D4h_symmetry_operations()
    permutations = list(pr.find_all_permutations(operations, coordinates).values())

    num_processes = mp.cpu_count()
    pool = mp.Pool(processes=num_processes)
    chunk_size = max(1, len(all_combinations) // num_processes)
    chunks = [list(all_combinations)[i:i + chunk_size] for i in range(0, len(all_combinations), chunk_size)]

    result_dicts = pool.map(process_permutations, [(chunk, permutations) for chunk in chunks])

    unique_configs = {}
    for result in result_dicts:
        for config, count in result.items():
            if config not in unique_configs:
                unique_configs[config] = 0
            unique_configs[config] += count

    pool.close()
    pool.join()

    return unique_configs, total_combinations

# Streamlit App UI
st.title("Crystal Configuration Generator")

# Choose the coordination sphere
sphere = st.selectbox('Select Coordination Sphere', [1, 2], format_func=lambda x: "1st Coordination Sphere (14 atoms)" if x == 1 else "2nd Coordination Sphere (46 atoms)")

# Choose the number of Bromine atoms based on the sphere
if sphere == 1:
    num_br = st.slider('Select Number of Br Atoms (0-7)', 0, 7, 1)
    coordinates = coordinates_first_sphere
else:
    num_br = st.slider('Select Number of Br Atoms (0-27)', 0, 27, 1)
    coordinates = coordinates_second_sphere

if st.button('Generate Configurations'):
    start = time.time()
    
    # Generate unique configurations
    unique_configs, n_config = generate_unique_configurations(num_br, total_positions=len(coordinates), sphere=sphere)

    end = time.time()

    total_unique_configs = len(unique_configs)

    # Display the parameters
    
    # st.write(f"Number of Br atoms: {num_br}")
    # st.write(f"Number of I atoms: {len(coordinates) - num_br}")
    # st.write(f"Total number of configurations: {n_config}")
    # # Display results
    # st.write(f"Total number of unique configurations: {total_unique_configs}")
    # # Display for each configuration its degeneracy
    # for idx, (config, degeneracy) in enumerate(unique_configs.items()):
    #     st.write(f"Configuration {idx + 1}: Degeneracy: {degeneracy}")
        
    # st.write(f"Time taken: {end - start:.2f} seconds")
    
    st.markdown(f"**Number of Br atoms:** {num_br}")
    st.markdown(f"**Number of I atoms:** {len(coordinates) - num_br}")
    st.markdown(f"**Total number of configurations:** {n_config}")
    st.markdown(f"**Total number of unique configurations:** {total_unique_configs}")

    # Add indentation and display each configuration and its degeneracy
    for idx, (config, degeneracy) in enumerate(unique_configs.items()):
        st.markdown(f"<div style='padding-left:20px'>Configuration {idx + 1}: Degeneracy: {degeneracy}</div>", unsafe_allow_html=True)

    # Add space before Time taken using <br> tag
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Time taken with bold
    st.markdown(f"**Time taken:** {end - start:.2f} seconds")

    # Optionally visualize configurations
    structures = []
    for idx, (config, degeneracy) in enumerate(unique_configs.items()):
        symbols = ['I'] * (len(coordinates) + 1)  # Initialize with all 'I' and add central Iodine atom
        symbols[0] = 'I'  # The central Iodine atom
        for i, atom in enumerate(config):
            symbols[i + 1] = atom  # Adjust indices to account for the central Iodine atom
        title = f'Config {idx + 1}: Degeneracy {degeneracy}'
        full_coordinates = [[0, 0, 0]] + coordinates  # Add central Iodine atom coordinates
        structures.append((full_coordinates, symbols, title))

    # Visualize the structures
    # figures = vis.plot_multiple_structures(structures, 
    #                                        main_title='Unique Configurations', 
    #                                        ratio=f'N˚ of Br atoms: {num_br} ; N˚ of I atoms: {len(coordinates) - num_br}',
    #                                        data=f'Total number of configurations: {n_config} ; Number of unique configurations: {total_unique_configs}')
    
    figures = vis.plot_multiple_structures(structures)
                 
    # Render each figure using st.plotly_chart
    for fig in figures:
        st.plotly_chart(fig)
