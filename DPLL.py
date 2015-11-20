import string

class DPLL(object):
    
    def __init__(self, KB, file):
        
        self.KB = KB;
        self.variables = file.variables;
        self.clauses = file.clauses;   
        self.exit = 0
        self.count = 0;

    def satisfiable(self, ):
        
        clauses = self.KB;
        symbols = list(string.ascii_uppercase[0:self.variables]);
        
        return DPLL.search(self, clauses, symbols, {})
    
    def search(self, clauses, symbols, model):
        if self.exit:
            return model
        if DPLL.check_false_clauses(self, clauses, model) == 0:
            return False
        n = DPLL.check_clauses(self, clauses, model)
        if n == self.clauses:
            self.exit = 1;    
            return model
        [P, value] = DPLL.find_pure_symbol(self, clauses, symbols, model)
        if P is not None:
            number = DPLL.pop_symbol(self, symbols, P)
            symbols.pop(number)
            DPLL.search(self, clauses, symbols, model.update({P:value}))
        [P, value] = DPLL.find_unit_clause(self, clauses, symbols, model)
        if P is not None:
            number = DPLL.pop_symbol(self, symbols, P)
            symbols.pop(number)
            DPLL.search(self, clauses, symbols, model.update({P:value}))
        print (symbols)
        print (model)
        print (symbols[0])
        return (DPLL.search(self, clauses, symbols[1:], model.update({symbols[0]:True}))
            or DPLL.search(self, clauses, symbols[1:], model.update({symbols[0]:False})))
            
    def check_false_clauses(self, clauses, model):
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
        
        for i in range(0, len(symbols)):
            if symbols[i] == literal:
                return i
        
    def check_clauses(self, clauses, model):
        
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
        
        List = list(string.ascii_uppercase[0:self.variables]);
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
        
        for i in symbols:
            
            if i == variable:
                return True
        
        return False         
            
            