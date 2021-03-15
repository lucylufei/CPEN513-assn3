from util import *
import copy


class KernighanLin():
    
    def __init__(self, n_cells, nets):
        self.n_cells = n_cells
        self.nets = nets
        
        self.best_partition = initialize_partition(n_cells)
        self.best_cost = cut_size(self.best_partition, self.nets)
        self.gains = {}
        
        debug_print("Initial Partition: {}".format(self.best_partition))
        debug_print("Initial Cost: {}".format(self.best_cost))
    
    def partition(self):
        
        self.current_partition = copy.deepcopy(self.best_partition)
        
        for i in range(initializing_iterations):
            debug_print("Iteration: {}".format(i))
            self.iterate()
        
        debug_print("Best partition: {}".format(self.best_partition))
        return self.best_partition


    def iterate(self):
        
        # Unlock all nodes
        unlocked_nodes = set(range(self.n_cells))
        
        # While some nodes are unlocked
        while len(unlocked_nodes) > 0:
            debug_print("Unlocked nodes: {}".format(unlocked_nodes))
            
            # Calculate all gains
            self.calculate_gains(self.current_partition)
            
            # Choose node with highest gain whose movement would not cause an imbalance
            gains = copy.deepcopy(self.gains)
            highest_gain = max(gains, key=gains.get)
            debug_print("Chosen {}".format(highest_gain))
            
            self.current_partition = self.swap_node(highest_gain, self.current_partition)
            debug_print("New partition: {}".format(self.current_partition))
                
            while not check_legality(self.current_partition, self.n_cells) or highest_gain not in unlocked_nodes:
                debug_print("Reverse {}".format(highest_gain))
                self.current_partition = self.swap_node(highest_gain, self.current_partition)
                debug_print("New partition: {}".format(self.current_partition))
                
                del gains[highest_gain]
                
                if len(gains) == 0:
                    raise Exception
                
                highest_gain = max(gains, key=gains.get)
                debug_print("Chosen {}".format(highest_gain))
                self.current_partition = self.swap_node(highest_gain, self.current_partition)
                debug_print("New partition: {}".format(self.current_partition))
                
            # Move node to other block and lock it
            unlocked_nodes.remove(highest_gain)
            
            cost = cut_size(self.current_partition, self.nets)
            debug_print("Cost: {}".format(cost))
            
            # Choose best cut seen in this pass
            if cost < self.best_cost:
                debug_print("Updated partition. New cost: {}".format(cost))
                self.best_partition = copy.deepcopy(self.current_partition)
                self.best_cost = cost
            
        

    
    def swap_node(self, cell, partition):
        
        if cell in partition["left"]:
            partition["left"].remove(cell)
            partition["right"].add(cell)
        else:
            partition["right"].remove(cell)
            partition["left"].add(cell)
            
        return partition


    def calculate_gains(self, partition):
        
        for cell in range(self.n_cells):
            gain = 0
            left = cell in partition["left"]
            right = cell in partition["right"]
            
            # Check all nets
            for net in self.nets:
                if cell in net:
                    # If cell in net, calculate gain with all other cells
                    for other_cell in net:
                        if other_cell != cell:
                            other_left = other_cell in partition["left"]
                            other_right = other_cell in partition["right"]
                            
                            if left and other_right or right and other_left:
                                gain += 1
                            else:
                                gain -= 1
                                
            self.gains[cell] = gain
            
        debug_print("Gains: {}".format(self.gains))
                                
                        
                        