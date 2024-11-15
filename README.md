# Chess_Knight_Paths

**Chess_Knight_Paths** is a Python project that calculates all the minimum-length sequences for a knight to move from a starting cell to an ending cell on an empty chessboard. The project accepts positions in algebraic notation and generates comprehensive visualizations of the paths, including:

- **Animated GIFs** showing the knight moving along each path
- **Graphviz DOT files**
- **PDF and PNG images** of the paths overlaid on a chessboard

[**Live Demo**](https://chessknightpaths-v42.streamlit.app/)

<p align="center">
  <img src="Visuals.gif" alt="Knight Paths Animation" width="300"/>
</p>

---

## Table of Contents

- [Features](#features)
- [Live Demo](#live-demo)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Local Installation](#local-installation)
  - [Docker Installation](#docker-installation)
- [Usage](#usage)
  - [Running the Streamlit App](#running-the-streamlit-app)
  - [Running the Script](#running-the-script)
  - [Command-Line Arguments](#command-line-arguments)
  - [Examples](#examples)
- [Output Files](#output-files)
- [Project Structure](#project-structure)
- [Detailed Explanation](#detailed-explanation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [About the Author](#about-the-author)

---

## Features

- **Web Interface with Streamlit**: An interactive web application allowing users to input starting and ending positions and visualize the knight's paths in real-time.
- **User-Friendly Input**: Accepts positions in standard algebraic notation (e.g., `e4`, `h7`).
- **Visualizations**:
  - **Animated GIFs**: Creates animations of the knight moving along each path using a knight chess piece icon.
  - **Graphviz DOT Files**: Represents the shortest paths as graphs with start and end points marked.
  - **Chessboard Images**: Generates PDF and PNG images showing the paths overlaid on a chessboard with start and end points highlighted.
- **Detailed Logging**: Provides informative logs at different verbosity levels for easy debugging and understanding of the process.
- **Error Handling**: Includes comprehensive error handling for invalid inputs and missing dependencies, ensuring the script exits gracefully when issues arise.
- **Cross-Platform Compatibility**: Designed to work on Windows, macOS, and Linux systems.

---

## Live Demo

Experience the application live at: [https://chessknightpaths-v42.streamlit.app/](https://chessknightpaths-v42.streamlit.app/)

---

## Requirements

### Python and Packages

- **Python 3.7** or higher (Note: Streamlit Cloud supports up to Python 3.9)
- **Python Packages** (listed in `requirements.txt`):
  - `streamlit`
  - `matplotlib`
  - `Pillow`
  - `numpy`
  - `imageio`

### System Dependencies

- **Fonts**:
  - **DejaVu Sans**: Used for rendering the knight symbol ('♘') in the animations.
  - Alternatively, any font that supports the '♘' character.

---

## Installation

### Local Installation

#### **Option 1: Using the Provided Zip File**

If you are running the program locally using the provided zip file, the working directory is:

```
C:\Users\YourUsername\Downloads\Project_Submissions_Alvi_Rownok\Part_1\kiwifarm_knight
```

- Replace `YourUsername` with your actual Windows username.
- All commands and executions should be performed within this directory.
- **Important**: To run everything smoothly, **Docker Desktop** should be open and running in the background.

#### **Option 2: Cloning the Repository**

Alternatively, you can clone the repository from GitHub.

##### 1. Clone the Repository

```bash
git clone https://github.com/AlviRownok/Chess_Knight_Paths.git
cd Chess_Knight_Paths
```

##### 2. Install Python Dependencies

It's recommended to use a virtual environment.

###### **Create a Virtual Environment**

```bash
python -m venv venv
```

###### **Activate the Virtual Environment**

- **Windows**:

  ```bash
  venv\Scripts\activate
  ```

- **macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

###### **Install the Dependencies**

```bash
pip install -r requirements.txt
```

---

### Docker Installation

If you prefer to run the project in a Docker container, follow these steps.

#### 1. Install Docker

- **Windows**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
  - **Note**: Ensure that Docker Desktop is installed and open in the background.
- **macOS**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: Install Docker Engine via your package manager.

#### 2. Build the Docker Image

Navigate to the project directory (e.g., `C:\Users\YourUsername\Downloads\Project_Submissions_Alvi_Rownok\Part_1\kiwifarm_knight`), then run:

```bash
docker build -t knight-paths-app .
```

#### 3. Run the Docker Container

```bash
docker run -p 8501:8501 --rm knight-paths-app
```

**Access the App**

After running the Docker container, you can access the Streamlit app in your browser at [http://localhost:8501](http://localhost:8501).

---

## Usage

### Running the Streamlit App

#### **Option 1: Live Demo**

Visit the live demo at [https://chessknightpaths-v42.streamlit.app/](https://chessknightpaths-v42.streamlit.app/) to use the application without any installation.

#### **Option 2: Local Streamlit App**

Run the Streamlit app locally on your machine.

```bash
streamlit run knight_paths.py
```

**Sample Interaction**:

- Enter the starting position (e.g., `e4`).
- Enter the ending position (e.g., `h7`).
- Click the **"Find Paths"** button.
- The animation will appear on the right side of the interface.

### Running the Script

If you prefer to run the script via command line:

#### **Option 1: Interactive Mode**

Simply run the script without arguments, and it will prompt you for input.

```bash
python knight_paths.py
```

**Sample Interaction**:

```
Enter the starting position (e.g., 'd5' or 'a3'): e4
Enter the ending position (e.g., 'h7' or 'b1'): h7
INFO: Found 6 shortest path(s) from e4 to h7.
INFO: Animation displayed in Streamlit app.
```

#### **Option 2: Command-Line Arguments**

You can provide the starting and ending positions, output file name, and verbosity level directly.

```bash
python knight_paths.py -s e4 -e h7 -o knight_paths -v
```

### Command-Line Arguments

```bash
python knight_paths.py [-h] [-s START] [-e END] [-o OUTPUT] [-v]
```

- `-h`, `--help`: Show help message and exit.
- `-s START`, `--start START`: Starting position in algebraic notation (e.g., `e4`).
- `-e END`, `--end END`: Ending position in algebraic notation (e.g., `h7`).
- `-o OUTPUT`, `--output OUTPUT`: Output file name without extension (default: `paths`).
- `-v`, `--verbose`: Enable verbose logging for detailed output.

### Examples

- **Run with default settings and prompts**:

  ```bash
  python knight_paths.py
  ```

- **Specify starting and ending positions**:

  ```bash
  python knight_paths.py -s a1 -e h8
  ```

- **Specify output file name and enable verbose logging**:

  ```bash
  python knight_paths.py -s b2 -e g7 -o knight_paths -v
  ```

---

## Output Files

When running the script via command line, the script can generate the following output files in your project directory:

1. **Animated GIF**: `paths.gif`
   - An animation showing the knight moving along each path.
   - Uses a knight chess piece icon for visualization.

2. **Graphviz DOT File**: `paths.dot`
   - A DOT file representing the shortest paths graphically.
   - Start nodes are marked in green, and end nodes in red.

3. **Chessboard Images**:
   - **PNG Image**: `paths.png`
   - **PDF Document**: `paths.pdf`
   - Visual representations of the paths overlaid on a chessboard.
   - Start positions are highlighted in green, end positions in red.

---

## Project Structure

```
Chess_Knight_Paths/
├── knight_paths.py       # Main script (Streamlit app)
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── .gitignore            # Git ignore file
├── README.md             # Project documentation
├── config.jsonc          # Configuration file (if used)
├── LICENSE               # License information
├── DejaVuSans.ttf        # Font file (if included locally)
└── Visuals.gif           # Sample animated GIF (output)
```

---

## Detailed Explanation

### **Script Workflow**

1. **Input Handling**:
   - The Streamlit app accepts starting and ending positions in algebraic notation via user input fields.

2. **Coordinate Conversion**:
   - Converts algebraic notation to 0-based row and column indices for internal processing.

3. **Path Finding**:
   - Uses Breadth-First Search (BFS) to find all shortest paths from the start to the end position.
   - Only valid knight moves are considered.

4. **Visualization Generation**:
   - **Animated GIF**:
     - Generates frames showing the knight moving along each path step by step.
     - Compiles frames into an animation displayed within the app.
   - **Graphviz DOT File** (when running via command line):
     - Represents paths as graphs.
     - Nodes are chessboard squares.
     - Edges represent knight moves.
   - **Chessboard Images** (when running via command line):
     - Creates an 8x8 grid representing the chessboard.
     - Overlays the paths with different colors.
     - Marks start and end positions distinctly.

5. **Output Files Creation**:
   - Saves the generated visualizations in the specified formats when running via command line.
   - In the Streamlit app, displays the animation directly without saving files.

### **Key Components**

- **KnightPathFinder Class**:
  - Encapsulates the logic for path finding and visualization.
  - Methods include `bfs_paths`, `create_animation`, and utility functions for coordinate conversions.

- **Error Handling**:
  - Validates inputs and provides informative error messages.
  - Handles exceptions during resource loading.

- **Logging**:
  - Uses Python's `logging` module to provide status updates and debug information.
  - Verbose mode (`-v`) enables detailed logs.

---

## Troubleshooting

### **Common Issues and Solutions**

- **Font Loading Error**:
  - **Error Message**: `Font could not be loaded: cannot open resource`
  - **Solution**: Ensure the `DejaVuSans.ttf` font is included in your project directory. Modify the font path in the script if necessary.

- **Knight Image Not Displaying**:
  - **Issue**: The knight symbol does not appear in the animations.
  - **Solution**: Verify that the font used supports the '♘' character or use an image file for the knight.

- **Dependencies Not Installed**:
  - **Error Message**: `ModuleNotFoundError: No module named 'module_name'`
  - **Solution**: Install missing dependencies using `pip install -r requirements.txt`.

- **Streamlit App Not Loading**:
  - **Issue**: The app does not load when running locally.
  - **Solution**: Ensure all dependencies are installed and that you are using the correct Python version.

- **Docker Container Exits Immediately**:
  - **Issue**: The Docker container stops running shortly after starting.
  - **Solution**:
    - Ensure that Docker Desktop is open and running in the background.
    - Check the container logs for error messages using:

      ```bash
      docker logs knight-paths-app
      ```

---

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. **Fork the Repository**: Click the "Fork" button on the GitHub page.

2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/your_username/Chess_Knight_Paths.git
   ```

3. **Create a New Branch**:

   ```bash
   git checkout -b feature/your_feature_name
   ```

4. **Make Your Changes**: Implement your feature or fix.

5. **Commit Your Changes**:

   ```bash
   git commit -am "Add your commit message here"
   ```

6. **Push to Your Fork**:

   ```bash
   git push origin feature/your_feature_name
   ```

7. **Submit a Pull Request**: Go to the original repository and open a pull request.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- **Streamlit**: For providing an easy way to create interactive web applications.
- **Matplotlib**: For making data visualization in Python accessible and versatile.
- **Pillow**: For easy image creation and manipulation.
- **Contributors**: Thank you to everyone who has contributed to this project.

---

## About the Author

**Name**: Alvi Rownok  
**Email**: [alvi2241998@gmail.com](mailto:alvi2241998@gmail.com)  
**LinkedIn**: [https://www.linkedin.com/in/alvi-rownok/](https://www.linkedin.com/in/alvi-rownok/)

---

Feel free to reach out if you have any questions or need further assistance with the **Chess_Knight_Paths** project. Enjoy exploring the fascinating paths of the knight!