class BN(object):
    
    def __init__(self, graph, query_variable):
        
        self.graph = graph
        self.q_variable = query_variable;
        
    
    def run(self, ):
        
        #find hidden variables
        hidden = BN.hidden(self)
        
        if not hidden:
            print (' no hidden variable')
        
        #now an elimination ordering needs to be determined
        hidden = BN.min_neighbors(self, hidden, self.graph)
        
        #auxiliary graph
        aux_graph = self.graph;
        
        
        
        
        
    def hidden(self):
        #returns the hidden variables
        
        graph = self.graph
        query = self.q_variable.query
        evidence = self.q_variable.evidence
        
        hidden = [];
        
        for i in range(0, len(graph)):
            count = 0
            
            if not(graph[i].name == query or graph[i].alias == query):
        
                for j in evidence:
                    
                    if not (graph[i].name == j or graph[i].alias == j):
                        count = count + 1
            
            #checks if none of the evidence variables are equal to the variable being checked as hidden variable
            if count == len(evidence):
                hidden.append(graph[i])
        
        return hidden
    
    def min_neighbors(self, hidden, graph):
        #heuristic function to the determine the elimination ordering
        #inputs:
        #hidden variables
        #the graph of the problem
        
        
        for i in range(0, len(hidden)):
            
            #reset count
            count = 0;
            
            #sum the number of parents has neighbors
            count = len(hidden[i].parents)
            
            #check if the hidden variables has any children
            for j in range(0, len(graph)):
                
                if graph[j].parents:
                    for k in range(0, len(graph[j].parents)):
                        if graph[j].parents[k] == hidden[i].name or graph[j].parents[k] == hidden[i].alias:
                            count = count + 1
                        
            hidden[i].neighbors = count;
            
        
        return hidden
            
            
            
                    
                        
                        
                        
                    
                    
        