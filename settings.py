# Print debug messages
debug = False
debug_log = open("logs/debug.txt", "a+")

# Run a 1 circuit only
single_circuit = True
# Circuit to run (if running 1 circuit only)
circuit_name = "con1"

# Show GUI
gui = True

# Global variable for output file (ignore)
out_file = None

# Settings for initial partition
# "random", "fixed", "clever"
initial_partition = "random"
# Number of iterations for initialization
initializing_iterations = 15
# Manually enter an initial partition
fixed_partition = {
    "left": [0, 1, 3, 5, 6, 8, 9, 11, 12, 14, 16, 17, 20, 23, 24, 26, 29, 33, 37, 38, 41, 43, 45, 46, 47, 48, 49, 50, 51, 53, 54, 57, 61, 63, 68],
    "right": [2, 4, 7, 10, 13, 15, 18, 19, 21, 22, 25, 27, 28, 30, 31, 32, 34, 35, 36, 39, 40, 42, 44, 52, 55, 56, 58, 59, 60, 62, 64, 65, 66, 67, 69]
}

# GUI settings
screensize = {
    "width": 1500, 
    "height": 800
}
canvas_border = 50

background_colour = "white"
line_colour = "black"

# Grid calculations
grid = {}
grid["left"] = canvas_border
grid["right"] = screensize["width"] / 2 - canvas_border
grid["top"] = canvas_border
grid["bottom"] = screensize["height"] - canvas_border
grid["middlex"] = grid["left"] + (grid["right"] - grid["left"]) / 2.0
grid["middley"] = grid["top"] + (grid["bottom"] - grid["top"]) / 2.0

grid2 = {}
grid2["left"] = screensize["width"] / 2 + canvas_border
grid2["right"] = screensize["width"] - canvas_border
grid2["top"] = canvas_border
grid2["bottom"] = screensize["height"] - canvas_border
