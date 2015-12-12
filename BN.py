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
        hidden = BN.min_neighbors(self, hidden, self.graph, 0)
        
        #auxiliary graph
        aux_graph = self.graph;
        
            
        #BN.VE_alg(self, aux_graph, hidden, self.q_variable)
        

    def VE_alg(self, graph, hidden, q_variable, probability):
        
        #start with the hidden variable with the lowest number of neighbors
        #initialize the neighbors variable to a big value
        neighbors = 1000
        for i in hidden:
            if hidden[i].neighbors < neighbors:
                min_neighbor = hidden[i]
                neighbors = hidden[i].neighbors;
        
        #you have chosen the variable with least neighbors
        #now you need to know which scenario applies to the variable
        
        var = 0;
        #does it have parents?
        if min_neighbor.parents:
            var = 1
        
            #does it have children and parents?
            if min_neighbor.childs:
                var = 3
        else:
            #does it only have children
            if min_neighbor.childs:
                var = 2
        
            
        BN.sum_prodFormulation(self, min_neighbor, var, graph)
            

    def sum_prodFormulation(self, hidden, var, graph):
        #calculate the conditional probability without the hidden variable
        #inputs:
        #hidden - the hidden variable
        #var - the variable var that specifies the characteristics of the hidden variable
        #graph - the graph of the problem
        #outputs:
        #table - the table of probability without the hidden variable
        
        if not var:
            print('ERROR: hidden variable does not belong to the network')
        
        #it only has parents
        if var == 1:
            
            table = {}
            for i in range(0, len(hidden.values)):
                #one of values (T or F); convert to lower case
                l = hidden.values[i].lower()
                for i in range(0, len(hidden.table)/2):
                    
                    
        
        
        
        
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
                            hidden[i].childs.append(graph[j])
                        
            hidden[i].neighbors = count;
            
        
        return hidden
            
            
            
                    
                        
                        
                        
                    
                    
        