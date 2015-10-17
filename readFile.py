from Node import Node

class readFile(object):
    
    
    def __init__(self, file): 
        
        self.file = file;
        self.f = 0;
        
    def openFile(self,):
        
        f = open(self.file, 'r')
        self.f = f;
        #Read first line of file
        first_line = f.readline()
        #Remove \n (the enter symbol)
        first_line = first_line.rstrip()
        if '.cli' in self.file:
            #convert to integer
            f.numClients = int(first_line);
        if '.map' in self.file:
            #Split the strings
            first_line = first_line.split(' ')
            #convert to integer
            first_line = [int(p) for p in first_line];
            f.numCities = first_line[0];
            f.numConnects = first_line[1];
            
        
        return f
    
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
        node.cost = line[3];
        node.duration = line[4];
        node.initTime = line[5];
        node.finTime = line[6];
        node.duration = line[7];
        
        graph.append(node);
        
        return graph

        
        