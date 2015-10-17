class BFS(object):
    
    def __init__(self):
        self.visitedNodes = [];

    
    def bfs_initState(self, graph, initState):
        startingNode = []
        for i in range(0, len(graph)):
            if graph[i].departure == initState:
                startingNode.append(graph[i]);
                
        return startingNode;
        
    def bfs_search(self, startingNode, soughtValue):
        stack = startingNode;
        
        while len(stack) > 0:
            for i in range(0, len(stack)):
                
                #This happens when there is no solution
                if i >= len(stack):
                    return False;
#                 print (i)
#                 print (len(stack))
                node = stack.pop(i)
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
                        #We don't want to go back or do the same cities again
                        if BFS.checkRepeated(self, n):
                            stack.pop()
                    
        return False
    
    
    def checkRepeated(self, n):
        
        check = False;
        for i in range(0, len(self.visitedNodes)):
            if (n.arrival == self.visitedNodes[i].departure) and (n.departure == self.visitedNodes[i].arrival):
                check = True;
        return check