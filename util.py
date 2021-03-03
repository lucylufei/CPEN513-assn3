from settings import *
import random
import matplotlib
from matplotlib import cm

def debug_print(content):
    '''
    Special print statement (prints only in debug mode, otherwise logs to file)
    Input:
        content - content to be printed
    '''
    if debug:
        print(content)
    else:
        debug_log.write(str(content))
        debug_log.write("\n")
        
        
def initialize_partition(n_cells):
    '''
    Basic random initialization
    '''
    cells = list(range(0, n_cells))
    partition = {}
    partition["left"] = set()
    partition["right"] = set()
    
    while len(cells) > 0:
        cell = random.choice(cells)
        cells.remove(cell)
        partition["left"].add(cell)
        
        if len(cells) > 0:
            cell = random.choice(cells)
            cells.remove(cell)
            partition["right"].add(cell)
            
    assert abs(len(partition["left"]) - len(partition["right"])) <= 1
    
    debug_print("Partition Left: {}".format(partition["left"]))
    debug_print("Partition Right: {}".format(partition["right"]))
    
    return partition     
        
        
def draw_partition(canvas, partition, configs, nets):
    
    half = int(round(configs["cells"] / 2))
    left_partition = [(x, y) for x in range(0, half) for y in range(0, configs["cells"])]
    right_partition = [(x, y) for x in range(0, half) for y in range(0, configs["cells"])]
    
    cells = {}
    
    for cell in partition["left"]:
        coord = random.choice(left_partition)
        left_partition.remove(coord)
        draw_circle(canvas, coord[0], coord[1], tag="cell")
        cells[cell] = coord
        
    for cell in partition["right"]:
        coord = random.choice(right_partition)
        right_partition.remove(coord)
        draw_circle(canvas, coord[0]+half, coord[1], tag="cell")
        cells[cell] = (coord[0]+half, coord[1])
            
    debug_print(cells)
    
    colour_range = 1.0 / len(nets)
            
    for i, net in enumerate(nets):
        orig = net[0]
        for cell in net[1:]:
            dest = cell
            draw_line(cells[orig], cells[dest], canvas, grid, colour=matplotlib.colors.to_hex(cm.hsv(i*colour_range)), tag="wire")
        
        
        
def draw_circle(c, x, y, color="black", tag=None, size=20):
    
    x_left = grid["left"] + x * grid["x"]
    y_top = grid["top"] + y * grid["y"]
    x_right = x_left + size
    y_bottom = y_top + size
    
    c.create_oval(
        x_left, y_top, x_right, y_bottom, 
        fill=color,
        tag=tag
    )
    
    
        
def draw_line(orig, dest, c, grid, colour="gray", tag="", size=20):
    '''
    Draw a line from (orig) to (dest) on canvas (c) using (grid) with (colour) and (tag)
    extra_point to draw a curve instead of a straight line 
    '''
    
    # Calculate starting position and end positions on the canvas grid
    start_x = grid["left"] + orig[0] * grid["x"] + size/2
    start_y = grid["top"] + orig[1] * grid["y"] + size/2
    end_x = grid["left"] + dest[0] * grid["x"] + size/2
    end_y = grid["top"] + dest[1] * grid["y"] + size/2
    
    # Draw line
    c.create_line(
        start_x, 
        start_y, 
        end_x,
        end_y,
        width=3,
        fill=colour,
        tag=tag
    )


def cut_size(partition, nets):
    
    cut_size = 0
    
    for net in nets:
        left = net[0] in partition["left"]
        
        for cell in net[1:]:
            right = cell in partition["right"]
            
            if (left and right) or (not left and not right):
                cut_size += 1
                break
            
    return cut_size
    
    
def write_cutsize(c, cut_size):
    c.delete("cost")
    c.create_text(
        grid["right"] - 100,
        20,
        text="Cost: {}".format(cut_size),
        fill="black",
        font=('Arial',20,'bold'),
        tag="cost"
    )