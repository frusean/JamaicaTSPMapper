Jamaica TSP Solver

Description

Jamaica TSP Solver is a Python application that solves the Traveling Salesman Problem (TSP) for Jamaica's 14 parishes using various algorithms. The project provides an interactive GUI for matrix input and visualizes the resulting routes on static and dynamic maps. It supports Nearest Neighbor, Greedy Best-First Search, and Brute Force algorithms. Routes are displayed using GeoPandas, and interactive maps are generated with Folium.

Features

Algorithms Implemented:

Nearest Neighbor

Greedy Best-First Search

Brute Force (Optimal Solution)

Visualization:

Plot routes dynamically on a GeoPandas map

Generate interactive HTML maps using Folium

Interactive GUI:

Enter distance matrices manually or upload via text files

View total distance and runtime for selected algorithms

Save interactive TSP route maps as HTML

Technologies Used

Python

GeoPandas (for static route visualization)

Folium (for interactive web-based map visualization)

NumPy (for matrix operations)

Matplotlib (for plotting)

Tkinter (GUI for user interaction)

Installation

Clone the repository:

git clone <repo-url>

Navigate to the project directory:

cd jamaica-tsp-solver

Install dependencies:

pip install numpy geopandas matplotlib folium tk

Download Jamaica’s shapefile (update the path in the script to point to your shapefile).

Usage

Run the application:

python tsp_solver.py

Enter the distance matrix manually or upload a text file containing the matrix.

Choose one of the algorithms from the GUI.

View route plots and save interactive Folium maps.

File Structure

jamaica-tsp-solver/
|-- tsp_solver.py              # Main application script
|-- jamaica_shapefile/         # Contains shapefile for GeoPandas
|-- README.md                  # Project documentation
|-- requirements.txt           # List of dependencies

Example

Scenario: Solve TSP for Jamaica’s 14 parishes

Algorithm: Nearest Neighbor

Output:

Visual route connecting all parishes

Total distance and runtime displayed in the GUI

Interactive Folium map saved as HTML

Notes

Ensure the shapefile path is correctly specified in the script.

Folium map will be saved in the project directory as jamaica_tsp_route.html.

 

 

