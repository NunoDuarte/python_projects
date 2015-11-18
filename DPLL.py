import string

class DPLL(object):
    
    def __init__(self, KB, file):
        
        self.KB = KB;
        self.variables = file.variables;
        self.clauses = file.clauses;   

    def satisfiable(self, ):
        
        clauses = self.KB;
        symbols = list(string.ascii_uppercase[0:self.variables]);
        
        return DPLL.search(self, clauses, symbols, {})
    
    def search(self, clauses, symbols, model):
        n = DPLL.check_clauses(self, clauses, model);
        if n == 0:
            return False
        if n == self.clauses:
            return True
        else:
            0
        
    def check_clauses(self, clauses, model):
        
        if not model:
            # if there is nothing in the model just return some number so it can continue to find the assignment
            return -1
        else:
            clauses_true = 0;
            for j in model:
                for i in range(0, len(clauses)):
                    for k in clauses[i]:
                        count = 0;
                        
                        if j == k:
                            if clauses[i][k] == model[j]:
                                count = count + 1;
                    if count > 0:
                        clauses_true = clauses_true + 1;
            
            return clauses_true;
                        
    def find_pure_symbol(self, symbols, clauses, model):
        
        value = list(string.ascii_uppercase[0:self.variables]);
        for i in value:
            value[i] = 0;
            
        
        for i in range(0, len(clauses)):
            for j in clauses[i]:
                if DPLL.in_symbols(self, j, symbols):
                    if value[j] == 0:
                        value[j] = clauses[i][j];
                    if value[j] == clauses[i][j]:
                        
                
            
            
    def in_symbols(self, variable, symbols):
        
        for i in symbols:
            
            if i == variable:
                return True
        
        return False         
            
            