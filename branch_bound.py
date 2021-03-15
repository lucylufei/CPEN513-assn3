from util import *
from settings import *
from kernighan_lin import *
import copy


class BranchBound():
    def __init__(self, canvas):
        self.c = canvas
        
    def setup(self, configs, nets):
        self.configs = configs
        self.nets = nets
        
        
    def clear(self):
        self.c.delete("cell")
        self.c.delete("wire")
        self.c.delete("cost")
        self.c.delete("node")
        
    def initialize_partition(self):
        if gui:
            self.c.delete("cell")
            self.c.delete("wire")
            self.c.delete("cost")
        
        if initial_partition == "random":
            
            self.partition = initialize_partition(self.configs["cells"])
            self.current_cutsize = cut_size(self.partition, self.nets)
            for i in range(initializing_iterations):
                partition = initialize_partition(self.configs["cells"])
                cost = cut_size(partition, self.nets)
                
                if cost < self.current_cutsize:
                    self.partition = partition
                    self.current_cutsize = cost 
                    
        elif initial_partition == "fixed":
            self.partition = fixed_partition
            self.current_cutsize = cut_size(self.partition, self.nets)
            
        
        elif initial_partition == "clever":
            fm = KernighanLin(self.configs["cells"], self.nets)
            
            self.partition = fm.partition()
            self.current_cutsize = cut_size(self.partition, self.nets)
            
        if gui:
            draw_partition(self.c, self.partition, self.configs, self.nets)
            write_cutsize(self.c, self.current_cutsize)
        
    
    def run_algorithm(self):
        
        self.nodes_visited = 0
        self.leaf_nodes_visited = 0
        self.path = []
        self.generate_tree({"left": [], "right": []}, 0)
        
        print("DONE")
        self.print_results()
        
        if gui:
            self.c.delete("cell")
            self.c.delete("wire")
            self.c.delete("cost")
            draw_partition(self.c, self.partition, self.configs, self.nets)
            write_cutsize(self.c, self.current_cutsize)
            draw_path(self.c, self.path, self.configs["cells"])
        
            self.c.update()
        
    
    def print_results(self):
        print("\nFinal Cutsize: {}\n".format(self.current_cutsize))
        
        print("{nodes} nodes visited out of {total} nodes total ({percent})".format(
            nodes=self.nodes_visited, 
            total=sum([pow(2, row) for row in range(self.configs["cells"]+1)]),
            percent=float(self.nodes_visited) / sum([pow(2, row) for row in range(self.configs["cells"]+1)])
        ))
        print("{nodes} leaf nodes visited out of {total} leaf nodes total ({percent})".format(
            nodes=self.leaf_nodes_visited, 
            total=pow(2, self.configs["cells"]), 
            percent=float(self.leaf_nodes_visited) / pow(2, self.configs["cells"])
        ))
        
        print("Left: {}".format(self.partition["left"]))
        print("Right: {}".format(self.partition["right"]))
        
        
    def write_output(self, out_file):

        out_file.write("\nFinal Partition\n")
        out_file.write("\tLeft: {}\n".format(self.partition["left"]))
        out_file.write("\tRight: {}\n".format(self.partition["right"]))
        
        out_file.write("\nFinal Cutsize: {}\n\n".format(self.current_cutsize))
    
        out_file.write("{nodes} nodes visited out of {total} nodes total ({percent})\n".format(
            nodes=self.nodes_visited, 
            total=sum([pow(2, row) for row in range(self.configs["cells"]+1)]),
            percent=float(self.nodes_visited) / sum([pow(2, row) for row in range(self.configs["cells"]+1)])
        ))
        out_file.write("{nodes} leaf nodes visited out of {total} leaf nodes total ({percent})\n".format(
            nodes=self.leaf_nodes_visited, 
            total=pow(2, self.configs["cells"]), 
            percent=float(self.leaf_nodes_visited) / pow(2, self.configs["cells"])
        ))
        
            
    
    def generate_tree(self, current_assignment, next_node, path=[]):
        if next_node == None:
            self.leaf_nodes_visited += 1
            assert check_legality(current_assignment, self.configs["cells"])
            # Check cost
            cost = cut_size(current_assignment, self.nets)
            if cost < self.current_cutsize:
                self.current_cutsize = cost
                self.partition = current_assignment
                self.path = path
                if gui:
                    draw_node(self.c, path, cost, colour="green")
                debug_print("New partition found! {a} has cost {c}".format(a=format_partition(current_assignment), c=cost))
                debug_print(self.path)
            else:
                if gui:
                    draw_node(self.c, path, cost, colour="red")
                debug_print("Cost {c} higher than lowest cost {l}. {a} pruned.".format(c=cost, l=self.current_cutsize, a=format_partition(current_assignment)))
                
        else:
            self.nodes_visited += 1
            cost = cut_size(current_assignment, self.nets)
            
            if cost < self.current_cutsize:
                if gui:
                    draw_node(self.c, path, cost)
                
                # Left
                temp_current_assignment = copy.deepcopy(current_assignment)
                temp_current_assignment["left"].append(next_node)
                temp_next_node = next_node + 1 if next_node + 1 < self.configs["cells"] else None
                
                temp_path = copy.deepcopy(path)
                temp_path.append("left")
                
                # Check for imbalance (left has more than half (+1) of all nodes)
                if len(temp_current_assignment["left"]) < (self.configs["cells"] / 2 + 1):
                    self.generate_tree(temp_current_assignment, temp_next_node, temp_path)
                else:
                    debug_print("Partition {a} imbalanced. Pruned".format(a=format_partition(temp_current_assignment)))
                
                # Right
                temp_current_assignment = copy.deepcopy(current_assignment)
                temp_current_assignment["right"].append(next_node)
                temp_next_node = next_node + 1 if next_node + 1 < self.configs["cells"] else None
                
                temp_path = copy.deepcopy(path)
                temp_path.append("right")
                
                # Check for imbalance (right has more than half (+1) of all nodes)
                if len(temp_current_assignment["right"]) < (self.configs["cells"] / 2 + 1):
                    self.generate_tree(temp_current_assignment, temp_next_node, temp_path)
                else:
                    debug_print("Partition {a} imbalanced. Pruned".format(a=format_partition(current_assignment)))
                
            else:
                if gui:
                    draw_node(self.c, path, cost, colour="yellow")
                debug_print("Cost {c} higher than lowest cost {l}. {a} pruned.".format(c=cost, l=self.current_cutsize, a=format_partition(current_assignment)))
                
    