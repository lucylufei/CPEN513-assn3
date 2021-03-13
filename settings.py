debug = False
single_circuit = True

debug_log = open("logs/debug.txt", "a+")
gui = False
filename = "con1"

save_to_file = True
out_file = None

initial_partition = "random"
initializing_iterations = 10
fixed_partition = {
    "left": [0, 2, 3, 4, 6, 7, 9],
    "right": [1, 5, 8, 10, 11, 12, 13]
}
path = ["left", "right", "left", "left", "left", "right", "left", "left", "right", "left", "right", "right", "right", "right"]

# GUI settings
screensize = {
    "width": 1500, 
    "height": 800
}
canvas_border = 50

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

background_colour = "white"
line_colour = "black"

wire_colour_palette = [
    "pink",
    "plum", 
    "turquoise",
    "lightblue",
    "salmon",
    "lightgreen",
    "lavender",
    "DarkSeaGreen",
    "coral",
    "blue", 
    "green",
    "yellow"
]