from Time import Time

class DFS(object):
    
    def __init__(self):
        self.visitedNodes = [];
        self.Time = Time()
        self.limitTime = 100000;
        self.limitCost = 100000;

    
    def dfs_initState(self, graph, initState, initTime):
        startingNode = []
        for i in range(0, len(graph)):
            if graph[i].departure == initState:
                startingNode.append(graph[i]);
                startingNode[-1] = self.Time.checkTime(startingNode[-1], initTime, self)                
                
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
                time = node.timeSpent;                
                cost = int(node.cost);
                output = node.departure + ' ' + node.type + ' ' + node.arrival
                while node.departure != self.visitedNodes[0].departure:
                    node = node.parent;
                    cost = cost + int(node.cost)
                    output = node.departure + ' ' + node.type + ' ' + output
                output = output + ' ' + str(time) + ' ' + str(cost) 
                return output
            
            for n in node.child:
                if DFS.checkIfInStack(self, n, stack):
                    continue
                if n not in self.visitedNodes:
                    n.parent = self.visitedNodes[-1];
                    stack.append(n)
                    stack[-1] = self.Time.checkTime(stack[-1], n.parent.initTime, self)    
                    if stack[-1].visited:
                        stack.pop();
                        continue;                
                    if DFS.checkRepeated(self, n):
                        stack.pop()
                    
        return False
    
    def checkRepeated(self, n):
        check = False;
        for i in range(0, len(self.visitedNodes)):
            if (n.arrival == self.visitedNodes[i].departure) and (n.departure == self.visitedNodes[i].arrival):
                check = True;
        return check
    
    def checkIfInStack(self, n, stack):
        check = False;
        if n in stack:
            check = True;
        return check
                        
                 
                        
                   
                
                
        