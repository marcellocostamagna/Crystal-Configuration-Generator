import plotly.graph_objects as go

# Function to calculate aspect ratio based on coordinates ranges
def calculate_aspect_ratio(coordinates):
    x_values = [c[0] for c in coordinates]
    y_values = [c[1] for c in coordinates]
    z_values = [c[2] for c in coordinates]

    # Calculate the range of each axis
    x_range = max(x_values) - min(x_values)
    y_range = max(y_values) - min(y_values)
    z_range = max(z_values) - min(z_values)

    # Set aspect ratio based on the axis ranges
    max_range = max(x_range, y_range, z_range)
    return dict(x=x_range / max_range, y=y_range / max_range, z=z_range / max_range)


# Define a function to plot the molecular structure using Plotly
def plot_molecular_structure(coordinates, symbols, title, elevation=1.5, azimuth=1.5):
    fig = go.Figure()

    # Define a color map based on the labels
    color_map = {'I': 'red', 'Br': 'blue'}

    # Add scatter plot for atoms
    for i, c in enumerate(coordinates):
        color = color_map[symbols[i]]
        fig.add_trace(go.Scatter3d(
            x=[c[0]], y=[c[1]], z=[c[2]],
            mode='markers+text',
            marker=dict(size=10, color=color),
            text=f'{symbols[i]} {i}',
            textposition='top center'
        ))

    # Calculate aspect ratio based on the coordinates
    aspect_ratio = calculate_aspect_ratio(coordinates)

    # Set equal aspect ratio, initial orientation, and titles
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X axis',
            yaxis_title='Y axis',
            zaxis_title='Z axis',
            aspectmode='manual',  # Ensures that the aspect ratio is explicitly set
            aspectratio=aspect_ratio,  # Set calculated aspect ratio
            camera=dict(
                eye=dict(x=elevation, y=azimuth, z=1.25)  # Adjusted camera position for closer view
            )
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    # Return the Plotly figure to be rendered in Streamlit
    return fig


# Define a function to plot multiple molecular structures using Plotly (sequentially in Streamlit)
def plot_multiple_structures(structures, elevation=1.5, azimuth=1.5):
    figures = []  # List to hold all the individual figures

    # Loop through each structure and add it to the figure
    for idx, (coordinates, symbols, title) in enumerate(structures):
        fig = go.Figure()

        # Define a color map based on the labels
        color_map = {'I': 'red', 'Br': 'blue'}

        # Add atoms as scatter plot points
        for i, c in enumerate(coordinates):
            color = color_map[symbols[i]]
            fig.add_trace(go.Scatter3d(
                x=[c[0]], y=[c[1]], z=[c[2]],
                mode='markers',
                marker=dict(size=8, color=color),
                name=f'{symbols[i]} {i}'
            ))

        # Define connections as pairs of point indices (0-based index)
        if len(coordinates) == 15:
            connections = [
                (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9),
                (1, 2), (1, 3), (1, 4), (1, 5),
                (2, 3), (2, 5),
                (4, 3), (4, 5),
                (6, 7), (6, 9),
                (8, 7), (8, 9),
                (6, 10), (7, 10), (8, 10), (9, 10),
                (0, 11), (0, 12), (0, 13), (0, 14)
            ]
        elif len(coordinates) == 27:
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
            ]
        else:
            connections = [
                (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8),
                (1, 2), (1, 4),
                (3, 2), (3, 4),
                (5, 6), (5, 8),
                (7, 6), (7, 8),
                
            ]
        # Add connections between specified points (check if indices are valid)
        for start, end in connections:
            if start < len(coordinates) and end < len(coordinates):  # Check if indices are valid
                x_values = [coordinates[start][0], coordinates[end][0]]
                y_values = [coordinates[start][1], coordinates[end][1]]
                z_values = [coordinates[start][2], coordinates[end][2]]
                fig.add_trace(go.Scatter3d(
                    x=x_values, y=y_values, z=z_values,
                    mode='lines',
                    line=dict(color='gray', width=2),
                    showlegend=False
                ))

        # Calculate aspect ratio based on the coordinates
        aspect_ratio = calculate_aspect_ratio(coordinates)

        # Update layout with aspect ratio, initial orientation, and titles
        fig.update_layout(
            title=f"{title}", #({ratio})" if ratio else title,
            scene=dict(
                xaxis_title='X axis',
                yaxis_title='Y axis',
                zaxis_title='Z axis',
                aspectmode='manual',  # Set aspect mode to 'manual' for explicit control
                aspectratio=aspect_ratio,  # Set calculated aspect ratio
                camera=dict(
                    eye=dict(x=elevation, y=azimuth, z=1.25)  # Set initial camera position (closer view)
                )
            ),
            margin=dict(l=0, r=0, b=0, t=40)
        )

        # If additional data is provided, display it in the plot title
        # if data:
        #     fig.update_layout(title=f"{title} ({ratio}), {data}" if ratio else f"{title}, {data}")

        # Append the generated figure to the list
        figures.append(fig)

    # Return the list of Plotly figures
    return figures
