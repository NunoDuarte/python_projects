import string

class DPLL(object):
    
    def __init__(self, KB, file):
        
        self.KB = KB;
        self.variables = file.variables;
        self.clauses = file.clauses;   

    def satisfiable(self, ):
        
        clauses = self.clauses;
        symbols = list(string.ascii_uppercase[0:self.variables]);
        
        return DPLL.search(self, clauses, symbols, {})
    
    def search(self, clauses, symbols, model):
        0
        
    def check_clauses(self, clauses, model):
        
        if not model:
            return True
        else:
            0
            