from Node import Node
class readFile(object):
    
    
    def __init__(self, file): 
        
        self.file = file;
        self.f = 0;
        self.numCities = 0
        self.numConnects = 0
        
    def openFile(self,):
        
        f_open = open(self.file, 'r')
        self.f = f_open
        #Read first line of file
        first_line = f_open.readline()
        #Remove \n (the enter symbol)
        first_line = first_line.rstrip()
        if '.cli' in self.file:
            #convert to integer
            self.numClients = int(first_line);
        if '.map' in self.file:
            #Split the strings
            first_line = first_line.split(' ')
            #convert to integer
            first_line = [int(p) for p in first_line];
            self.numCities = first_line[0];
            self.numConnects = first_line[1];
            
        
        return self.f
    
    def readLine(self,):
        
        line = self.f.readline()
        #Remove \n (the enter symbol)
        line = line.rstrip()
        
        #Split the strings
        line = line.split(' ')
        
        return line
    
    
    def readMap(self, graph):
        
        line = self.f.readline();
        #Remove \n (the enter symbol)
        line = line.rstrip()
        
        #Split the strings
        line = line.split(' ')        
        
        node = Node();
        node.departure = line[0];
        node.arrival = line[1];
        node.type = line[2];
        node.cost = int(line[4]);
        node.duration = int(line[3]);
        node.initTime = int(line[5]);
        node.finTime = int(line[6]);
        node.intervals = int(line[7]); 
        
        graph.append(node);
        
        #The inverted route also is available
        node = Node();
        node.departure = line[1];
        node.arrival = line[0];
        node.type = line[2];
        node.cost = int(line[4]);
        node.duration = int(line[3]);
        node.initTime = int(line[5]);
        node.finTime = int(line[6]);
        node.intervals = int(line[7]); 
               
        graph.append(node);
        
        return graph

        
        