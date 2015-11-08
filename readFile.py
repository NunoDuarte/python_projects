import string


class readFile(object):
    
    def __init__(self, arg):
        
        self.file = arg;
        self.f = 0;
        self.format = 'cnf';
        self.variables = 0;
        self.clauses = 0;
        
    def openFile(self,):
        
        f_open = open(self.file, 'r')
        self.f = f_open;
        
        line = f_open.readline();
        
        #to check if there is comment lines
        while( line[0] == 'c'):
            print (line)
            line = f_open.readline();
            
        #read line starting with 'p'
        p_line = line;
        p_line = p_line.split(' ');
        
        #save format, variables and clauses of the file
        format = p_line[1];
        variables = int(p_line[2]);
        clauses = int(p_line[3]);
        
        #save to file
        self.format = format;
        self.variables = variables;
        self.clauses = clauses;
        
        
        return self
    
    def readClauses(self, file):
        
        f_open = self.f;
        List = list(string.ascii_uppercase[0:self.variables]);
        
        for i in range(0, self.clauses):
            
            line = f_open.readline();
            line = line.split(' ');
            line = [int(p) for p in line];
            
            print (line)
            
            clause_dict = {};
            for j in range(0, len(line)):
                if line[j] == 0:
                    continue
                clause_dict[List[abs(line[j])-1]] = False;
            
            print (clause_dict)
                
            
    
    
    
    