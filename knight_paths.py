"""
Knight's Shortest Path Finder (Streamlit Version)

This Streamlit app finds all minimum-length sequences for a knight to move from an initial cell
to a final cell on an empty chessboard. It displays:
- An animated GIF showing the knight moving along each path.

Features:
- Accepts positions in algebraic chess notation (e.g., e4, h7)
- Provides input fields for user to enter positions
- Generates visualizations in GIF format displayed within the app
- Includes detailed logging and error handling
"""

import sys
import os
import logging
import re
from collections import deque
import random

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import imageio
import streamlit as st  # Streamlit for web app

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class KnightPathFinder:
    def __init__(self, start, end):
        self.start = start  # Starting position as (row, col)
        self.end = end  # Ending position as (row, col)
        self.knight_moves = [  # All possible moves a knight can make
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        self.board_size = 8  # Standard chessboard size
        logging.debug(f"Initialized KnightPathFinder with start={start} and end={end}")

    def is_valid(self, position):
        row, col = position  # Unpack the position
        return 0 <= row < self.board_size and 0 <= col < self.board_size  # Check if position is on the board

    def bfs_paths(self):
        queue = deque([[self.start]])  # Queue for BFS initialized with the starting position
        visited = set()  # Set to keep track of visited positions
        paths = []  # List to store all shortest paths found
        min_length = None  # Variable to store the length of the shortest path
        while queue:
            path = queue.popleft()  # Get the next path from the queue
            current = path[-1]  # Current position is the last in the path
            if current == self.end:
                if min_length is None:
                    min_length = len(path)  # Set min_length when the first path is found
                if len(path) == min_length:
                    paths.append(path)  # Add the path if it's of minimum length
                continue  # Continue to check for other paths of the same length
            if current in visited:
                continue  # Skip if we've already visited this position
            visited.add(current)  # Mark the current position as visited
            for move in self.knight_moves:
                next_position = (current[0] + move[0], current[1] + move[1])  # Calculate the next position
                if self.is_valid(next_position):
                    queue.append(path + [next_position])  # Add the new path to the queue
        return paths  # Return all the shortest paths found

    def create_animation(self, paths):
        # Load knight image
        knight_image = self.get_knight_image()  # Get the image of the knight piece

        # Create a chessboard
        board_colors = ['#F0D9B5', '#B58863']  # Chessboard colors
        cmap = ListedColormap(board_colors)  # Create colormap
        board = [[(row + col) % 2 for col in range(8)] for row in range(8)]  # Generate board pattern

        images = []  # List to store images for animation

        for idx, path in enumerate(paths):
            xs = [coord[1] + 0.5 for coord in path]  # X-coordinates for the path
            ys = [coord[0] + 0.5 for coord in path]  # Y-coordinates for the path
            for i in range(len(path)):
                fig, ax = plt.subplots(figsize=(6, 6))  # Create a new figure for each frame
                ax.imshow(board, cmap=cmap, extent=(0, 8, 0, 8))  # Display the chessboard
                ax.set_xticks([])  # Remove x-axis ticks
                ax.set_yticks([])  # Remove y-axis ticks
                ax.set_xlim(0, 8)  # Set x-axis limits
                ax.set_ylim(0, 8)  # Set y-axis limits
                # Add labels to squares
                files = 'abcdefgh'
                ranks = '12345678'
                for row in range(8):
                    for col in range(8):
                        square = f"{files[col]}{row + 1}"  # Square notation
                        ax.text(col + 0.5, row + 0.5, square, ha='center', va='center', fontsize=8, color='black')  # Label

                # Mark start and end points
                start_x, start_y = xs[0], ys[0]  # Start position
                end_x, end_y = xs[-1], ys[-1]  # End position
                ax.plot(start_x, start_y, marker='o', markersize=12, color='green', markeredgecolor='black')  # Start
                ax.plot(end_x, end_y, marker='o', markersize=12, color='red', markeredgecolor='black')  # End

                # Plot path so far
                ax.plot(xs[:i+1], ys[:i+1], marker='o', color='blue', linewidth=2)  # Path up to current move

                # Place the knight image
                x = xs[i] - 0.5  # Adjust x-coordinate for image placement
                y = ys[i] - 0.5  # Adjust y-coordinate
                ax.imshow(knight_image, extent=(x, x + 1, y, y + 1))  # Overlay knight image

                # Capture the frame
                fig.canvas.draw()  # Render the figure
                image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')  # Get image data
                image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))  # Reshape data
                images.append(image)  # Add frame to images list
                plt.close(fig)  # Close the figure

        # Save as GIF to a BytesIO object
        import io
        bytes_io = io.BytesIO()
        imageio.mimsave(bytes_io, images, format='GIF', fps=1)
        bytes_io.seek(0)
        return bytes_io.getvalue()  # Return the GIF bytes

    def get_knight_image(self):
        import os                                           # Import os module for file path operations
        img = Image.new('RGBA', (100, 100), color=(255, 255, 255, 0))  # Create a transparent image (100x100 pixels)
        d = ImageDraw.Draw(img)                             # Initialize drawing context on the image
        try:
            font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")  # Build path to the font file
            font = ImageFont.truetype(font_path, 80)        # Load the TrueType font at size 80
            d.text((10, 10), '♘', font=font, fill=(0, 0, 0))  # Draw the knight symbol '♘' at position (10,10)
        except IOError as e:
            logging.error(f"Font could not be loaded: {e}")  # Log an error if the font can't be loaded
            font = ImageFont.load_default()                 # Fallback: load the default font
            d.text((10, 10), 'K', font=font, fill=(0, 0, 0))  # Draw 'K' instead of '♘' at position (10,10)
        knight_image = np.array(img)                        # Convert the image to a NumPy array
        return knight_image                                 # Return the knight image array

    @staticmethod
    def alg_to_coord(alg_notation):
        files = 'abcdefgh'  # Files (columns) on the chessboard
        ranks = '12345678'  # Ranks (rows) on the chessboard
        match = re.match(r'^([a-hA-H])([1-8])$', alg_notation.strip())  # Match algebraic notation
        if match:
            file_char, rank_char = match.groups()  # Extract file and rank
            col = files.index(file_char.lower())  # Convert file to column index
            row = int(rank_char) - 1  # Convert rank to row index
            return (row, col)  # Return position as (row, col)
        else:
            raise ValueError(f"Invalid algebraic notation: {alg_notation}")  # Raise error if invalid

    @staticmethod
    def coord_to_alg(coord):
        files = 'abcdefgh'  # Files labels
        ranks = '12345678'  # Ranks labels
        row, col = coord  # Unpack the coordinate
        if 0 <= row < 8 and 0 <= col < 8:
            return f"{files[col]}{row + 1}"  # Convert to algebraic notation
        else:
            raise ValueError(f"Invalid coordinate: {coord}")  # Raise error if out of bounds

