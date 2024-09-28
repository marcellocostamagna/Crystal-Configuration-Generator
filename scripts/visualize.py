import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_molecular_structure(coordinates, symbols, title):
    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection='3d')

    # Define a color map based on the labels
    color_map = {'I': 'red', 'Br': 'blue'}
    # Offset for the label placement
    label_offset = 0.1

    for i, c in enumerate(coordinates):
        color = color_map[symbols[i]]
        ax.scatter(*c, color=color, label=symbols[i])
        # Adding offset to the label position
        label_position = [c[0] + label_offset, c[1] + label_offset, c[2] + label_offset]
        ax.text(*label_position, f'{symbols[i]} {i}', color=color)

    # Set equal aspect ratio
    ax.set_box_aspect([1, 1, 1])  # Aspect ratio is 1:1:1

    # Set the same limits for all axes
    max_range = max([max(coordinates, key=lambda item: abs(item[i]))[i] for i in range(3)])
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)

    # Add titles and labels
    ax.set_title(title)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    # Customize legend to prevent duplicate labels
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), title='Elements')

    plt.show()

def plot_multiple_structures(structures, main_title='Molecular Structures', ratio=None, data=None, elevation=20, azimuth=80):
    fig = plt.figure(figsize=(15, 8.5))
    num_structures = len(structures)
    cols = int(np.ceil(np.sqrt(num_structures)))
    rows = int(np.ceil(num_structures / cols))

    base_size = 100  # Base marker size
    marker_size = base_size / np.sqrt(num_structures)  # Decrease size as the number of structures increases

    # Define connections as pairs of point indices (0-based index)
    if len(structures[0][0]) == 15:
        connections = [
            (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9),
            (1, 2), (1, 3), (1, 4), (1, 5),
            (2, 3), (2, 5),
            (4, 3), (4, 5),
            (6, 7), (6, 9),
            (8, 7), (8, 9),
            (6, 10), (7, 10), (8, 10), (9, 10),
            (0, 11), (0, 12), (0, 13), (0, 14),
        ]
    else:
        connections = [
            (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9),
            (1, 2), (1, 3), (1, 4), (1, 5),
            (2, 3), (2, 5), (2, 11), (2, 12), (2, 14), (2, 15),
            (3, 4), (3, 5), (3, 38), (3, 39), (3, 40), (3, 41),
            (4, 5), (4, 29), (4, 30), (4, 32), (4, 33),
            (5, 20), (5, 21), (5, 22), (5, 23),
            (6, 7), (6, 9), (6, 10), (6, 11), (6, 17), (6, 18), (6, 19),
            (7, 8), (7, 9), (7, 10), (7, 38), (7, 43), (7, 44), (7, 46),
            (8, 9), (8, 10), (8, 29), (8, 35), (8, 36), (8, 37),
            (9, 10), (9, 20), (9, 25), (9, 26), (9, 28),
            (11, 13), (11, 14), (11, 15), (11, 16), (11, 17), (11, 18),
            (12, 13), (12, 14), (12, 15),
            (13, 14), (13, 15),
            (16, 17), (16, 18), (16, 19),
            (17, 18), (17, 19),
            (18, 19),
            (19, 6),
            (20, 21), (20, 22), (20, 23), (20, 24), (20, 25), (20, 26), (20, 27),
            (21, 22), (21, 23), (21, 24),
            (22, 23), (22, 24),
            (23, 24),
            (24, 21), (24, 22), (24, 23),
            (25, 20), (25, 26), (25, 27), (25, 28),
            (26, 20), (26, 27), (26, 28),
            (27, 20), (27, 25), (27, 26), (27, 28),
            (28, 25), (28, 26),
            (29, 30), (29, 31), (29, 32), (29, 33), (29, 34), (29, 35), (29, 36), (29, 8),
            (30, 31), (30, 32), (30, 33),
            (31, 32), (31, 33),
            (32, 31), (32, 33),
            (33, 31), (33, 32),
            (34, 35), (34, 36), (34, 37),
            (35, 34), (35, 36), (35, 37),
            (36, 34), (36, 35), (36, 37),
            (37, 34), (37, 35), (37, 36), (37, 8),
            (38, 39), (38, 40), (38, 41), (38, 42), (38, 43), (38, 44), (38, 45),
            (39, 40), (39, 41), (39, 42),
            (40, 38), (40, 39), (40, 41), (40, 42),
            (41, 38), (41, 39), (41, 40), (41, 42),
            (42, 39), (42, 40), (42, 41),
            (43, 7), (43, 44), (43, 45), (43, 46),
            (44, 7), (44, 43), (44, 45), (44, 46),
            (45, 43), (45, 44), (45, 46),
            (46, 43), (46, 44), (46, 45),
            (0, 47), (0, 49), (0, 51), (0, 53),
            (47, 48), (49, 50), (51, 52), (53, 54),
        ]

    for idx, (coordinates, symbols, title) in enumerate(structures):
        ax = fig.add_subplot(rows, cols, idx + 1, projection='3d')

        # Define a color map based on the labels
        color_map = {'I': 'red', 'Br': 'blue'}

        # Plot the atoms
        for i, c in enumerate(coordinates):
            color = color_map[symbols[i]]
            ax.scatter(*c, color=color, label=symbols[i], s=marker_size)

        # Draw lines between specified points
        for start, end in connections:
            x_values = [coordinates[start][0], coordinates[end][0]]
            y_values = [coordinates[start][1], coordinates[end][1]]
            z_values = [coordinates[start][2], coordinates[end][2]]
            ax.plot(x_values, y_values, z_values, color='grey', linewidth=0.5)

        # Set equal aspect ratio
        ax.set_box_aspect([1, 1, 1])  # Aspect ratio is 1:1:1

        # Set the same limits for all axes
        max_range = max([max(coordinates, key=lambda item: abs(item[i]))[i] for i in range(3)])
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        ax.set_zlim(-max_range, max_range)

        # Set the initial orientation (view angle)
        ax.view_init(elev=elevation, azim=azimuth)  # Set initial elevation and azimuth

        # Add titles and labels
        ax.set_title(title, fontsize=10)
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')

        # Hide axes for better visualization
        ax.set_axis_off()

    # Create a custom legend for the entire figure
    handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='I'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Br')
    ]
    fig.legend(handles=handles, title='Elements', loc='upper right')

    # Adjust layout and spacing to prevent subplot overlap
    plt.tight_layout(pad=3.0, h_pad=3.0, w_pad=3.0)
    plt.subplots_adjust(top=0.85)

    # Title
    fig.suptitle(main_title, fontsize=16)
    # Number of Br atoms and I atoms
    fig.text(0.5, 0.93, ratio, ha='center', fontsize=12)
    # Total number of configurations and unique configurations
    fig.text(0.5, 0.9, data, ha='center', fontsize=12)

    # Save the image as an SVG
    # plt.savefig('unique_configurations_5.svg', format='svg')

    plt.show()
