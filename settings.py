# Print debug messages
debug = False
debug_log = open("logs/debug.txt", "a+")

# Run a 1 circuit only
single_circuit = True
# Circuit to run (if running 1 circuit only)
filename = "z4ml"

# Show GUI
gui = True

# Global variable for output file
out_file = None

# Settings for initial partition
# "random", "fixed", "clever"
initial_partition = "clever"
# Number of iterations for initialization
initializing_iterations = 15
# Manually enter an initial partition
fixed_partition = {
    "left": [0, 2, 3, 4, 6, 7, 9],
    "right": [1, 5, 8, 10, 11, 12, 13]
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
