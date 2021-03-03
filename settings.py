debug = True
single_circuit = True

debug_log = open("logs/debug.txt", "a+")


# GUI settings
screensize = {
    "width": 1000, 
    "height": 500
}
canvas_border = 50

grid = {}
grid["left"] = canvas_border
grid["right"] = screensize["width"] - canvas_border
grid["top"] = canvas_border
grid["bottom"] = screensize["height"] - canvas_border
grid["middlex"] = grid["left"] + (grid["right"] - grid["left"]) / 2.0
grid["middley"] = grid["top"] + (grid["bottom"] - grid["top"]) / 2.0

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