from Time import Time

class A_star(object):
    
    def __init__(self):
        self.visitedNodes = [];
        self.Time = Time();
        self.limitTime = 100000;
        self.limitCost = 100000;
        self.min = 'tempo';

    
    def aStar_initState(self, graph, initState, initTime):
        startingNode = []
        for i in range(0, len(graph)):
            if graph[i].departure == initState:
                startingNode.append(graph[i]);
                startingNode[-1] = self.Time.checkTime(startingNode[-1], initTime, self)
                
        return startingNode;
        
    def aStar(self, startingNode, soughtValue):
        stack = startingNode;
        
        solutions = [];
        
        while len(stack) > 0:
            for i in range(0, len(stack)):
                
                node = stack.pop(0)
                if node in self.visitedNodes:
                    continue
                
                self.visitedNodes.append(node)
                if node.arrival == soughtValue:
                    solutions.append(node);
                    continue
                
                for n in node.child:
                    if n not in self.visitedNodes:
                        n.parent = self.visitedNodes[-1];
                        stack.append(n)
                        stack[-1] = self.Time.checkTime(stack[-1], n.parent.timeSpent, self)
                        if stack[-1].visited or A_star.checkRepeated(self, n):
                            stack.pop();
                        #We don't want to go back or do the same cities again
        if not solutions:
            return False;
        else:
            node = A_star.checkMin(self, solutions, self.min);
            time = node.timeSpent;                
            cost = int(node.cost);
            output = node.departure + ' ' + node.type + ' ' + node.arrival
            while node.departure != self.visitedNodes[0].departure:
                node = node.parent;
                cost = cost + int(node.cost)
                output = node.departure + ' ' + node.type + ' ' + output
            output = output + ' ' + str(time) + ' ' + str(cost) 
            return output
            
    
    
    def checkRepeated(self, n):
        
        check = False;
        for i in range(0, len(self.visitedNodes)):
            if (n.arrival == self.visitedNodes[i].departure) and (n.departure == self.visitedNodes[i].arrival):
                check = True;
        return check
    
    def checkMin(self, graph, minimizing):
        
        if minimizing == 'tempo':
            timeSpent = graph[0].timeSpent;
            path = graph[0];
            for node in graph:
                if node.timeSpent < timeSpent:
                    path = node;
            return path
        if minimizing == 'custo':
            pathCost = graph[0].pathCost;
            path = graph[0];
            for node in graph:
                if node.pathCost < pathCost:
                    path = node;
            return path
        
        
                
            
    
    