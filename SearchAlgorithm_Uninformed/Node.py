class Node(object):
    
    def __init__(self,):
        
        self.departure = 0;
        self.arrival = 0;
        self.type = 'comboio';
        self.cost = 0;
        self.duration = 0;
        self.initTime = 0;
        self.finTime = 0;
        self.intervals = 0;
        
        self.visited = False;

        self.parent = [];
        self.child = [];

        self.pathCost = 0;
        self.timeSpent = 0;        