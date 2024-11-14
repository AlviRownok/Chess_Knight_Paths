"""
Knight's Shortest Path Finder

This script finds all minimum-length sequences for a knight to move from an initial cell
to a final cell on an empty chessboard. It generates:
- A Graphviz DOT file representing the paths.
- PDF and PNG images of the paths overlaid on a chessboard.
- A GIF animation showing the knight moving along each path.

Features:
- Accepts positions in algebraic chess notation (e.g., e4, h7)
- Prompts user for input if arguments are not provided
- Generates visualizations in DOT, PDF, PNG, and GIF formats
- Includes detailed logging and error handling
"""

import sys  # Provides access to some variables used or maintained by the interpreter
import os  # Miscellaneous operating system interfaces
import argparse  # Parser for command-line options, arguments, and sub-commands
import logging  # Logging facility for Python
import re  # Regular expression operations
from collections import deque  # Container datatype providing fast appends and pops
import graphviz  # Graph visualization software
import random  # Generate pseudo-random numbers

import matplotlib.pyplot as plt  # MATLAB-like plotting framework
import matplotlib.patches as patches  # Create patch objects for matplotlib plots
from matplotlib.colors import ListedColormap  # Generate custom colormaps
import matplotlib.animation as animation  # Support for animations in matplotlib
from PIL import Image, ImageDraw, ImageFont  # Python Imaging Library for image manipulation
import numpy as np  # Fundamental package for scientific computing with Python
import imageio  # Read and write image data

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

    def generate_graphviz(self, paths, filename='paths'):
        dot = graphviz.Digraph(comment="Knight's Shortest Paths")  # Create a new directed graph
        for idx, path in enumerate(paths):
            with dot.subgraph(name=f'cluster_{idx}') as c:  # Create a subgraph for each path
                c.attr(label=f'Path {idx + 1}')  # Label the subgraph
                for i in range(len(path) - 1):
                    from_square = self.coord_to_alg(path[i])  # Convert coordinate to algebraic notation
                    to_square = self.coord_to_alg(path[i + 1])  # Convert next coordinate
                    c.edge(from_square, to_square)  # Add an edge between the squares
                # Mark start and end nodes
                c.node(self.coord_to_alg(path[0]), color='green')  # Start node in green
                c.node(self.coord_to_alg(path[-1]), color='red')  # End node in red
        dot.format = 'dot'  # Set output format to DOT
        dot.render(filename, cleanup=True)  # Render the graph and clean up temporary files
        logging.info(f"Graphviz DOT file saved to {filename}.dot")  # Log the file creation

    def draw_paths_on_board(self, paths, filename='paths'):
        # Create a chessboard
        board_colors = ['#F0D9B5', '#B58863']  # Light and dark square colors
        cmap = ListedColormap(board_colors)  # Create a colormap
        board = [[(row + col) % 2 for col in range(8)] for row in range(8)]  # Generate the board pattern

        fig, ax = plt.subplots(figsize=(8, 8))  # Create a figure and axis
        ax.imshow(board, cmap=cmap, extent=(0, 8, 0, 8))  # Display the board

        # Draw the paths
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow']  # Colors for paths
        for idx, path in enumerate(paths):
            color = colors[idx % len(colors)]  # Select color for the path
            xs = [coord[1] + 0.5 for coord in path]  # X-coordinates for plotting
            ys = [coord[0] + 0.5 for coord in path]  # Y-coordinates for plotting
            ax.plot(xs, ys, marker='o', color=color, linewidth=2, label=f'Path {idx + 1}')  # Plot the path
            # Mark start and end points
            ax.plot(xs[0], ys[0], marker='o', markersize=12, color='green', markeredgecolor='black')  # Start point
            ax.plot(xs[-1], ys[-1], marker='o', markersize=12, color='red', markeredgecolor='black')  # End point

        # Add labels to squares
        files = 'abcdefgh'  # Files (columns) labels
        ranks = '12345678'  # Ranks (rows) labels
        for row in range(8):
            for col in range(8):
                square = f"{files[col]}{row + 1}"  # Create square notation
                ax.text(col + 0.5, row + 0.5, square, ha='center', va='center', fontsize=8, color='black')  # Add text

        # Set axis labels and title
        ax.set_xticks([])  # Remove x-axis ticks
        ax.set_yticks([])  # Remove y-axis ticks
        ax.set_xlim(0, 8)  # Set x-axis limits
        ax.set_ylim(0, 8)  # Set y-axis limits
        ax.set_title("Knight's Shortest Paths")  # Set plot title
        ax.legend()  # Add a legend

        # Save the figure
        plt.savefig(f"{filename}.png", bbox_inches='tight')  # Save as PNG
        plt.savefig(f"{filename}.pdf", bbox_inches='tight')  # Save as PDF
        logging.info(f"Paths overlaid on chessboard saved as {filename}.png and {filename}.pdf")  # Log info
        plt.close()  # Close the figure

    def create_animation(self, paths, filename='paths'):
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

        # Save as GIF
        imageio.mimsave(f'{filename}.gif', images, fps=1)  # Create GIF from images
        logging.info(f"Animation saved as {filename}.gif")  # Log completion

    def get_knight_image(self):
        import os  # Import os for file path operations
        # Create a transparent image
        img = Image.new('RGBA', (100, 100), color=(255, 255, 255, 0))  # Create a blank image
        d = ImageDraw.Draw(img)  # Create a drawing context
        try:
            # Load the font from the local directory
            font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")  # Path to font file
            font = ImageFont.truetype(font_path, 80)  # Load the font at size 80
            d.text((10, 10), '♘', font=font, fill=(0, 0, 0))  # Draw the knight symbol
        except IOError as e:
            logging.error(f"Font could not be loaded: {e}")  # Log the error
            # Fallback to a simple 'K' character or handle as needed
            font = ImageFont.load_default()  # Load default font
            d.text((10, 10), 'K', font=font, fill=(0, 0, 0))  # Draw placeholder
        # Convert PIL image to numpy array for matplotlib
        knight_image = np.array(img)  # Convert image to array
        return knight_image  # Return the image array

    @staticmethod
    def alg_to_coord(alg_notation):
        files = 'abcdefgh'  # Files (columns) on the chessboard
        ranks = '12345678'  # Ranks (rows) on the chessboard
        match = re.match(r'^([a-hA-H])([1-8])$', alg_notation)  # Match algebraic notation
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

