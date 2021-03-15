from util import *
import copy


class KernighanLin():
    '''
    Implementation of Kernighan-Lin algorithm
    '''
    
    def __init__(self, n_cells, nets):
        '''
        Initialize with some random partition and set up to current circuit
        '''
        self.n_cells = n_cells
        self.nets = nets
        self.gains = {}
        
        # Get a random starting partition
        self.best_partition = initialize_partition(n_cells)
        # Record current best cost
        self.best_cost = cut_size(self.best_partition, self.nets)
        
        debug_print("Initial Partition: {}".format(format_partition(self.best_partition)))
        debug_print("Initial Cost: {}".format(self.best_cost))
    
    
    def partition(self):
        '''
        Run partitioning algorithm
        '''    
        # Make a copy of initial partition
        self.current_partition = copy.deepcopy(self.best_partition)
        
        # Run algorithm for a number of iterations
        for i in range(initializing_iterations):
            debug_print("Iteration: {}".format(i))
            self.iterate()
        
        # Return best partition
        debug_print("Best partition: {}".format(format_partition(self.best_partition)))
        return self.best_partition


    def iterate(self):
        '''
        Implementation of 1 iteration of the algorithm
        '''
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
            
            # Special case if there are an even number of cells (need to swap 2 at a time to be legal)
            if (self.n_cells % 2 == 0):
                
                while highest_gain not in unlocked_nodes:
                    # Make sure the swap is unlocked
                    del gains[highest_gain]
                    highest_gain = max(gains, key=gains.get)
                    
                debug_print("Chosen {}".format(highest_gain))
                
                # Update the partition
                self.current_partition = self.swap_node(highest_gain, self.current_partition)
                unlocked_nodes.remove(highest_gain)
                debug_print("New partition: {}".format(format_partition(self.current_partition)))
                
                # Choose the next highest gain as the second cell to be swapped
                del gains[highest_gain]
                highest_gain = max(gains, key=gains.get)    
                
            debug_print("Chosen {}".format(highest_gain))
            
            # Update the partition
            self.current_partition = self.swap_node(highest_gain, self.current_partition)
            debug_print("New partition: {}".format(format_partition(self.current_partition)))
                
            # Ensure swap is legal and unlocked
            while not check_legality(self.current_partition, self.n_cells) or highest_gain not in unlocked_nodes:
                debug_print("Reverse {}".format(highest_gain))
                self.current_partition = self.swap_node(highest_gain, self.current_partition)
                debug_print("New partition: {}".format(format_partition(self.current_partition)))
                
                del gains[highest_gain]
                
                # There should be a possible cell to choose, otherwise something is wrong
                if len(gains) == 0:
                    raise Exception
                
                # If previous choice was invalid, choose the next highest gain
                highest_gain = max(gains, key=gains.get)
                debug_print("Chosen {}".format(highest_gain))
                self.current_partition = self.swap_node(highest_gain, self.current_partition)
                debug_print("New partition: {}".format(format_partition(self.current_partition)))
                
            # Move node to other block and lock it
            unlocked_nodes.remove(highest_gain)
            
            # Calculate cost
            cost = cut_size(self.current_partition, self.nets)
            debug_print("Cost: {}".format(cost))
            
            # Choose best cut seen in this pass
            if cost < self.best_cost:
                debug_print("Updated partition. New cost: {}".format(cost))
                self.best_partition = copy.deepcopy(self.current_partition)
                self.best_cost = cost
            

    def swap_node(self, cell, partition):
        '''
        Swap a cell from one side of the partition to the other
        '''
        if cell in partition["left"]:
            partition["left"].remove(cell)
            partition["right"].add(cell)
        else:
            partition["right"].remove(cell)
            partition["left"].add(cell)
            
        return partition


    def calculate_gains(self, partition):
        '''
        Calculate the "gain" value for each cell
        '''
        for cell in range(self.n_cells):
            # Initialize gain to 0
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
                            
                            # If there is a crossing, increment gain
                            if left and other_right or right and other_left:
                                gain += 1
                            # If the connection does not cross the partition, decrement gain
                            else:
                                gain -= 1
                                
            # Record gain value
            self.gains[cell] = gain
            
        debug_print("Gains: {}".format(self.gains))
                                
                        
                        