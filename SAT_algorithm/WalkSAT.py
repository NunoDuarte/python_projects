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
        i = 1;
        while( len(List) != self.variables):
            List.append('A' + str(i));
            i = i +1
        
        # initiate all proposition symbols with random assignment
        assign = WalkSAT.random_gen_assign(self, assign, List);
        
        for i in range(0, self.max_flips):
            n = WalkSAT.check_clauses(self, assign)
            if self.clauses == n:
                return assign
            false_clauses = WalkSAT.false_clauses(self, assign);
            false_clause = WalkSAT.select_one(self, false_clauses);
            
            #choose from the two options randomly:   1. choose a random variable from the false_clause and change it in the assignment
            #                                        2. choose the variable which a value satisfies the most clauses in the KB
            if_statement = random.choice([0]*self.p*10 + [1]*(1-self.p)*10);
            if if_statement == 0:
                symbol = WalkSAT.random_value(self, false_clause)            
                assign = WalkSAT.change_model(self, assign, symbol);
            else:
                assign = WalkSAT.most_satisfied(self, assign, n, false_clause)

    def change_model(self, assign, symbol):
        #add the new variable with the new value from the random_value
        #input: variable with value
        #output: assignment with the new variable with value
        
        for i in symbol:
            assign[i] = symbol[i];
        return assign
            
    def random_value(self, clause):
        #chose random value a variable in a false clauses
        #input: a false_clause
        #output: returns a variable with a value 
        
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
        # select one of the false_clauses
        #input: all the false clauses
        #output: just one false clause
        
        size = len(false_clauses);
        number = random.randint(0, size-1);
        
        false_clause = false_clauses[number];
        return false_clause
    
    
    def false_clauses(self, assign):
        # find all of the clauses that are not satisfied by the assignment
        #input: the assignment
        #output: the set of clauses that are not satisfied
        
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
    
    
    def most_satisfied(self, assign, n_max, false_clause):
        #it returns the assignment that satisfies the most clauses
        #input: assign, number of satisfied clauses, and all the false clauses
        #output: new assignment
        
        old_assign = assign.copy();
        new_assign = [];
        
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
        
    