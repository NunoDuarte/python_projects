class Time(object):
    
    def __init(self,):
        
        self;
        
    def checkTime(self, node, initTime, constraints):
        ##match times correctly
        
        if node.parent:
            node.timeSpent = node.timeSpent + node.parent.timeSpent;
            node.pathCost = node.pathCost + node.parent.pathCost;
            Time = node.initTime;
            while Time < node.timeSpent:
                Time = Time + node.intervals;
            if Time > node.timeSpent:
                node.timeSpent = Time;  
            node.timeSpent = node.timeSpent + (Time - node.timeSpent) + node.duration ;
        else:
            Time = initTime;
            while initTime < node.initTime:
                node.timeSpent = node.timeSpent + node.intervals
                initTime = initTime + node.timeSpent;
            if Time > node.initTime:
                initTime = node.initTime;
                #This means that the clients misses the first flight or boat or train
                while Time > initTime:
                    initTime = initTime + node.intervals;
                node.timeSpent = initTime - Time;
            node.timeSpent = node.timeSpent + node.duration;
            

        node.pathCost = node.pathCost + node.cost;
        
#         if node.pathCost > constraints.limitCost:
#             node.visited = True;
#              
#         if node.timeSpent > constraints.limitTime:
#             node.visited = True;
        
        return node