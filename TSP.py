
import numpy as np
import time
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from itertools import permutations
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import folium
import os

# Reordered list of Jamaica's 14 Parishes
parishes = [
    "Hanover", "Westmoreland", "St. James", "St. Elizabeth", "Manchester",
    "Trelawny", "Clarendon", "St Ann", "St Catherine", "St Mary",
    "St Andrew", "Kingston", "Portland", "St Thomas"
]

# Coordinates for Jamaican parishes (latitude, longitude)
parish_coordinates = {
    "Hanover": (18.417, -78.133),
    "Westmoreland": (18.242, -78.010),
    "St. James": (18.471, -77.920),
    "St. Elizabeth": (18.038, -77.737),
    "Manchester": (18.042, -77.508),
    "Trelawny": (18.282, -77.657),
    "Clarendon": (17.964, -77.245),
    "St Ann": (18.429, -77.200),
    "St Catherine": (18.012, -76.949),
    "St Mary": (18.267, -76.896),
    "St Andrew": (18.002, -76.791),
    "Kingston": (17.970, -76.788),
    "Portland": (18.176, -76.398),
    "St Thomas": (17.941, -76.339)
}

# Define algorithms
def nearest_neighbor_algorithm(distance_matrix):
    num_parishes = len(distance_matrix)
    visited = [False] * num_parishes
    tour = []
    total_distance = 0

    current_parish = 0
    tour.append(current_parish)
    visited[current_parish] = True

    for _ in range(num_parishes - 1):
        nearest_distance = float('inf')
        next_parish = None

        for j in range(num_parishes):
            if not visited[j] and 0 < distance_matrix[current_parish][j] < nearest_distance:
                nearest_distance = distance_matrix[current_parish][j]
                next_parish = j

        if next_parish is None:
            raise ValueError("No unvisited parish found. The matrix may be incomplete.")

        tour.append(next_parish)
        visited[next_parish] = True
        total_distance += nearest_distance
        current_parish = next_parish

    total_distance += distance_matrix[current_parish][tour[0]]
    tour.append(tour[0])  # Return to the start
    return tour, total_distance

def greedy_best_first_algorithm(distance_matrix):
    num_parishes = len(distance_matrix)
    visited = [False] * num_parishes
    tour = []
    total_distance = 0

    current_parish = 0
    tour.append(current_parish)
    visited[current_parish] = True

    for _ in range(num_parishes - 1):
        next_parish = None
        heuristic_value = float('inf')

        for j in range(num_parishes):
            if not visited[j]:
                if distance_matrix[current_parish][j] < heuristic_value:
                    heuristic_value = distance_matrix[current_parish][j]
                    next_parish = j

        if next_parish is None:
            raise ValueError("No unvisited parish found. The matrix may be incomplete.")

        tour.append(next_parish)
        visited[next_parish] = True
        total_distance += heuristic_value
        current_parish = next_parish

    total_distance += distance_matrix[current_parish][tour[0]]
    tour.append(tour[0])

    return tour, total_distance

def brute_force_tsp(distance_matrix):
    num_parishes = len(distance_matrix)
    all_parishes = list(range(num_parishes))  # Create a list of parish indices (0, 1, 2, ..., num_parishes-1)
    best_tour = None
    min_distance = float('inf')

    for perm in permutations(all_parishes[1:]):  # Fix the starting parish as 0 (Hanover)
        perm = (0,) + perm  # Always start from the first parish (Hanover, index 0)
        total_distance = 0

        for i in range(len(perm) - 1):
            total_distance += distance_matrix[perm[i]][perm[i + 1]]

        total_distance += distance_matrix[perm[-1]][perm[0]]  # Return to the start (Hanover)

        if total_distance < min_distance:
            min_distance = total_distance
            best_tour = perm

    best_tour = best_tour + (0,)
    return best_tour, min_distance

