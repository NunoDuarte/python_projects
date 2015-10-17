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
        self.parent = None;
        self.child = [];
        
        
    def MakeGraph(self, startingNode, graph, tree):
        
        count = 0;
        for i in range(0, len(graph)):
            #print (graph[i].arrival)
            #print (startingNode)
            if graph[i].departure == startingNode:
                if count == 0:
                    node = Node();
                    count = count + 1;
                node.child.append(graph[i])

        tree = node;
            
        #print (tree[0].child[0].arrival)
        return tree
