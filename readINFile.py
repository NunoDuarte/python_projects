class readINFile(object):
    
    def __init__(self, file):
        
        self.file = file
        self.query = 0
        self.evidence = {}
        
        
    def readfile(self, graph):
        
        with open(self.file, 'r') as fp:
            for line in fp:
                   
                #to check if there is comment lines
                if( line[0] == '#'):
                    continue
                
                #Read first meaningful line of file
                if 'QUERY' in line:
                    var = 1;
                if 'EVIDENCE' in line:
                    var = 2;
                
                if var == 1:
                    #Remove \n (the enter symbol) 
                    line = line.rstrip()   
                    p_line = line.split(' ') 
                    self.query = p_line[1];
                    
                    #checks if query variable exists in the graph
                    count = 0;
                    for i in range(0, len(graph)):
                        if graph[i].name == p_line[1] or graph[i].alias == p_line[1]:
                            count = count + 1
                    
                    if not count:
                        print ('ERROR: query variable does not exist')
                    
                    continue
                
                if var == 2:
                    #Remove \n (the enter symbol) 
                    line = line.rstrip()   
                    p_line = line.split(' ') 
                    
                    #checks if evidence has the correct amount of information
                    if int(p_line[1])*2 + 2 != len(p_line):
                        print ('ERROR: wrong size format')
                    
                    for i in range(0, int(p_line[1])):
                        #we want the first value and its pair, and also we don't want to count the first 2 values 
                        #which are the name and number of evidences
                        self.evidence[p_line[2*(i)+2]] = p_line[2*(i)+1+2];
                    continue
                
            return self
                                            
                    
                    
        
        