# Function to load distance matrix from file or manual input
def load_distance_matrix(file_path=None):
    if file_path:
        try:
            matrix = np.loadtxt(file_path)
            return matrix
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
            return None
    else:
        try:
            matrix_input = matrix_textbox.get("1.0", tk.END).strip()
            rows = int(row_entry.get())  # Number of rows as entered by the user
            matrix_lines = matrix_input.split('\n')
            if len(matrix_lines) != rows:
                raise ValueError(f"Expected {rows} rows but found {len(matrix_lines)} rows.")
            matrix = [list(map(int, line.split())) for line in matrix_lines]
            return np.array(matrix)
        except ValueError as e:
            messagebox.showerror("Error", f"ValueError: {e}. Please enter valid numbers.")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            return None

# Function to browse and upload a matrix file
def browse_file():
    file_path = filedialog.askopenfilename(title="Select Matrix File to Upload", filetypes=(("Text Files", "*.txt"),))
    if file_path:
        selected_file_label.config(text=file_path)
        matrix = load_distance_matrix(file_path)
        if matrix is not None:
            start_algorithm(matrix)

# Plot TSP Route on a Geographical Map Using GeoPandas
def plot_tsp_route_geopandas(tour, distance_matrix):
    try:
        jamaica_map = gpd.read_file(
            r"C:/Users/fruse/Downloads/Jamaica TSP Mapper/gadm41_JAM_shp/gadm41_JAM_0.shp")  # replace with your unique path or code won't execute

        fig, ax = plt.subplots(figsize=(15, 15))

        jamaica_map.plot(ax=ax, color='lightgray')

        tour_coords = [parish_coordinates[parishes[i]] for i in tour]

        for i in range(len(tour_coords) - 1):
            start = tour_coords[i]
            end = tour_coords[i + 1]
            line = Line2D([start[1], end[1]], [start[0], end[0]], color='red', linewidth=2)
            ax.add_line(line)

            distance = distance_matrix[tour[i]][tour[i + 1]]
            mid_point_lon = (start[1] + end[1]) / 2
            mid_point_lat = (start[0] + end[0]) / 2
            ax.text(mid_point_lon, mid_point_lat, f'{distance} km', color='green', fontsize=12)

        start_point = tour_coords[0]
        ax.scatter(start_point[1], start_point[0], marker='o', color='yellow', s=250, label="Start/End (Hanover)")

        for parish, (lat, lon) in parish_coordinates.items():
            ax.scatter(lon, lat, marker='o', color='blue', s=100)
            ax.text(lon, lat, parish, fontsize=12, ha='right')

        ax.set_xlim([-78.5, -76.0])
        ax.set_ylim([17.7, 18.5])

        plt.title("TSP Route for Parishes in Jamaica", fontsize=16)
        plt.xlabel("Longitude", fontsize=14)
        plt.ylabel("Latitude", fontsize=14)
        plt.legend()
        plt.show()
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}. Please check the shapefile path.")
    except Exception as e:
        print(f"An unexpected error occurred while plotting the route: {e}")

# Function to save Folium map without opening the browser
def save_folium_map(jamaica_map):
    file_path = os.path.abspath("jamaica_tsp_route.html")
    jamaica_map.save(file_path)
    print(f"Map saved at: {file_path}. You can open this file in a browser to view the route.")

