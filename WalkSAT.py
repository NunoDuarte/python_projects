import string
import random

class WalkSAT(object):
    
    def __init__(self, KB, file, p, max_flips):
        
        self.KB = KB;
        self.variables = file.variables;
        self.clauses = file.clauses;
        self.p = p;
        self.max_flips = max_flips;
        
    def search(self,):
        
        assign = {}
        List = list(string.ascii_uppercase[0:self.variables]);
        
        # initiate all proposition symbols with random assignment
        assign = WalkSAT.random_gen_assign(self, assign, List);
        
        for i in range(0, self.max_flips):
            n = WalkSAT.check_clauses(self, assign)
            if self.clauses == n:
                return assign
            false_clauses = WalkSAT.false_clauses(self, assign);
            false_clause = WalkSAT.select_one(self, false_clauses);
            if_statement = random.choice([0]*self.p*10 + [1]*(1-self.p)*10);
            if if_statement == 0:
                symbol = WalkSAT.random_value(self, false_clause)            
                assign = WalkSAT.change_model(self, assign, symbol);
            else:
                assign = WalkSAT.most_satisfied(self, assign, n, false_clause)

    def change_model(self, assign, symbol):
        
        for i in symbol:
            assign[i] = symbol[i];
        return assign
            
    def random_value(self, clause):
        
        size = len(clause);
        number = random.randint(0, size-1);
        
        count = 0;
        for i in clause:
            if count == number:
                if clause[i] == True:
                    value = clause[i];
                    index = i;
                if clause[i] == False:
                    value = clause[i];
                    index = i;
            count = count + 1;
        
        symbol = {};
        symbol[index] = value;
        return symbol
            
    def select_one(self, false_clauses):
        
        size = len(false_clauses);
        number = random.randint(0, size-1);
        
        false_clause = false_clauses[number];
        return false_clause
    
    
    def false_clauses(self, assign):
        
        KB = self.KB;
        
        clauses = [];
        for i in range(0, len(KB)):
            count = 0;
            for j in KB[i]:
                
                if KB[i][j] == assign[j]:
                    count = count + 1;
                    
            if count == 0:
                clauses.append(KB[i])
                
        return clauses;          
                

    def random_gen_assign(self, assign, List):
        # random generation of value for an assignment
        
        for i in range(0, self.variables):
            randomValue = random.randint(0,1);
            
            if randomValue == 0:
                assign[List[i]] = False;
            if randomValue == 1:
                assign[List[i]] = True;
                
        return assign     
        
    def check_clauses(self, assign):
        # check which clauses are true for a specific assignment
        
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
    
    
    def most_satisfied(self, assign, n_max, false_clause):
        
        old_assign = assign.copy();
        
        for j in false_clause:
            assign =  old_assign.copy();
            for i in assign:
                if j == i:
                    if assign[i] == False:
                        assign[i] = True;
                        n = WalkSAT.check_clauses(self, assign);
                        if n > n_max:
                            new_assign = assign;
                            n_max = n;
                        continue;
                        
                    if assign[i] == True:
                        assign[i] = False;
                        n = WalkSAT.check_clauses(self, assign);
                        if n > n_max:
                            new_assign =  assign;
                            n_max = n;
                        continue;
                
        if not new_assign:
            return old_assign
        else:
            return new_assign 
        
    