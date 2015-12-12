class Node(object):
    
    #Every VAR is a Node of the Graph
    def __init__(self,):
        
        self.name = 0;
        self.values = [];
        self.alias = 0;
        self.parents = [];
        
        self.table = {}
        
        self.neighbors = 0
        #nodes that are children and so this node is parent
        self.childs = []