# Folium Plot Function
def plot_tsp_route_folium(tour):
    jamaica_map = folium.Map(location=[18.1096, -77.2975], zoom_start=8)
    tour_coords = [parish_coordinates[parishes[i]] for i in tour]

    # Add markers for each parish
    for parish, (lat, lon) in parish_coordinates.items():
        folium.Marker(
            location=[lat, lon],
            popup=parish,
            icon=folium.Icon(color="blue")
        ).add_to(jamaica_map)

    # Draw lines between each point in the tour
    folium.PolyLine(
        locations=[(lat, lon) for lat, lon in tour_coords],
        color="red",
        weight=2.5,
        opacity=0.8
    ).add_to(jamaica_map)

    # Mark starting and ending points differently
    start_point = tour_coords[0]
    folium.Marker(
        location=start_point,
        popup="Start/End (Hanover)",
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(jamaica_map)

    save_folium_map(jamaica_map)  # Save map without opening the browser

# Start the algorithm based on selection
def start_algorithm(distance_matrix):
    selected_algorithm = algorithm_var.get()

    start_time = time.time()

    if selected_algorithm == "Nearest Neighbor":
        tour, distance = nearest_neighbor_algorithm(distance_matrix)
    elif selected_algorithm == "Greedy Best-First":
        tour, distance = greedy_best_first_algorithm(distance_matrix)
    elif selected_algorithm == "Brute Force":
        tour, distance = brute_force_tsp(distance_matrix)
    else:
        messagebox.showerror("Error", "Invalid algorithm selection")
        return

    end_time = time.time()
    runtime = end_time - start_time

    tour_names = [parishes[i] for i in tour]
    display_results_gui(tour_names, distance, runtime)

    plot_tsp_route_geopandas(tour, distance_matrix)
    plot_tsp_route_folium(tour)  # Save updated map without opening the browser

    ask_to_rerun()  # Ask to rerun or exit after each test

# Ask the user if they want to rerun another algorithm or exit
def ask_to_rerun():
    retry = messagebox.askyesno("Retry?", "Do you want to try another algorithm?")
    if retry:
        reset_gui()  # Reset the interface for a new run
    else:
        exit_program()  # Exit the program

# Reset the GUI to allow the user to test another algorithm
def reset_gui():
    matrix_textbox.delete('1.0', tk.END)  # Clear the matrix input
    row_entry.delete(0, tk.END)  # Clear the number of rows entry
    selected_file_label.config(text="")  # Clear the file upload label

# Exit the program
def exit_program():
    root.quit()

# GUI Function to create the main window
def create_gui():
    global algorithm_var, matrix_textbox, selected_file_label, row_entry, root

    root = tk.Tk()
    root.title("TSP Solver")

    # Heading for the application
    tk.Label(root, text="Traveling Salesman Problem (TSP)", font=("Helvetica", 16, "bold")).pack(pady=10)

    # Create a frame for centering the algorithm selection
    center_frame = tk.Frame(root)
    center_frame.pack(pady=10)

    tk.Label(center_frame, text="Please Select One of the Following Algorithm:", font=("Helvetica", 12)).pack(pady=5)
    algorithm_var = tk.StringVar(value="Nearest Neighbor")
    algorithms = ["Nearest Neighbor", "Greedy Best-First", "Brute Force"]
    for algo in algorithms:
        ttk.Radiobutton(center_frame, text=algo, variable=algorithm_var, value=algo).pack(anchor=tk.W, pady=2)

    # Input for the number of rows in the matrix
    tk.Label(center_frame, text="Number of Rows in Matrix:", font=("Helvetica", 12)).pack(pady=5)
    row_entry = ttk.Entry(center_frame)
    row_entry.pack(pady=5)

    tk.Label(center_frame, text="Enter Distance Matrix (space-separated rows):", font=("Helvetica", 12)).pack(pady=5)

    matrix_textbox = tk.Text(center_frame, height=10, width=50)
    matrix_textbox.pack(pady=5)

    tk.Label(center_frame, text="Or Upload a Matrix File:", font=("Helvetica", 12)).pack(pady=5)
    ttk.Button(center_frame, text="Browse File", command=browse_file).pack(pady=5)

    selected_file_label = tk.Label(center_frame, text="", font=("Helvetica", 10), fg="blue")
    selected_file_label.pack(pady=5)

    ttk.Button(center_frame, text="Run Algorithm", command=lambda: start_algorithm(load_distance_matrix())).pack(
        pady=10)

    root.mainloop()

# Display results in GUI
def display_results_gui(tour, distance, runtime):
    result_root = tk.Toplevel()
    result_root.title("TSP Results")

    tour_label = tk.Label(result_root, text="Tour: " + ' -> '.join(tour), font=('Helvetica', 12))
    tour_label.pack(pady=10)

    distance_label = tk.Label(result_root, text=f"Total Distance: {distance:.2f} km", font=('Helvetica', 12))
    distance_label.pack(pady=10)

    runtime_label = tk.Label(result_root, text=f"Runtime: {runtime:.6f} seconds", font=('Helvetica', 12))
    runtime_label.pack(pady=10)

    close_button = ttk.Button(result_root, text="Close", command=result_root.destroy)
    close_button.pack(pady=20)

if __name__ == "__main__":
    create_gui()
