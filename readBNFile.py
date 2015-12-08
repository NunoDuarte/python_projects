from Node import Node

class readBNFile(object):
    
    
    def __init__(self, file): 
        
        self.file = file;
        self.f = 0;
        self.name = 0
        self.alias = 0
        self.parents = []
        self.values = []
        
        self.variable = 0;
        self.table = {};
        
    
    def readfile(self, Graph):
        
        with open(self.file, 'r') as fp:
            for line in fp:
                   
                #to check if there is comment lines
                if( line[0] == '#'):
                    continue
                
                #Read first meaningful line of file
                if 'VAR' in line:
                    var = 1;
                    continue
                if 'CPT' in line:
                    var = 2;
                    continue
                if var == 1:
                    print (line)
                    if 'name' in line:
                        #Remove \n (the enter symbol) 
                        line = line.rstrip()   
                        p_line = line.split(' ') 
                        self.name = p_line[1];
                        continue
                    if 'values' in line:
                        #Remove \n (the enter symbol) 
                        line = line.rstrip()   
                        p_line = line.split(' ') 
                        for i in range(0, len(p_line) - 1):
                            self.values.append(p_line[i+1]);
                        continue
                    if 'parents' in line:
                        #Remove \n (the enter symbol) 
                        line = line.rstrip()   
                        p_line = line.split(' ') 
                        for i in range(0, len(p_line) - 1):
                            self.parents.append(p_line[i+1]);
                        continue
                    if 'alias' in line:
                        #Remove \n (the enter symbol) 
                        line = line.rstrip()   
                        p_line = line.split(' ') 
                        self.alias = p_line[1];
                        continue
                    else:
                        var = 0;
                        Graph = readBNFile.AddNode(self, Graph)
                        #break out of the for loop
                if var == 2:
                    if 'var' in line:
                        #Remove \n (the enter symbol) 
                        line = line.rstrip()   
                        p_line = line.split(' ') 
                        self.variable = p_line[1];
                        (node, num) = readBNFile.FindNode(self, Graph, self.variable);                        
                        continue
                    if 'table' in line:
                        if node:
                            print (line) 
                            #Remove \n (the enter symbol) 
                            p_line = line.rstrip()                          
                            p_line = p_line.split(' ');
                            node = readBNFile.AddTable(self, node, p_line, num, var)
                            if node == -1:
                                #it means table is separate by lines
                                var = 3;
                            else:
                                Graph[num] = node
                            continue
                        else:
                            print('ERROR: no variable name')
                            exit
                if var == 3:
                    (node, num) = readBNFile.FindNode(self, Graph, self.variable);  
                    #Remove \n (the enter symbol) 
                    p_line = line.rstrip()                          
                    p_line = p_line.split(' ');
                    node = readBNFile.AddTable(self, node, p_line, num, var)
                    Graph[num] = node
                
        return Graph
                        
                
                
    def AddNode(self, Graph):
        #check if it has a name and value
        if (self.name == 0 or not (self.values)):
            print ('ERROR: VAR doesnt have a name or value');     
            exit;
        
        # Create a Node
        node = Node();
        node.name = self.name
        node.values = self.values
        node.alias = self.alias
        node.parents = self.parents;
        
        #reset variables
        self.name = 0;
        self.values = [];
        self.alias = 0;
        self.parents = [];
        
        Graph.append(node)
        
        return Graph
    
    def FindNode(self, Graph, variable):
        # Look for node corresponding to the variable name in CPT
        
        for i in range(0, len(Graph)):
            
            if(Graph[i].name == variable or Graph[i].alias == variable):
                return [Graph[i], i]
    
        print('ERROR: no corresponding Node for CPT')
        exit
    
    
    def AddTable(self, Node, Line, Int, typeOf):
        #Complete the conditional probability for a specific variable
        #Inputs:
        #Node - the node that of the specific variable
        #Line - the line that has the probabilities of the table
        #Int - the position of the Node in the Graph to be reintroduced. 
        #type - how are they separate (white spaces or newlines)
        
        #the number of parents for a specific variable

        num = len(Node.parents);
        if len(Line) == 1:
            return -1;
            
        if typeOf == 2:
            #check if the table has all the parameters required for a correct evaluation
            if len(Line) != (1 + (pow(2,1+num))*(1+num) + (pow(2,1+num))):
                print ('ERROR: line size not correct')
        if typeOf == 3:
            #check if the table has all the parameters required for a correct evaluation (specific variable + number of parents + value)
            if len(Line) != (1 + num + 1):
                print ('ERROR: line size not correct')
        
        count = 0
        element = ''
        for p in Line:
            if p == 'table':
                continue
            else:
                #compare if the count of parents is equal to the (number of parents + the specific variable)
                if count != num + 1:
                    #add to the element name the value of the parent or the value of the specific variable
                    element = element + p;
                    #increment the count
                    count = count + 1;
                else:
                    #Save to table and reset the count of the parents and the name of the element
                    Node.table[element] = p;
                    element = ''
                    count = 0;
                    print (Node.table)
        
        return Node
            

        
        