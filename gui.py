import os
import time
from tkinter import *
from tkinter.ttk import *
from settings import *
from util import *
from netlist_parser import *
from branch_bound import *


# Initialize the debug log
debug_log.write("\n\n{}\n".format("="*20))
debug_log.write(time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime()))
debug_log.write("{}\n".format("="*20))


# If only running 1 circuit
if single_circuit:
    
    # Choose circuit
    filename = input("Name of circuit: ")

    # Open circuit
    debug_print("Reading configurations for {}...".format(filename))
    configs, nets = parse_file("./benchmarks/{}.txt".format(filename))

    # Initialize GUI
    root = Tk()
    frame = Frame(root, width=screensize["width"], height=screensize["height"])
    frame.grid(row=0, column=0)
    grid["x"] = (grid["right"] - grid["left"]) / configs["cells"]
    grid["y"] = (grid["bottom"] - grid["top"]) / configs["cells"]
    c = Canvas(frame, bg=background_colour, width=screensize["width"], height=screensize["height"])
    c.pack()

    c.create_text(
        20,
        20,
        text="Circuit: {}".format(filename),
        fill="black",
        font=('Arial',20,'bold'),
        anchor=W
    )
    
    c.create_line(grid["middlex"], grid["top"], grid["middlex"], grid["bottom"], fill=line_colour)

    branch_bound = BranchBound(c)
    branch_bound.setup(configs, nets)

    # Add buttons
    button_frame = Frame(root, width=screensize["width"])
    init_button = Button(button_frame, text ="Initialize", command=branch_bound.initialize_partition)
    
    button_frame.grid(row=1, column=0)
    init_button.grid(row=0, column=0)
    
    
    
# Otherwise, run "benchmark"
else:
    pass
    
    
# Close debug log
debug_log.close()

# Run GUI
root.mainloop()