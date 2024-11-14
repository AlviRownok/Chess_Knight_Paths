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

import sys
import os
import argparse
import logging
import re
from collections import deque
import graphviz
import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import ListedColormap
import matplotlib.animation as animation
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import imageio

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class KnightPathFinder:
    def __init__(self, start, end):
        self.start = start  # Tuple (row, col)
        self.end = end      # Tuple (row, col)
        self.knight_moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        self.board_size = 8  # Standard chessboard size
        logging.debug(f"Initialized KnightPathFinder with start={start} and end={end}")

    def is_valid(self, position):
        row, col = position
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def bfs_paths(self):
        queue = deque([[self.start]])
        visited = set()
        paths = []
        min_length = None
        while queue:
            path = queue.popleft()
            current = path[-1]
            if current == self.end:
                if min_length is None:
                    min_length = len(path)
                if len(path) == min_length:
                    paths.append(path)
                continue
            if current in visited:
                continue
            visited.add(current)
            for move in self.knight_moves:
                next_position = (current[0] + move[0], current[1] + move[1])
                if self.is_valid(next_position):
                    queue.append(path + [next_position])
        return paths

    def generate_graphviz(self, paths, filename='paths'):
        dot = graphviz.Digraph(comment="Knight's Shortest Paths")
        for idx, path in enumerate(paths):
            with dot.subgraph(name=f'cluster_{idx}') as c:
                c.attr(label=f'Path {idx + 1}')
                for i in range(len(path) - 1):
                    from_square = self.coord_to_alg(path[i])
                    to_square = self.coord_to_alg(path[i + 1])
                    c.edge(from_square, to_square)
                # Mark start and end nodes
                c.node(self.coord_to_alg(path[0]), color='green')
                c.node(self.coord_to_alg(path[-1]), color='red')
        dot.format = 'dot'
        dot.render(filename, cleanup=True)
        logging.info(f"Graphviz DOT file saved to {filename}.dot")

    def draw_paths_on_board(self, paths, filename='paths'):
        # Create a chessboard
        board_colors = ['#F0D9B5', '#B58863']  # Light and dark squares
        cmap = ListedColormap(board_colors)
        board = [[(row + col) % 2 for col in range(8)] for row in range(8)]

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(board, cmap=cmap, extent=(0, 8, 0, 8))

        # Draw the paths
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow']
        for idx, path in enumerate(paths):
            color = colors[idx % len(colors)]
            xs = [coord[1] + 0.5 for coord in path]
            ys = [coord[0] + 0.5 for coord in path]
            ax.plot(xs, ys, marker='o', color=color, linewidth=2, label=f'Path {idx + 1}')
            # Mark start and end points
            ax.plot(xs[0], ys[0], marker='o', markersize=12, color='green', markeredgecolor='black')
            ax.plot(xs[-1], ys[-1], marker='o', markersize=12, color='red', markeredgecolor='black')

        # Add labels to squares
        files = 'abcdefgh'
        ranks = '12345678'
        for row in range(8):
            for col in range(8):
                square = f"{files[col]}{row + 1}"
                ax.text(col + 0.5, row + 0.5, square, ha='center', va='center', fontsize=8, color='black')

        # Set axis labels and title
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 8)
        ax.set_title("Knight's Shortest Paths")
        ax.legend()

        # Save the figure
        plt.savefig(f"{filename}.png", bbox_inches='tight')
        plt.savefig(f"{filename}.pdf", bbox_inches='tight')
        logging.info(f"Paths overlaid on chessboard saved as {filename}.png and {filename}.pdf")
        plt.close()

    def create_animation(self, paths, filename='paths'):
        # Load knight image
        knight_image = self.get_knight_image()

        # Create a chessboard
        board_colors = ['#F0D9B5', '#B58863']  # Light and dark squares
        cmap = ListedColormap(board_colors)
        board = [[(row + col) % 2 for col in range(8)] for row in range(8)]

        images = []

        for idx, path in enumerate(paths):
            xs = [coord[1] + 0.5 for coord in path]
            ys = [coord[0] + 0.5 for coord in path]
            for i in range(len(path)):
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.imshow(board, cmap=cmap, extent=(0, 8, 0, 8))
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_xlim(0, 8)
                ax.set_ylim(0, 8)
                # Add labels to squares
                files = 'abcdefgh'
                ranks = '12345678'
                for row in range(8):
                    for col in range(8):
                        square = f"{files[col]}{row + 1}"
                        ax.text(col + 0.5, row + 0.5, square, ha='center', va='center', fontsize=8, color='black')

                # Mark start and end points
                start_x, start_y = xs[0], ys[0]
                end_x, end_y = xs[-1], ys[-1]
                ax.plot(start_x, start_y, marker='o', markersize=12, color='green', markeredgecolor='black')
                ax.plot(end_x, end_y, marker='o', markersize=12, color='red', markeredgecolor='black')

                # Plot path so far
                ax.plot(xs[:i+1], ys[:i+1], marker='o', color='blue', linewidth=2)

                # Place the knight image
                x = xs[i] - 0.5
                y = ys[i] - 0.5
                ax.imshow(knight_image, extent=(x, x + 1, y, y + 1))

                # Capture the frame
                fig.canvas.draw()
                image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
                image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
                images.append(image)
                plt.close(fig)

        # Save as GIF
        imageio.mimsave(f'{filename}.gif', images, fps=1)
        logging.info(f"Animation saved as {filename}.gif")

    def get_knight_image(self):
        import os
        # Create a transparent image
        img = Image.new('RGBA', (100, 100), color=(255, 255, 255, 0))
        d = ImageDraw.Draw(img)
        try:
            # Load the font from the local directory
            font_path = os.path.join(os.path.dirname(__file__), "DejaVuSans.ttf")
            font = ImageFont.truetype(font_path, 80)
            d.text((10, 10), '♘', font=font, fill=(0, 0, 0))
        except IOError as e:
            logging.error(f"Font could not be loaded: {e}")
            # Fallback to a simple 'K' character or handle as needed
            font = ImageFont.load_default()
            d.text((10, 10), 'K', font=font, fill=(0, 0, 0))
        # Convert PIL image to numpy array for matplotlib
        knight_image = np.array(img)
        return knight_image

    @staticmethod
    def alg_to_coord(alg_notation):
        files = 'abcdefgh'
        ranks = '12345678'
        match = re.match(r'^([a-hA-H])([1-8])$', alg_notation)
        if match:
            file_char, rank_char = match.groups()
            col = files.index(file_char.lower())
            row = int(rank_char) - 1  # Adjust for 0-based index
            return (row, col)
        else:
            raise ValueError(f"Invalid algebraic notation: {alg_notation}")

    @staticmethod
    def coord_to_alg(coord):
        files = 'abcdefgh'
        ranks = '12345678'
        row, col = coord
        if 0 <= row < 8 and 0 <= col < 8:
            return f"{files[col]}{row + 1}"  # Adjust for 1-based rank
        else:
            raise ValueError(f"Invalid coordinate: {coord}")