def prompt_for_position(prompt_message, suggestions):
    while True:
        suggestion_text = f"e.g., '{suggestions[0]}' or '{suggestions[1]}'"  # Example suggestions
        user_input = input(f"{prompt_message} ({suggestion_text}): ").strip()  # Prompt user
        if re.match(r'^[a-hA-H][1-8]$', user_input):  # Validate input
            return user_input  # Return valid input
        else:
            print("Invalid input. Please enter a valid chess position (a1 to h8).")  # Error message

def main():
    # Default configuration
    config = {
        "output_file": "paths",  # Default output filename
    }

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Knight's Shortest Path Finder")  # Create parser
    parser.add_argument('-s', '--start', help='Starting position (e.g., e4)')  # Start position argument
    parser.add_argument('-e', '--end', help='Ending position (e.g., h7)')  # End position argument
    parser.add_argument('-o', '--output', help='Output file name without extension')  # Output file argument
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')  # Verbose flag

    args = parser.parse_args()  # Parse command-line arguments

    # Update configuration with command-line arguments
    if args.output:
        config['output_file'] = args.output  # Set output filename
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)  # Enable debug logging

    # Prompt for start and end positions
    positions = [f"{file}{rank}" for file in 'abcdefgh' for rank in '12345678']  # All valid positions
    if args.start:
        start_input = args.start  # Use provided start position
    else:
        suggestions = random.sample(positions, 2)  # Generate suggestions
        start_input = prompt_for_position("Enter the starting position", suggestions)  # Prompt user

    if args.end:
        end_input = args.end  # Use provided end position
    else:
        suggestions = random.sample(positions, 2)  # Generate suggestions
        end_input = prompt_for_position("Enter the ending position", suggestions)  # Prompt user

    try:
        # Convert algebraic notation to coordinates
        start_coord = KnightPathFinder.alg_to_coord(start_input)  # Convert start position
        end_coord = KnightPathFinder.alg_to_coord(end_input)  # Convert end position

        # Initialize and run pathfinder
        finder = KnightPathFinder(start_coord, end_coord)  # Create an instance
        paths = finder.bfs_paths()  # Find all shortest paths

        if not paths:
            logging.warning(f"No paths found from {start_input} to {end_input}.")  # Log warning
            sys.exit(0)  # Exit if no paths found

        # Log the number of paths found
        logging.info(f"Found {len(paths)} shortest path(s) from {start_input} to {end_input}.")  # Log info

        # Generate Graphviz DOT file
        finder.generate_graphviz(paths, filename=config['output_file'])  # Generate DOT file

        # Draw paths on the chessboard
        finder.draw_paths_on_board(paths, filename=config['output_file'])  # Generate images

        # Create animation GIF
        finder.create_animation(paths, filename=config['output_file'])  # Generate GIF

    except Exception as e:
        logging.error(f"An error occurred: {e}")  # Log error
        sys.exit(1)  # Exit with error code

if __name__ == "__main__":
    main()  # Run the main function