# Streamlit App
def main():
    st.set_page_config(layout="wide")  # Set layout to wide mode

    # Create two columns for layout
    col1, col2 = st.columns([1, 2])

    with col1:
        st.header("Knight's Shortest Path Finder")
        st.write("Enter the starting and ending positions in algebraic notation (e.g., e4, h7).")

        # Input fields for starting and ending positions
        start_input = st.text_input("Enter the starting position (e.g., e4)", value="")
        end_input = st.text_input("Enter the ending position (e.g., h7)", value="")

        # Button to trigger the path finding
        if st.button("Find Paths"):
            # Clear previous outputs
            if 'gif_bytes' in st.session_state:
                del st.session_state['gif_bytes']
            try:
                # Validate inputs
                start_coord = KnightPathFinder.alg_to_coord(start_input)
                end_coord = KnightPathFinder.alg_to_coord(end_input)

                # Initialize and run pathfinder
                finder = KnightPathFinder(start_coord, end_coord)
                paths = finder.bfs_paths()

                if not paths:
                    st.warning(f"No paths found from {start_input} to {end_input}.")
                else:
                    st.info(f"Found {len(paths)} shortest path(s) from {start_input} to {end_input}.")
                    # Generate the GIF animation
                    gif_bytes = finder.create_animation(paths)
                    # Store the GIF bytes in session state
                    st.session_state['gif_bytes'] = gif_bytes
            except Exception as e:
                st.error(f"An error occurred: {e}")

    with col2:
        # Display the GIF animation
        if 'gif_bytes' in st.session_state:
            st.image(st.session_state['gif_bytes'], use_column_width=True)
        else:
            st.write("The animation will appear here after you input positions and click 'Find Paths'.")

if __name__ == "__main__":
    main()
