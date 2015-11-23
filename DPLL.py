import string

class DPLL(object):
    
    def __init__(self, KB, file):
        
        self.KB = KB;
        self.variables = file.variables;
        self.clauses = file.clauses;   
        self.exit = 0
        self.count = 0;
        self.model = {}

    def satisfiable(self, ):
        
        clauses = self.KB;
        symbols = list(string.ascii_uppercase[0:self.variables]);
        i = 1;
        while( len(symbols) != self.variables):
            symbols.append('A' + str(i));
            i = i +1
        
        return DPLL.search(self, clauses, symbols, self.model)
    
    def search(self, clauses, symbols, model):
        if self.exit:
            return model
        if DPLL.check_false_clauses(self, clauses, self.model) == 0:
            DPLL.remove_sym_model(self, self.model, symbols)
            return False
        n = DPLL.check_clauses(self, clauses, self.model)
        if n == self.clauses:
            #if all clauses are true return the model
            self.exit = 1;    
            return self.model
        [P, value] = DPLL.find_pure_symbol(self, clauses, symbols, self.model)
        if P is not None:
            number = DPLL.pop_symbol(self, symbols, P)
            symbols.pop(number)
            return DPLL.search(self, clauses, symbols, self.model.update({P:value}))
        [P, value] = DPLL.find_unit_clause(self, clauses, symbols, self.model)
        if P is not None:
            number = DPLL.pop_symbol(self, symbols, P)
            symbols.pop(number)
            return DPLL.search(self, clauses, symbols, self.model.update({P:value}))
        return (DPLL.search(self, clauses, symbols[1:], self.model.update({symbols[0]:True}))
            or DPLL.search(self, clauses, symbols[1:], self.model.update({symbols[0]:False})))
            
            
    def remove_sym_model(self, model, symbols):
        # Before you go back you need to remove from the model the variables that are no longer in the truth model and belong to 
        # the not-assignment variables (symbols)
        #input: the model/assignment so far and the symbols that are left
        #output: the model with just the assign variables
        
        for i in symbols:
            if i in model:
                del model[i]
        
        return model
                    
    def check_false_clauses(self, clauses, model):
        #checks if there is any false clause
        #input: all the clauses, and the current model
        #output: 0 if true, -1 if not true
        
        if not model:
            # if there is nothing in the model just return some number so it can continue to find the assignment
            return -1
        else:
            for i in range(0, len(clauses)):
                count = 0;                    
                for k in clauses[i]:
                    for j in model:
                        if k == j:
                            if clauses[i][k] != model[j]:
                                count = count + 1;
                if count == len(clauses[i]):
                    # This means that there is at least one clauses that all of the literals are false
                    return 0
            
            return -1                
        
    
    def find_unit_clause(self, clauses, symbols, model):
        #find unit clauses
        #input: clauses, symbols and the current model
        #output: variable and value of unit clause if exists
        
        if not model:
            # if there is nothing in the model just return some number so it can continue to find the assignment
            return (None, None)
        
        for j in model:
            for i in range(0, len(clauses)):
                count = 0;     
                total = 0;     
                not_count = 0;          
                for k in clauses[i]:
                    total = total + 1;
                    if j == k:
                        if clauses[i][k] != model[j]:
                            count = count + 1;
                    else:
                        not_count = not_count + 1;
                        P = k;
                        value = clauses[i][k]
                            
                if count + not_count == total:
                    if not_count == 1:
                        if P not in model:
                            # this means that only one is not true!
                            return (P, value)
        
        return (None, None)
                    
                
                
    def pop_symbol(self, symbols, literal):
        #if there is a unit clause or unit symbol it needs to be removed from the symbols
        #input: symbols and the literal to be removed
        #output: the position in the symbols vector.
        
        for i in range(0, len(symbols)):
            if symbols[i] == literal:
                return i
        
    def check_clauses(self, clauses, model):
        #check the clauses if they are being satisfied
        #input: the assignment
        #output: the clauses that are true
               
        if not model:
            # if there is nothing in the model just return some number so it can continue to find the assignment
            return -1
        else:
            clauses_true = 0;
            # check for repeated clauses!!!!!
            for i in range(0, len(clauses)):
                count = 0;                    
                for k in clauses[i]:
                    for j in model:
                        if j == k:
                            if clauses[i][k] == model[j]:
                                count = count + 1;
                if count > 0:
                    clauses_true = clauses_true + 1;
            
            return clauses_true;
                        
    def find_pure_symbol(self, clauses, symbols, model):
        #it finds pure symbols
        #input: clauses, symbols and the current model
        #output: the variables and value for the pure symbol if it exists
        
        List = list(string.ascii_uppercase[0:self.variables]);
        i = 1;
        while( len(List) != self.variables):
            List.append('A' + str(i));
            i = i +1
            
        value = {}
        
        for i in range(0, len(List)):
            value[List[i]] = 2
            
        
        for i in range(0, len(clauses)):
            for j in clauses[i]:
                if DPLL.in_symbols(self, j, symbols):
                    if value[j] == 2:
                        value[j] = clauses[i][j];
                    if value[j] != clauses[i][j]:
                        value[j] = -1;
                    if value[j] == -1:
                        #it means that you found the literal and its complementary. So it is NOT a pure symbol
                        value[j] = -1;
        
        for i in value:
            if value[i] != -1:
                if value[i] != 2:
                    if i not in model:
                        return (i, value[i])
                
        return (None, None)
            
            
    def in_symbols(self, variable, symbols):
        #check if the variable is in symbols
        #input: variable and the symbols vector
        #output: true if yes, false if not.
        
        for i in symbols:
            
            if i == variable:
                return True
        
        return False         
            
            