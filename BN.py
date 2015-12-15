import numpy as np
import copy
import itertools

class BN(object):
    
    def __init__(self, graph, query_variable):
        
        self.graph = graph
        self.q_variable = query_variable;
        self.exit = 0
        self.table = []
    
    def run(self, ):
        
        #find hidden variables
        hidden = BN.hidden(self)
        
        if not hidden:
            print (' no hidden variable')
        
        #now an elimination ordering needs to be determined
        hidden = BN.min_neighbors(self, hidden, self.graph)
        
        #auxiliary graph
        aux_graph = self.graph;
    
            
        BN.VE_alg(self, aux_graph, hidden, self.q_variable)
        return self.table

    def VE_alg(self, graph, hidden, q_variable):
        
        if not hidden:
            self.graph = graph          
            self.exit = 1
            
        if self.exit:
            return True
        
        #start with the hidden variable with the lowest number of neighbors
        #initialize the neighbors variable to a big value
        neighbors = 1000
        for i in range(0, len(hidden)):
            if hidden[i].neighbors < neighbors:
                min_neighbor = hidden[i]
                number = i
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
        
        
        [graph, self.table] = BN.sum_prodFormulation(self, min_neighbor, var, graph)
        #remove hidden variable
        hidden.pop(number)
        BN.VE_alg(self, graph, hidden, self.q_variable)

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
            
            table = [[0 for i in range( len(hidden.parents) + 1)] for j in range(pow(2, len(hidden.parents)))]
            table = sum(hidden.table[-1][i+pow(2, len(hidden.parents))] for i in range(0, len(len(hidden.table[:]/2))))
            
            return (graph, table)
        
        if var == 2:
            
            
            for i in range(0, len(hidden.childs)):
                child = hidden.childs[i]
                #check what is the index of the child
                index = 0
                count = 0
                for i in child.parents:
                    count = count + 1
                    if i == hidden.name or i == hidden.alias:
                        index = count
                
                table = []
                table = child.table[:]
                #print (range(0,len(child.table[:][0:index]) + range(len(child.table[:][index + 1:]))))
                i = 0
                while i < len(table):
                    if table[i][index] == 'f':
                        table[i][-1] = float(table[i][-1])*float(hidden.table[1][-1]) + float(table[i+pow(2, len(child.parents) - index)][-1])*float(hidden.table[0][-1])
                        #remove repeated row
                        del table[(i+pow(2, len(child.parents) - index))]
                
                    if table[i][index] == 't':
                        table[i][-1] = float(table[i][-1])*float(hidden.table[0][-1]) + float(table[i+pow(2, len(child.parents) - index)][-1])*float(hidden.table[1][-1])
                        #remove repeated row
                        del table[(i+pow(2, len(child.parents) - index))]

                    i = i+1
                table = [[x[0:index], x[index+1:]] for x in table]
                for i in range(0, len(graph)):
                    if graph[i].name == child.name:
                        graph[i].table = table
                        for j in range(0, len(graph[i].parents)):
                            if graph[i].parents[j] == hidden.name or graph[i].parents[j] == hidden.alias:
                                del graph[i].parents[j]
            
            return (graph, table)
        
        if var == 3:
            #if the hidden variable has children and parents
            
            #count the number of variables you have
            count = len(hidden.childs)
            count = count + len(hidden.parents)
            
            table = [[0 for i in range(0, count + 1)] for j in range(0, pow(2, count))]
            
            index = 0
            index_parent = 0
            index_child = 0
            mux_1 = 1
            mux_2 = 1
            for i in itertools.product(['t','f'],repeat=count):
                table[index] = [i] + [0]

                for j in range(0, len(hidden.childs)):
                    child = hidden.childs[j]
                    for k in range(0, len(child.parents)):
                        if child.parents[k] == hidden.name or child.parents[k] == hidden.alias:
                            parent = k
                    value_1 = float(child.table[index_child][-1])
                    value_2 = float(child.table[index_child+pow(2, len(child.parents) - parent)][-1])
                    
                    
                    mux_1 = value_1*mux_1
                    mux_2 = value_2*mux_2
                index_child = index_child + 1
                if index_child >= len(child.table)/2:
                    index_child = 0;
                
                #the parents
                value_1 = hidden.table[index_parent][-1][0]
                value_2 = hidden.table[index_parent+pow(2, len(hidden.parents))][-1][0]
                    
                mux_1 = value_1*mux_1
                mux_2 = value_2*mux_2 
                
                table[index][-1] = mux_1 + mux_2
                index_parent = index_parent + 1
                if index_parent >= len(hidden.table)/2:
                    index_parent = 0
                
                #reset
                mux_1 = 1
                mux_2 = 1
                index = index + 1
                
            for i in range(0, len(graph)):
                if graph[i].name == hidden.name:
                    for j in range(0, len(graph[i].childs)):
                        for k in range(0, len(graph)):
                            if graph[k].name == graph[i].childs[j].name or graph[k].name == graph[i].childs[j].alias:
                                graph[k].table = table
                                for l in range(0, len(graph[k].parents)):
                                    if graph[k].parents[l] == hidden.name or graph[k].parents[l] == hidden.alias:
                                        del graph[k].parents[l]
                                        #graph[k].parents.append()
                    #table[index][i[j]] = 
            
            return (graph, table)  
                
            
        
        
        
        
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
            
            
            
                    
                        
                        
                        
                    
                    
        