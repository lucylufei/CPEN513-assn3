from util import *
from settings import *



class BranchBound():
    def __init__(self, canvas):
        self.c = canvas
        
    def setup(self, configs, nets):
        self.configs = configs
        self.nets = nets
        
        
    def initialize_partition(self):
        self.c.delete("cell")
        self.c.delete("wire")
        self.c.delete("cost")
        
        self.partition = initialize_partition(self.configs["cells"])
        draw_partition(self.c, self.partition, self.configs, self.nets)
        self.current_cutsize = cut_size(self.partition, self.nets)
        write_cutsize(self.c, self.current_cutsize)
        
        
    