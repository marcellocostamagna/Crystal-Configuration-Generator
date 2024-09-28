import sym_operations as sym
import define_permutations as pr
import visualize as vis
import time
import multiprocessing as mp
from itertools import combinations

# First coordination sphere (10 atoms)
coordinates_first_sphere = [ 
    [0, 0, 2],   # 1
    [1, 0, 1],   # 2
    [0, -1, 1],  # 3  
    [-1, 0, 1],  # 4 
    [0, 1, 1],   # 5
    [1, 0, -1],  # 6
    [0, -1, -1], # 7 
    [-1, 0, -1], # 8
    [0, 1, -1],  # 9
    [0, 0, -2],  # 10
     # Adding the 4 alogens equatorial atoms
    [1, 1, 0],
    [1, -1, 0],
    [-1, 1, 0],
    [-1, -1, 0]
]

# Second coordination sphere (50 atoms)
coordinates_second_sphere = [ 
    # [0, 0, 0],  # Always an Iodine atom
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
    # second double-octaehdron traslated by 2 units in the x direction (less the same atoms)
    [2, 0, 0],
    [2, 0, 2],   
    [3, 0, 1],   
    [2, -1, 1],    
    [2, 1, 1],   
    [3, 0, -1],  
    [2, -1, -1],  
    [2, 1, -1],  
    [2, 0, -2],  
    # third double-octaehdron traslated by 2 units in the y direction
    [0, 2, 0],   
    [0, 2, 2],   
    [1, 2, 1],   
    [-1, 2, 1],   
    [0, 3, 1],   
    [1, 2, -1],  
    [-1, 2, -1], 
    [0, 3, -1],  
    [0, 2, -2],  
    # fourth double-octaehdron traslated by 2 units in the -x direction
    [-2, 0, 0],   
    [-2, 0, 2],   
    [-3, 0, 1],   
    [-2, -1, 1],    
    [-2, 1, 1],   
    [-3, 0, -1],  
    [-2, -1, -1],  
    [-2, 1, -1],  
    [-2, 0, -2],  
    # fifth double-octaehdron traslated by 2 units in the -y direction
    [0, -2, 0],   
    [0, -2, 2],   
    [1, -2, 1],   
    [-1, -2, 1],   
    [0, -3, 1],   
    [1, -2, -1],  
    [-1, -2, -1], 
    [0, -3, -1],  
    [0, -2, -2],  
    # four corner atoms
    [1, 1, 0],
    [2, 2, 0],   
    [1, -1, 0],
    [-2, 2, 0],  
    [-1, 1, 0],
    [2, -2, 0], 
    [-1, -1, 0], 
    [-2, -2, 0],    
]

# Normalize configurations
def apply_permutation(configuration, permutation):
    return [configuration[i] for i in permutation]

def normalize_configuration(configuration, symmetry_operations):
    equivalent_configs = [apply_permutation(configuration, op) for op in symmetry_operations]
    return min(equivalent_configs)

# Normalization function to be run in parallel
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
    # Choose the positions for Br
    for br_positions in combinations(range(total_positions), num_br):
        # Create a list of all 'I's
        elements_list = ['I'] * total_positions
        # Place 'Br' at the chosen positions
        for pos in br_positions:
            elements_list[pos] = 'Br'
        # Yield the current combination of Br and I as a tuple (tuples are hashable)
        yield tuple(elements_list)

def generate_unique_configurations(num_br, total_positions=10, sphere=1):
    
    # Generate all possible combinations of Br and I
    all_combinations= set(generate_combinations(total_positions, num_br))
        
    total_combinations = len(all_combinations)
    # print(f'Total number of combinations: {total_combinations}')

    # Get D4h symmetry operations and permutations
    operations = sym.D4h_symmetry_operations()
    permutations = list(pr.find_all_permutations(operations, coordinates).values())
    
    # Set up multiprocessing
    num_processes = mp.cpu_count()
    pool = mp.Pool(processes=num_processes)
    chunk_size = max(1, len(all_combinations) // num_processes)
    chunks = [list(all_combinations)[i:i + chunk_size] for i in range(0, len(all_combinations), chunk_size)]
    
    # Map multiprocessing
    result_dicts = pool.map(process_permutations, [(chunk, permutations) for chunk in chunks])
    
    # Combine results
    unique_configs = {}
    for result in result_dicts:
        for config, count in result.items():
            if config not in unique_configs:
                unique_configs[config] = 0
            unique_configs[config] += count
            
    pool.close()
    pool.join()
    
    return unique_configs, total_combinations


if __name__ == '__main__':
    ##### Define Initial Input #####

    ## COORDINATES OF THE SYSTEM ##
    
    # choose first or second coordination sphere
    sphere = 2
    
    if sphere == 1:
        coordinates = coordinates_first_sphere
    elif sphere == 2:
        coordinates = coordinates_second_sphere
        
    ## NUMBER OF BROMINE ATOMS ##
    # Define the number of Br atoms (example: 1 Br)
    num_br = 1
    start = time.time()

    # Generate and print unique configurations and their degeneracy
    unique_configs, n_config = generate_unique_configurations(num_br, total_positions=len(coordinates), sphere=sphere)

    end = time.time()

    # # Print the results
    # print("\nUnique configurations and their degeneracy:")
    # for config, degeneracy in unique_configs.items():
    #     print(f"Configuration: {config}, Degeneracy: {degeneracy}")

    total_unique_configs = len(unique_configs)
  

    ## VISUALIZE THE MOLECULAR STRUCTURES ##
    structures = []
    for idx, (config, degeneracy) in enumerate(unique_configs.items()):
        symbols = ['I'] * (len(coordinates) + 1)  # Initialize all as 'I' and add the central Iodine atom
        symbols[0] = 'I'  # Add central Iodine atom
        for i, atom in enumerate(config):
            symbols[i + 1] = atom  # Adjust indices to account for the central Iodine atom
        title = f'Config {idx + 1}: Degeneracy {degeneracy}'
        full_coordinates = [[0, 0, 0]] + coordinates  # Add central Iodine atom coordinates
        structures.append((full_coordinates, symbols, title))
        
    # Get the total number of configurations for the give number of Br and the number of unique configurations
    tot_config = sum(unique_configs.values())
    n_unq_config = len(unique_configs)

    # Check that there are all the possible configurations
    print(f"\nTotal number of configurations: {tot_config}")
    print(f"\nTotal number of unique configurations: {total_unique_configs}")
    print(f"Time taken: {end - start:.2f} seconds")

    assert tot_config == n_config, f"Error: Total number of configurations ({tot_config}) does not match the expected number ({n_config})"

    # # Plot the unique configurations
    vis.plot_multiple_structures(structures, 
                                main_title='Unique Configurations', 
                                ratio=f'N˚ of Br atoms: {num_br} ; N˚ of I atoms: {len(coordinates) - num_br}',
                                data=f'Total number of configurations: {tot_config} ; Number of unique configurations: {n_unq_config}')

    end = time.time()
    print(f"Time taken to generate unique configurations: {end - start:.2f} seconds")