def prompt_for_position(prompt_message, suggestions):
    while True:
        suggestion_text = f"e.g., '{suggestions[0]}' or '{suggestions[1]}'"
        user_input = input(f"{prompt_message} ({suggestion_text}): ").strip()
        if re.match(r'^[a-hA-H][1-8]$', user_input):
            return user_input
        else:
            print("Invalid input. Please enter a valid chess position (a1 to h8).")

def main():
    # Default configuration
    config = {
        "output_file": "paths",
    }

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Knight's Shortest Path Finder")
    parser.add_argument('-s', '--start', help='Starting position (e.g., e4)')
    parser.add_argument('-e', '--end', help='Ending position (e.g., h7)')
    parser.add_argument('-o', '--output', help='Output file name without extension')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    # Update configuration with command-line arguments
    if args.output:
        config['output_file'] = args.output
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Prompt for start and end positions
    positions = [f"{file}{rank}" for file in 'abcdefgh' for rank in '12345678']
    if args.start:
        start_input = args.start
    else:
        suggestions = random.sample(positions, 2)
        start_input = prompt_for_position("Enter the starting position", suggestions)

    if args.end:
        end_input = args.end
    else:
        suggestions = random.sample(positions, 2)
        end_input = prompt_for_position("Enter the ending position", suggestions)

    try:
        # Convert algebraic notation to coordinates
        start_coord = KnightPathFinder.alg_to_coord(start_input)
        end_coord = KnightPathFinder.alg_to_coord(end_input)

        # Initialize and run pathfinder
        finder = KnightPathFinder(start_coord, end_coord)
        paths = finder.bfs_paths()

        if not paths:
            logging.warning(f"No paths found from {start_input} to {end_input}.")
            sys.exit(0)

        # Log the number of paths found
        logging.info(f"Found {len(paths)} shortest path(s) from {start_input} to {end_input}.")

        # Generate Graphviz DOT file
        finder.generate_graphviz(paths, filename=config['output_file'])

        # Draw paths on the chessboard
        finder.draw_paths_on_board(paths, filename=config['output_file'])

        # Create animation GIF
        finder.create_animation(paths, filename=config['output_file'])

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
