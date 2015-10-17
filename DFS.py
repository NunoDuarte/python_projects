class DFS(object):
    
    def __init__(self):
        self.visitedNodes = [];

    
    def dfs_initState(self, graph, initState):
        startingNode = []
        for i in range(0, len(graph)):
            if graph[i].departure == initState:
                startingNode.append(graph[i]);
                
        return startingNode;
        
    def dfs_search(self, startingNode, soughtValue):
        stack = startingNode;
        
        while len(stack) > 0:
            node = stack.pop()
#             print (node.departure)
#             print (node.arrival)
            #print ('here')
            if node in self.visitedNodes:
                continue
            
            self.visitedNodes.append(node)
            if node.arrival == soughtValue:
                print (node.arrival)
                print (node.departure)
                while node.departure != self.visitedNodes[0].departure:
                    node = node.parent;
                    print (node.arrival)
                    print (node.departure)
                return True
            
            for n in node.child:
                if n not in self.visitedNodes:
                    n.parent = self.visitedNodes[-1];
                    stack.append(n)
                    if DFS.checkRepeated(self, n):
                        stack.pop()
                    
        return False
    
    def checkRepeated(self, n):
        
        check = False;
        for i in range(0, len(self.visitedNodes)):
            if (n.arrival == self.visitedNodes[i].departure) and (n.departure == self.visitedNodes[i].arrival):
                check = True;
        return check
                 
                        
                   
                
                
        