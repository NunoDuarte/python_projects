class Graph(object):
    
    def __init__(self,):
        self.graph = [];
        

    def MakeGraph(self, Connect, startingNode, graph):
        
        count = 0;
        for i in range(0, len(graph)):
            #print (graph[i].arrival)
            #print (startingNode)
            if startingNode == graph[i].departure:
                if count == 0:
                    j = Connect;
                    count = count + 1;
                graph[j].child.append(graph[i])
                #graph[j].parent.append(graph[i])
            
        #print (tree[0].child[0].arrival)
        return graph;
