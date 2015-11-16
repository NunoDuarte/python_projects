from readFile import readFile
from GSAT import GSAT
from WalkSAT import WalkSAT

file = readFile('input.cnf')
file = file.openFile()

KB = file.readClauses(file)
print (KB)



max_restarts = 3;
max_climbs = 5;
max_flips = 3;
probability = 5;

GSAT = GSAT(KB, file, max_restarts, max_climbs);
solution = GSAT.search();

print (solution)

WalkSAT = WalkSAT(KB, file, probability, max_flips);
solution = WalkSAT.search();
#print (random.choice([0]*20 + [1]*80))
print (solution)


# print (random.randint(0,1))


