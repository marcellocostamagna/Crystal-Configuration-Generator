import matplotlib.pyplot as plt
import numpy as np
import os

def get_connections(num_atoms):
    """Return a list of (start, end) tuples defining connections between atoms."""
    if num_atoms == 15:
        return [
            (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9),
            (1, 2), (1, 3), (1, 4), (1, 5),
            (2, 3), (2, 5),
            (4, 3), (4, 5),
            (6, 7), (6, 9),
            (8, 7), (8, 9),
            (6, 10), (7, 10), (8, 10), (9, 10),
            (0, 11), (0, 12), (0, 13), (0, 14)
        ]
    elif num_atoms == 47:
        return  [
            (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9),
            (1, 2), (1, 3), (1, 4), (1, 5),
            (2, 3), (2, 5), (2, 11), (2, 12), (2, 14), (2, 15),
            (3, 4), (3, 38), (3, 39), (3, 40), (3, 41),
            (4, 5), (4, 29), (4, 30), (4, 32), (4, 33),
            (5, 20), (5, 21), (5, 22), (5, 23),
            (6, 7), (6, 9), (6, 10), (6, 11), (6, 17), (6, 18), (6, 19),
            (7, 8), (7, 10), (7, 38), (7, 43), (7, 44), (7, 46),
            (8, 9), (8, 10), (8, 29), (8, 35), (8, 36), (8, 37),
            (9, 10), (9, 20), (9, 25), (9, 26), (9, 28),
            (11, 13), (11, 14), (11, 15), (11, 16), (11, 17), (11, 18),
            (12, 13), (12, 14), (12, 15),
            (13, 14), (13, 15), 
            (16, 17), (16, 18), (16, 19), 
            (17, 19),
            (18, 19), 
            (20, 22), (20, 23), (20, 24), (20, 25), (20, 26), (20, 27),
            (21, 22), (21, 23), (21, 24), 
            (22, 24), 
            (23, 24),
            (25, 27), (25, 28), 
            (26, 20), (26, 27), (26, 28),
            (27, 28),
            (29, 31), (29, 32), (29, 33), (29, 34), (29, 35), (29, 36),
            (30, 31), (30, 32), (30, 33), 
            (31, 32), (31, 33),
            (34, 35), (34, 36), (34, 37), 
            (35, 37),
            (36, 34), (36, 37), 
            (38, 40), (38, 41), (38, 42), (38, 43), (38, 44), (38, 45),
            (39, 40), (39, 41), (39, 42), 
            (40, 42),
            (41, 42), 
            (43, 45), (43, 46),
            (44, 45), (44, 46), (45, 46),
            ]
    else:
        return [
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8),
            (1, 2), (1, 4),
            (3, 2), (3, 4),
            (5, 6), (5, 8),
            (7, 6), (7, 8),
        ]
            
def save_structures_as_svgs(structures, outdir, prefix='', elevation=20, azimuth=80):
    """
    Save each molecular structure as a separate SVG image.
    Connections are added (no labels, no axes shown).
    """
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    color_map = {'I': 'red', 'Br': 'blue'}

    for idx, (coordinates, symbols, title) in enumerate(structures):
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111, projection='3d')

        # Plot atoms
        for i, c in enumerate(coordinates):
            color = color_map[symbols[i]]
            ax.scatter(*c, color=color, label=symbols[i], s=50)

        # Draw connections
        connections = get_connections(len(coordinates))
        for start, end in connections:
            x_values = [coordinates[start][0], coordinates[end][0]]
            y_values = [coordinates[start][1], coordinates[end][1]]
            z_values = [coordinates[start][2], coordinates[end][2]]
            ax.plot(x_values, y_values, z_values, color='grey', linewidth=0.8)

        ax.set_box_aspect([1, 1, 1])
        max_range = max([max(coordinates, key=lambda item: abs(item[i]))[i] for i in range(3)])
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        ax.set_zlim(-max_range, max_range)
        ax.set_title(title)
        ax.view_init(elev=elevation, azim=azimuth)
        ax.set_axis_off()  # Hide all axes

        handles = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='I'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Br')
        ]
        fig.legend(handles=handles, title='Elements', loc='upper right')

        filename = f"{prefix}_config{idx+1}.svg"
        filepath = os.path.join(outdir, filename)
        plt.savefig(filepath, format='svg')
        plt.close(fig)
        
