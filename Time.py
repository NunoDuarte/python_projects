class Time(object):
    
    def __init(self,):
        
        self;
        
    def checkTime(self, node, initTime):
        ##match times correctly
        
        while initTime < node.initTime:
            node.timeSpent = node.timeSpent + node.intervals
            initTime = initTime + node.timeSpent;
        
        node.timeSpent = node.timeSpent + node.duration;
        
        return node