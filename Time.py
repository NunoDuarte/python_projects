class Time(object):
    
    def __init(self,):
        
        self;
        
    def checkTime(self, node, initTime, constraints):
        ##match times correctly
        Time = initTime;
        while initTime < node.initTime:
            node.timeSpent = node.timeSpent + node.intervals
            initTime = initTime + node.timeSpent;
        if Time > node.initTime:
            node.timeSpent = node.timeSpent + Time;
            
        
        if node.parent:
            node.timeSpent = node.timeSpent + node.parent.timeSpent;
            node.pathCost = node.pathCost + node.parent.pathCost;
        node.timeSpent = node.timeSpent + node.duration;

        node.pathCost = node.pathCost + node.cost;
        
        if node.pathCost > constraints.limitCost:
            node.visited = True;
            
        if node.timeSpent > constraints.limitTime:
            node.visited = True;
        
        return node