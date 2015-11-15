import string
import random

class GSAT(object):
    
    def __init__(self, KB, file, max_restarts, max_climbs):
        
        self.KB = KB;
        self.variables = file.variables;
        self.clauses = file.clauses;
        self.max_restarts = max_restarts;
        self.max_climbs = max_climbs;
        
    def search(self,):
        
        assign = {}
        List = list(string.ascii_uppercase[0:self.variables]);
        
        # initiate all proposition symbols with assignment of False
        for i in range(0, self.variables):
            assign[List[i]] = False;
        
        for i in range(0, self.max_restarts):
            # A randomly generated truth assignment
            A = GSAT.random_gen_assign(self, assign, List)         
            for j in range(0, self.max_climbs):
                n = GSAT.check_clauses(self, A)
                if n == self.clauses:
                    return A;
                if n != self.clauses:
                    best = GSAT.best_sucessor_of_assign(self, assign, n)
                    A = GSAT.random_best(self, best);
                
                
                
            
    def random_best(self, best):     
       
        randomValue = random.randint(0, len(best)-1)
        assign = best[randomValue];
        
        return assign;    
            
               

    
    def random_gen_assign(self, assign, List):
        
        for i in range(0, self.variables):
            randomValue = random.randint(0,1);
            
            if randomValue == 0:
                assign[List[i]] = False;
            if randomValue == 1:
                assign[List[i]] = True;
                
        return assign
    
    def check_clauses(self, assign):
        
        KB = self.KB;
        
        clauses_true = 0;
        for i in range(0, len(KB)):
            count = 0;
            for j in KB[i]:
                
                if KB[i][j] == assign[j]:
                    count = count + 1;
                    
            if count > 0:
                clauses_true = clauses_true + 1;
                
        return clauses_true;
    
    def best_sucessor_of_assign(self, assign, n_max):
        
        old_assign = assign.copy();
        new_assign = [];
        
        for i in assign:
            assign =  old_assign.copy();
            if assign[i] == False:
                assign[i] = True;
                n = GSAT.check_clauses(self, assign);
                if n >= n_max:
                    new_assign.append(assign);
                continue;
                
            if assign[i] == True:
                assign[i] = False;
                n = GSAT.check_clauses(self, assign);
                if n >= n_max:
                    new_assign.append(assign);
                continue;
            
        if not new_assign:
            return old_assign
        else:
            return new_assign
            
            
        
        
        
        
        
            
        
        
        