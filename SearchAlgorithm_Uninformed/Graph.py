class Graph(object):
    
    def __init__(self,):
        self.graph = [];
        self.count = 0;
        self.limitTime = 100000;
        self.limitCost = 100000;
        

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
    
    def checkConstraints(self, graph, client, number):
        
        if number == 1:
            typeA = client[7]
            A = Graph.typeAB(self, client[6]);
            if A == 1:
                count = 0;
                for i in range(0, len(graph)):
                    if graph[i].type == typeA:
                        count = count + 1;
                self.count = count;
                for j in range(0, count):
                    clean = False;
                    for i in range(0, len(graph)):
                        if not clean:
                            if graph[i].type == typeA:
                                graph.pop(i);
                                clean = True;
            if A == 2:
                count = 0;
                for i in range(0, len(graph)):
                    if graph[i].duration > int(typeA):
                        count = count + 1;
                self.count = count;
                for j in range(0, count):
                    clean = False;
                    for i in range(0, len(graph)):
                        if not clean:
                            if graph[i].duration > int(typeA):
                                graph.pop(i);
                                clean = True;
            if A == 3:
                count = 0;
                for i in range(0, len(graph)):
                    if graph[i].cost > int(typeA):
                        count = count + 1;
                self.count = count;
                for j in range(0, count):
                    clean = False;
                    for i in range(0, len(graph)):
                        if not clean:
                            if graph[i].cost > int(typeA):
                                graph.pop(i);
                                clean = True; 
        if number == 2:
            typeA = client[7]
            A = Graph.typeAB(self, client[6]);
            if A == 1:
                count = 0;
                for i in range(0, len(graph)):
                    if graph[i].type == typeA:
                        count = count + 1;
                self.count = count;
                for j in range(0, count):
                    clean = False;
                    for i in range(0, len(graph)):
                        if not clean:
                            if graph[i].type == typeA:
                                graph.pop(i);
                                clean = True;
            if A == 2:
                count = 0;
                for i in range(0, len(graph)):
                    if graph[i].duration > int(typeA):
                        count = count + 1;
                self.count = count;
                for j in range(0, count):
                    clean = False;
                    for i in range(0, len(graph)):
                        if not clean:
                            if graph[i].duration > int(typeA):
                                graph.pop(i);
                                clean = True;
            if A == 3:
                count = 0;
                for i in range(0, len(graph)):
                    if graph[i].cost > int(typeA):
                        count = count + 1;
                self.count = count;
                for j in range(0, count):
                    clean = False;
                    for i in range(0, len(graph)):
                        if not clean:
                            if graph[i].cost > int(typeA):
                                graph.pop(i);
                                clean = True; 
            B = Graph.typeAB(self, client[8]);
            if B == 4:
                self.limitTime = int(client[9]);
            if B == 5:
                self.limitCost = int(client[9]);
            
        return graph;                    
            
            
    def typeAB(self, argument):
        # switch case 
        switch = {
                  'A1': 1,
                  'A2': 2,
                  'A3': 3,
                  'B1': 4,
                  'B2': 5,
                  }
        return switch.get(argument, 'nothing')
    