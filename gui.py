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

    # Open circuit
    debug_print("Reading configurations for {}...".format(filename))
    configs, nets = parse_file("./benchmarks/{}.txt".format(filename))

    # Initialize GUI
    if gui:
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
    
    else:
        branch_bound = BranchBound(None)
        
    branch_bound.setup(configs, nets)

    if gui:
        # Add buttons
        button_frame = Frame(root, width=screensize["width"])
        init_button = Button(button_frame, text ="Initialize", command=branch_bound.initialize_partition)
        run_button = Button(button_frame, text ="Run", command=branch_bound.run_algorithm)
        
        button_frame.grid(row=1, column=0)
        init_button.grid(row=0, column=0)
        run_button.grid(row=0, column=1)
        
    else:
        out_file_name = "logs/Results__{}".format(time.strftime("%m-%d_%H-%M-%S", time.localtime()))
        out_file = open(out_file_name, "w+")
        out_file.write("Initialization Iterations: {}\n".format(initializing_iterations))
        
        branch_bound.initialize_partition()
        
        out_file = open(out_file_name, "a+")
        out_file.write("="*40)
        out_file.write("\nCircuit: {}\n".format(filename))
        out_file.write("\nInitial Partition\n")
        out_file.write("\tLeft: {}\n".format(branch_bound.partition["left"]))
        out_file.write("\tRight: {}\n".format(branch_bound.partition["right"]))
        out_file.close()
        
        branch_bound.run_algorithm()
        
        out_file = open(out_file_name, "a+")
        branch_bound.write_output(out_file)
        out_file.close()
        
        
    
# Otherwise, run "benchmark"
else:
    
    out_file_name = "logs/Results__{}".format(time.strftime("%m-%d_%H-%M-%S", time.localtime()))
    out_file = open(out_file_name, "w+")
    out_file.write("Initialization Iterations: {}\n".format(initializing_iterations))
    
    # Get all benchmark files
    benchmarks = [f.replace(".txt", "") for f in os.listdir("benchmarks") if ".txt" in f]
    out_file.write("Benchmarks: {}\n".format(benchmarks))
    out_file.close()
    
    # Initialize GUI
    root = Tk()
    frame = Frame(root, width=screensize["width"], height=screensize["height"])
    frame.grid(row=0, column=0)
    c = Canvas(frame, bg=background_colour, width=screensize["width"], height=screensize["height"])
    c.pack()
    
    c.create_line(grid["middlex"], grid["top"], grid["middlex"], grid["bottom"], fill=line_colour)

    branch_bound = BranchBound(c)

    # Add buttons
    button_frame = Frame(root, width=screensize["width"])
    init_button = Button(button_frame, text ="Initialize", command=branch_bound.initialize_partition)
    run_button = Button(button_frame, text ="Run", command=branch_bound.run_algorithm)
    
    button_frame.grid(row=1, column=0)
    init_button.grid(row=0, column=0)
    run_button.grid(row=0, column=1)
    
    for benchmark in benchmarks:
        c.delete("circuit")
        
        # Open circuit
        debug_print("Reading configurations for {}...".format(benchmark))
        configs, nets = parse_file("./benchmarks/{}.txt".format(benchmark))
        grid["x"] = (grid["right"] - grid["left"]) / configs["cells"]
        grid["y"] = (grid["bottom"] - grid["top"]) / configs["cells"]
        
        branch_bound.setup(configs, nets)

        c.create_text(
            20,
            20,
            text="Circuit: {}".format(benchmark),
            fill="black",
            font=('Arial',20,'bold'),
            anchor=W,
            tag="circuit"
        )
        
        branch_bound.initialize_partition()
        out_file = open(out_file_name, "a+")
        out_file.write("="*40)
        out_file.write("\nCircuit: {}\n".format(benchmark))
        out_file.write("\nInitial Partition\n")
        out_file.write("\tLeft: {}\n".format(branch_bound.partition["left"]))
        out_file.write("\tRight: {}\n".format(branch_bound.partition["right"]))
        out_file.close()
        
        branch_bound.run_algorithm()
        out_file = open(out_file_name, "a+")
        branch_bound.write_output(out_file)
        out_file.close()
        
        time.sleep(5)
        
        branch_bound.clear()
        
    c.delete("circuit")
    c.create_text(
        20,
        20,
        text="DONE",
        fill="black",
        font=('Arial',20,'bold'),
        anchor=W
    )
    

# Run GUI
if gui:
    root.mainloop()
    
# Close debug log
debug_log.close()