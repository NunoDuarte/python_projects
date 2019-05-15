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
        i = 1;
        while( len(List) != self.variables):
            List.append('A' + str(i));
            i = i +1
        
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
                    [best, count] = GSAT.best_sucessor_of_assign(self, assign, n)
                    A = GSAT.random_best(self, best, count);
                
                
                
            
    def random_best(self, best, number):     
        #From the best assignments possible it choose one randomly
        #input: the vector of the best assignments and the total number of them
        #output: the best assignment chosen randomly
        
        if number < 1:
            #if it only one just choose that one
            return best
        else:
            randomValue = random.randint(0, len(best)-1)
            assign = best[randomValue];
            return assign;    
            
               

    
    def random_gen_assign(self, assign, List):
        #it generates randomly the values to the variables of the assignment.
        #input: the assignment itself and the list of variables
        #output the assignment with the values of true and false assigned
        
        for i in range(0, self.variables):
            randomValue = random.randint(0,1);
            
            if randomValue == 0:
                assign[List[i]] = False;
            if randomValue == 1:
                assign[List[i]] = True;
                
        return assign
    
    def check_clauses(self, assign):
        #check the clauses if they are being satisfied
        #input: the assignment
        #output: the clauses that are true
        
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
        #it chooses the assignment that changing a value of a variable will satisfy more clauses than the previous value
        #input: the assignment, and number of satisfied clauses currently
        #output the new assignment and the new number of satisfied clauses
        
        old_assign = assign.copy();
        new_assign = [];
        
        count = 0;
        for i in assign:
            assign =  old_assign.copy();
            if assign[i] == False:
                assign[i] = True;
                n = GSAT.check_clauses(self, assign);
                if n > n_max:
                    new_assign.append(assign);
                    count = count + 1;
                continue;
                
            if assign[i] == True:
                assign[i] = False;
                n = GSAT.check_clauses(self, assign);
                if n > n_max:
                    new_assign.append(assign);
                    count = count + 1;
                continue;
            
        if not new_assign:
            return (old_assign, count)
        else:
            return (new_assign, count)
            
            
        
        
        
        
        
            
        
        
        