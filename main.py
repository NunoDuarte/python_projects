from readFile import readFile
from GSAT import GSAT
from WalkSAT import WalkSAT
from DPLL import DPLL

file = readFile('input.cnf')
file = file.openFile()

KB = file.readClauses(file)
print (KB)

## uf20-files take on average 30 s using GSAT
max_restarts = 1000000;
max_climbs = 5;

## uf20-files are almost instantly for the WalkSAT
max_flips = 3000;
probability = 5;

# GSAT = GSAT(KB, file, max_restarts, max_climbs);
# solution = GSAT.search();
# 
# print (solution)

# WalkSAT = WalkSAT(KB, file, probability, max_flips);
# solution = WalkSAT.search();
# #print (random.choice([0]*20 + [1]*80))
# print (solution)

DPLL = DPLL(KB, file);
solution = DPLL.satisfiable();
print (solution)



# print (random.randint(0,1))


